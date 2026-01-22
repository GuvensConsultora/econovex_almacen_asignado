# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Module Overview

Odoo 19 module that extends user configuration:
1. Filters "Resumen de inventario" by user's assigned warehouse (solves `user` unavailability in JS domain evaluation)
2. Adds `sale_journal_id` field to `res.users` for default sales journal per user

## Module Dependencies

- `sale_stock` - Required for `property_warehouse_id` field on users
- `account` - Required for `account.journal` model access

## Architecture

### Warehouse Filtering Problem & Solution

Odoo's `ir.actions.act_window` domains are evaluated in JavaScript where `user` context is unavailable. Solution: Use `ir.actions.server` that executes Python code server-side, then return the modified action.

**Flow:**
```
Menu Click → ir.actions.server → StockPickingType.action_inventory_overview_my_wh() → Returns filtered action
```

### Key Files

| File | Purpose |
|------|---------|
| `models/res_users.py` | Adds `sale_journal_id` Many2one field to res.users |
| `models/stock_picking_type.py` | `action_inventory_overview_my_wh()` method - applies warehouse filter dynamically |
| `views/res_users_views.xml` | Inherits user form to show `sale_journal_id` field |
| `views/stock_picking_type_views.xml` | Server action definition + menu override |

## Development Commands

```bash
# Restart Odoo with module update
odoo -d DATABASE -u econovex_almacen_asignado --stop-after-init

# Full upgrade (when changing __manifest__.py)
odoo -d DATABASE -i econovex_almacen_asignado --stop-after-init

# Check logs for warehouse filtering debug
grep "filtrar inventario" /path/to/odoo.log
```

## Common Issues

### XPath targeting `property_warehouse_id` fails
The `property_warehouse_id` field is NOT in `base.view_users_form`. It's added by `sale_stock` module in its own inherited view (`sale_stock.res_users_view_form`). Solution: Inherit from `sale_stock.res_users_view_form` instead, or use a different xpath target.

### Field not appearing after module update
1. Check Odoo logs for view parsing errors
2. Verify the xpath target exists in the parent view
3. Try upgrading the module: `odoo -d DB -u econovex_almacen_asignado`
4. Clear browser cache and reload

## Testing

Test manually:
1. Assign a warehouse to user in Settings > Users > [User] > Preferences
2. Open Inventory module - should show filtered operations
3. Check logs for `DEBUG: Intentando filtrar inventario...` messages
