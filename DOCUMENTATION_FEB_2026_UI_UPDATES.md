# UI & Metadata Updates (Post-Admin Navbar Update)

Date: 2026-02-05

This document summarizes the UI and metadata changes introduced after the Admin navigation bar update. It focuses on HomePage calls-to-action, section framing colors, card borders, button order for CV actions, and the new database-driven year/version values.

---

## 1) HomePage CTA updates

### A) Data Entry button next to Start Building
**Location:** [app/templates/index.html](app/templates/index.html#L12-L27)
- The hero CTA row now includes:
  - **Start Building** (`/forms/person`)
  - **Data Entry** (`/admin/data-management`)

### B) Removal of the old Data Entry button from the HomePage body
**Location:** [app/templates/index.html](app/templates/index.html)
- The only Data Entry CTA is now in the hero area. There is no separate Data Entry button inside the body sections.

---

## 2) Frame colors for “Available CV Profiles” and “Technical Evidence”

### A) Available CV Profiles section frame
**Location:** [app/templates/index.html](app/templates/index.html#L30-L76)
- Section wrapper uses:
  - Background: `#f8fafc`
  - Border: `1px solid #0d6efd`
  - Radius: `16px`

### B) Technical Evidence section frame
**Location:** [app/templates/index.html](app/templates/index.html#L78-L142)
- Section wrapper uses:
  - Background: `#f5f9ff`
  - Border: `1px solid #198754`
  - Radius: `16px`

---

## 3) Card border colors in both sections

### A) Available CV Profiles cards
**Location:** [app/templates/index.html](app/templates/index.html#L40-L71)
- Each profile card body uses:
  - Background: `#f8fafc`
  - Border: `1px solid #0d6efd`
  - Radius: `16px`

### B) Technical Evidence cards
**Location:** [app/templates/index.html](app/templates/index.html#L101-L134), [app/static/css/modern.css](app/static/css/modern.css#L287-L300)
- Border styles are applied by slug-based classes:
  - `card-border-ui-section-technical`: `1px solid #0d6efd`
  - `card-border-api-section-technical`: `1px solid #094dbf`
  - `card-border-data-section-technical`: `1px solid #198754`
  - All include `border-radius: 16px`

---

## 4) Button order in “Available CV Profiles” cards

**Location:** [app/templates/index.html](app/templates/index.html#L52-L88)

Current order (top to bottom):
1. **Preview CV**
2. **Export PDF**
3. **One-Page PDF**
4. **Edit Profile**
5. **View Settings**

This order ensures the primary viewing action is first, followed by export options and configuration links.

---

## 5) Dynamic year/version (database-driven)

### A) New table: `app_metadata`
**Location:** [app/models/app_metadata.py](app/models/app_metadata.py)
- Table schema:
  - `id` (INTEGER, primary key)
  - `key` (TEXT, unique, required)
  - `value` (TEXT, required)
  - `updated_at` (timestamp, auto-updated)

**Default records:**
- `application_name`: `API CV`
- `application_version`: `2026.1.0`
- `release_year`: `2026`

### B) Template injection & defaults
**Location:** [app/__init__.py](app/__init__.py#L41-L63)
- `ensure_app_metadata_defaults()` runs after table creation.
- A template context processor injects `app_metadata` for all templates.

### C) Footer now uses database values
**Location:** [app/templates/base.html](app/templates/base.html#L125-L133)
- The year is read from `app_metadata['release_year']`.
- The version is read from `app_metadata['application_version']`.

---

## 6) Time Period list now uses release year

**Location:** [app/templates/forms/experience_form.html](app/templates/forms/experience_form.html#L89-L99)
- The “Recent” time block uses the `release_year` value from `app_metadata`:
  - `2021-<release_year> (Recent)`
- This ensures the latest year is controlled by the database, not hardcoded.

---

## Summary Checklist

- HomePage CTA includes **Start Building** + **Data Entry** side by side. ✅
- No separate Data Entry CTA remains in the body sections. ✅
- Section frame colors updated for Available CV and Technical Evidence. ✅
- Card border colors defined by slug-based classes. ✅
- Available CV action buttons reordered. ✅
- Footer year/version values now read from `app_metadata`. ✅
- Time Period “Recent” range driven by `release_year`. ✅
