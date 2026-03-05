# CV 2025 Credential Image Upload Feature

## Implementation Summary
**Branch:** `cv2025-credential-images`  
**Date:** January 5, 2026  
**Status:** ✅ Complete and Ready for Testing

---

## What Was Implemented

### 1. **Database Schema Updates**
Added credential image fields to two tables:
- **`education`** table: PhD, degrees, diplomas
- **`advanced_training`** table: courses and certifications

New columns for both:
- `image_path` - full image file path
- `image_thumbnail_path` - 200x200px thumbnail (auto-generated for images)
- `image_filename` - original filename
- `image_mime_type` - file type (image/jpeg, image/png, application/pdf)

**Migration:** `migrate_add_credential_images.py` (already run ✓)

---

### 2. **Image Service**
Created `app/services/image_service.py` with:
- **File validation:** PNG, JPG, PDF only; 5MB max
- **Secure naming:** `education_{id}_{timestamp}.jpg` pattern
- **Auto thumbnails:** 200x200px for images (JPEG format)
- **Safe cleanup:** Removes old images on replace/delete
- **Storage:** `app/static/uploads/education/` and `app/static/uploads/advanced_training/`

---

### 3. **API Updates**
Custom endpoints replacing generic CRUD for education and advanced training:

**Education Endpoints:**
- `POST /api/education` - Create with optional image upload
- `PUT /api/education/{id}` - Update with replace/remove image
- `GET /api/education` - List all (ordered by display_order)

**Advanced Training Endpoints:**
- `POST /api/advanced-training` - Create with optional image
- `PUT /api/advanced-training/{id}` - Update with replace/remove
- `GET /api/advanced-training` - List all (ordered by display_order)

**Features:**
- Accept `multipart/form-data` for file uploads
- Support `remove_image=true` flag to delete existing images
- Auto-replace old image when uploading new one
- Return full image URLs in responses (`image_url`, `image_thumbnail_url`)

---

### 4. **Form Updates**

#### Education Form (`app/templates/forms/education_form.html`)
- File upload input with preview
- Shows current credential image thumbnail + link
- "Remove existing image" checkbox
- Switched from JSON to FormData submission

#### Advanced Training Form (`app/templates/forms/advanced_training_form.html`)
- Same upload/preview/remove functionality
- Works for both courses and certifications

---

### 5. **List/Edit Interface** ⭐ NEW
Created admin list pages for managing records:

**`/admin/education`** - Education List View
- Shows all degrees with image indicators
- Edit button links to `/forms/education/{id}`
- Delete button (soft delete)
- Profile visibility badges

**`/admin/training`** - Advanced Training List View
- Shows courses & certifications
- Type icons (book for course, badge for cert)
- Same edit/delete functionality

**Navigation Updated:**
- Menu "Data Entry → Education" now goes to `/admin/education` (list view)
- Menu "Data Entry → Advanced Training" now goes to `/admin/training` (list view)
- Each list has "Add New" button at top

---

### 6. **CV Preview Updates**
Updated `app/templates/profile_view.html`:
- Education section shows credential thumbnails (if present)
- Advanced Training section shows credential images
- "View credential" links open full image in new tab
- PDFs show link only (no thumbnail)
- Section renamed to "Advanced Training & Certifications"

**Preview Only - PDFs remain image-free** ✓

---

### 7. **Image Linking Script**
Created `link_education_images.py` for one-time migration:
- Links manually copied images to existing records
- Generates thumbnails automatically
- Updates database paths

**Already run** - your 3 education images are now linked ✓

---

## How to Use

### For Users - Adding/Editing Credentials with Images

1. **Navigate to Data Entry**
   - Click "Data Entry" → "Education" (or "Advanced Training")
   - You'll see a **list view** with all existing records

2. **Edit Existing Record**
   - Click the **pencil icon** (Edit button) next to any record
   - Form will load with all current data
   - Scroll down to "Credential Image" section
   - See current image preview if one exists

