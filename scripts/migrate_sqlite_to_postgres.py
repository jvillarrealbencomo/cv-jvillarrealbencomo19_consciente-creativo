import os
import argparse
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from sqlalchemy import create_engine, MetaData, select, text
from sqlalchemy.exc import SQLAlchemyError


def normalize_pg_url(url: str) -> str:
    # Forzar driver psycopg
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    # Forzar SSL en Render
    parsed = urlparse(url)
    q = dict(parse_qsl(parsed.query))
    q.setdefault("sslmode", "require")
    q.setdefault("connect_timeout", "20")
    new_query = urlencode(q)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def batched(rows, size=500):
    for i in range(0, len(rows), size):
        yield rows[i:i + size]


def main():
    parser = argparse.ArgumentParser(description="Migrate data from SQLite to Postgres")
    parser.add_argument("--reset", action="store_true", help="Truncate target Postgres tables before load")
    args = parser.parse_args()

    sqlite_url = os.getenv("SQLITE_URL", "sqlite:///instance/app.db")
    postgres_url = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")
    if not postgres_url:
        raise SystemExit("Missing POSTGRES_URL (or DATABASE_URL)")

    postgres_url = normalize_pg_url(postgres_url)

    sqlite_engine = create_engine(sqlite_url, future=True)
    pg_engine = create_engine(postgres_url, future=True, pool_pre_ping=True)

    sqlite_meta = MetaData()
    sqlite_meta.reflect(bind=sqlite_engine)

    pg_meta = MetaData()
    pg_meta.reflect(bind=pg_engine)

    # Excluir versionado de migraciones; incluir tablas funcionales (ej: app_metadata)
    excluded_tables = {"alembic_version"}
    sqlite_tables = [t for t in sqlite_meta.sorted_tables if t.name not in excluded_tables]

    try:
        with pg_engine.begin() as pg_conn:
            if args.reset:
                for table in reversed(sqlite_tables):
                    if table.name in pg_meta.tables:
                        pg_conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
                        print(f"[TRUNCATE] {table.name}")

            with sqlite_engine.connect() as sq_conn:
                for sq_table in sqlite_tables:
                    if sq_table.name not in pg_meta.tables:
                        print(f"[SKIP] Table not found in Postgres: {sq_table.name}")
                        continue

                    pg_table = pg_meta.tables[sq_table.name]
                    rows = sq_conn.execute(select(sq_table)).mappings().all()

                    if not rows:
                        print(f"[OK] {sq_table.name}: 0 rows")
                        continue

                    data = [dict(r) for r in rows]
                    for chunk in batched(data, 500):
                        pg_conn.execute(pg_table.insert(), chunk)

                    print(f"[OK] {sq_table.name}: {len(rows)} rows inserted")

            for table_name in pg_meta.tables:
                if table_name in excluded_tables:
                    continue
                pg_conn.execute(text(f"""
                    DO $$
                    DECLARE seq_name text;
                    BEGIN
                        SELECT pg_get_serial_sequence('"{table_name}"', 'id') INTO seq_name;
                        IF seq_name IS NOT NULL THEN
                            EXECUTE format(
                                'SELECT setval(%L, COALESCE((SELECT MAX(id) FROM "{table_name}"), 1), (SELECT COUNT(*) > 0 FROM "{table_name}"))',
                                seq_name
                            );
                        END IF;
                    END $$;
                """))

        print("\n✅ Migration completed successfully.")
    except SQLAlchemyError as e:
        raise SystemExit(f"❌ Migration failed: {e}")


if __name__ == "__main__":
    main()