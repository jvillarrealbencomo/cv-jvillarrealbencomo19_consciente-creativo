Admin Endpoints Summary
# CV 2026 Credential Image Upload Feature (CV 2025+ Credential Image Feature)


**Branch:** `cv2025-credential-images`  
**Date:** January 14, 2026  
**Status:** ✅ Complete and Ready for Testing in Production

**Purpose**: Temporary migration helpers for database management (data import & bulk image uploads).

**Securit**y: All admin endpoints require ADMIN_PASSWORD environment variable to be set on Render. Without it, endpoints return 401 Unauthorized.

**Available Endpoints**:
Endpoint	                        Method	Purpose	                            Destructive?
/admin/import-data?pw=PASSWORD	    GET	    Shows upload form	                No
/admin/import-data	                POST	Clears all tables, imports JSON	    Yes
/admin/upload-images?pw=PASSWORD	GET	    Shows bulk image upload UI	        No
/admin/upload-education-images	    POST	Uploads education credential images	No
/admin/upload-training-images	    POST	Uploads training credential images	No

**How to use**:
Set ADMIN_PASSWORD environment variable on Render (e.g., MySecurePass123)
Visit: https://cv.javiervillarreal.me/admin/import-data?pw=MySecurePass123
Upload cv_data_export.json (for data) or credential images (via forms)

**Data import behavior**:
Deletes all records from: Person, WorkExperience, Education, AdvancedTraining, TechnicalTool, Language, ITProduct
Imports fresh data from JSON file
Database-agnostic (works with PostgreSQL, SQLite, MySQL)

**Security note**: Password appears in URL query string. Acceptable for admin-only use. For higher security, upgrade to Bearer token authentication.

**Security note**: Password ci90...
