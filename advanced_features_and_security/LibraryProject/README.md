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
