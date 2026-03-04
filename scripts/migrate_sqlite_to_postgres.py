import os
import argparse
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.exc import SQLAlchemyError


def normalize_pg_url(url: str) -> str:
    """Normaliza postgres:// a postgresql+psycopg:// para SQLAlchemy 2.0+"""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


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
    pg_engine = create_engine(postgres_url, future=True)

    sqlite_meta = MetaData()
    sqlite_meta.reflect(bind=sqlite_engine)

    pg_meta = MetaData()
    pg_meta.reflect(bind=pg_engine)

    # Exclusión explícita: alembic_version (versionado de migraciones)
    # Inclusión implícita: metadata + todas las tablas funcionales
    EXCLUDED_TABLES = {"alembic_version"}
    sqlite_tables = [t for t in sqlite_meta.sorted_tables if t.name not in EXCLUDED_TABLES]

    try:
        with pg_engine.begin() as pg_conn:
            if args.reset:
                # TRUNCATE en orden inverso por FK
                for table in reversed(sqlite_tables):
                    if table.name in pg_meta.tables:
                        pg_conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
                        print(f"[TRUNCATE] {table.name}")

            with sqlite_engine.connect() as sq_conn:
                for sq_table in sqlite_tables:
                    if sq_table.name not in pg_meta.tables:
                        print(f"[SKIP] Table not found in Postgres: {sq_table.name}")
                        continue

                    pg_table = Table(sq_table.name, MetaData(), autoload_with=pg_engine)
                    rows = sq_conn.execute(select(sq_table)).mappings().all()

                    if not rows:
                        print(f"[OK] {sq_table.name}: 0 rows")
                        continue

                    pg_conn.execute(pg_table.insert(), [dict(r) for r in rows])
                    print(f"[OK] {sq_table.name}: {len(rows)} rows inserted")

            # Ajuste de secuencias para columnas id
            for table_name in pg_meta.tables:
                if table_name in EXCLUDED_TABLES:
                    continue
                pg_conn.execute(text(f"""
                    DO $
                    DECLARE seq_name text;
                    BEGIN
                        SELECT pg_get_serial_sequence('"{table_name}"', 'id') INTO seq_name;
                        IF seq_name IS NOT NULL THEN
                            EXECUTE format(
                                'SELECT setval(%L, COALESCE((SELECT MAX(id) FROM "{table_name}"), 1), (SELECT COUNT(*) > 0 FROM "{table_name}"))',
                                seq_name
                            );
                        END IF;
                    END $;
                """))

        print("\n✅ Migration completed successfully.")
    except SQLAlchemyError as e:
        raise SystemExit(f"❌ Migration failed: {e}")


if __name__ == "__main__":
    main()
