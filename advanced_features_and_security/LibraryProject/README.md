# Permissions and Groups Setup

## Models
The `Book` model includes custom permissions:
- `can_view`: Allows viewing books.
- `can_create`: Allows creating new book entries.
- `can_edit`: Allows editing existing book entries.
- `can_delete`: Allows deleting book entries.

## Groups
The following groups are configured:
- **Editors**: Can create and edit books.
- **Viewers**: Can only view books.
- **Admins**: Can view, create, edit, and delete books.

## Views
Permissions are enforced in the views using the `@permission_required` decorator.
- `view_books`: Requires `can_view` permission.
- `create_book`: Requires `can_create` permission.
- `edit_book`: Requires `can_edit` permission.
- `delete_book`: Requires `can_delete` permission.

# Security Measures Documentation

## Settings
- **DEBUG**: Set to `False` to prevent detailed error pages in production.
- **SECURE_BROWSER_XSS_FILTER**: Enables the browser's XSS filter.
- **X_FRAME_OPTIONS**: Set to `DENY` to prevent the site from being embedded in frames.
- **SECURE_CONTENT_TYPE_NOSNIFF**: Prevents browsers from interpreting files as a different MIME type.
- **CSRF_COOKIE_SECURE & SESSION_COOKIE_SECURE**: Ensure cookies are only sent over HTTPS.

## CSRF Tokens
Ensure all forms include `{% csrf_token %}` to prevent CSRF attacks.

## CSP
Configured CSP headers to mitigate XSS risks by specifying allowed sources for content.