3. **Upload New Image**
   - Click "Choose File"
   - Select PNG, JPG, or PDF (max 5MB)
   - Image will automatically replace old one on save

4. **Remove Image**
   - Check "Remove existing image" box
   - Image will be deleted on save

5. **Create New Record**
   - Click "Add New Education" button at top of list
   - Fill in degree details
   - Optionally upload credential image
   - Save

### For Viewing in CV

1. Go to Home → "Edit Profile" for any profile (QA Analyst, etc.)
2. Click "Preview CV" button
3. Scroll to **Education** and **Advanced Training** sections
4. Credential thumbnails appear below each entry
5. Click "View credential" to open full image

---

## File Structure

```
app/
├── models/
│   ├── education.py                 # Added image fields
│   └── advanced_training.py         # Added image fields
├── routes/
│   ├── api.py                       # Custom education/training endpoints
│   └── admin.py                     # Added list view routes
├── services/
│   └── image_service.py             # NEW - Upload/thumbnail service
├── static/uploads/
│   ├── education/                   # Education credential images
│   │   ├── education_1_*.jpg        # Auto-named files
│   │   └── education_1_*_thumb.jpg  # Auto-generated thumbnails
│   └── advanced_training/           # Training credential images
├── templates/
│   ├── forms/
│   │   ├── education_form.html      # Updated with upload UI
│   │   └── advanced_training_form.html  # Updated with upload UI
│   ├── admin/
│   │   ├── education_list.html      # NEW - List view
│   │   └── training_list.html       # NEW - List view
│   └── profile_view.html            # Shows credential images

Migration Scripts:
├── migrate_add_credential_images.py # DB migration (run ✓)
└── link_education_images.py         # One-time image linker (run ✓)
```

---

## Current Status

### ✅ Completed
- [x] Database migration
- [x] Image service with validation & thumbnails
- [x] API endpoints for upload/replace/remove
- [x] Education form with upload UI
- [x] Advanced training form with upload UI
- [x] CV Preview shows credential images
- [x] Admin list views with edit buttons
- [x] Navigation menu updated
- [x] Manual images linked to database (3 education records)

### 🧪 Ready to Test
1. Navigate to `/admin/education`
2. Click edit on "PhD in Educational Sciences"
3. See the credential image preview
4. Try uploading a new image or removing it
5. View changes in CV Preview (`/profile/1`)

---

## Technical Notes

### PDF Behavior
- PDFs are **accepted** for upload
- **No thumbnail** generated (only images get thumbnails)
- Link to open PDF in new tab provided
- Users can verify certificates externally

### Image Optimization
- Thumbnails: 200x200px, JPEG, 85% quality
- Original images preserved in full resolution
- Safe filenames prevent conflicts: `category_{id}_{timestamp}.ext`

### Deployment Considerations
- Images stored locally in `app/static/uploads/`
- For production with domain hosting:
  - Use Docker volume mount for persistence
  - Example: `-v /host/uploads:/app/app/static/uploads`
- PDF stays profile-picture-only (no credential images)

---

## Migration Path

If deploying to another environment:

1. **Copy database** (includes image paths)
2. **Copy upload folders:**
   ```
   app/static/uploads/education/
   app/static/uploads/advanced_training/
   ```
3. **Run on new server** - paths are relative, will work automatically

---

## Summary

**What the user sees:**
- Go to "Data Entry → Education" to see a **table of all degrees**
- Click **Edit** button (pencil icon) to modify any record
- Forms now have a **file upload section** to add credential images
- CV Preview shows **thumbnail images** next to degrees/certifications
- One-page PDF generation **remains unchanged** (profile photo only)

**Your manually copied images are now fully integrated!** You can edit them, replace them, or remove them through the UI.

---

**Next Steps:**
1. Test editing education records via `/admin/education`
2. Try uploading a new credential image
3. Verify preview in CV (`/profile/1`)
4. Add images to advanced training records if needed
