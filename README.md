# Inventory Overview: My Default Warehouse (Odoo 17)

Este módulo agrega un menú **“Resumen de inventario (mi almacén)”** que abre el dashboard estándar de Inventario (modelo `stock.picking.type`, vista kanban), pero **filtrado por el almacén por defecto del usuario**.

## Problema que resuelve
En Odoo, el “Valor del dominio” de una acción (`ir.actions.act_window`) se evalúa del lado del cliente y **no existe `user`** en ese evaluador, por lo que un dominio tipo:

```python
[('warehouse_id', '=', user.property_warehouse_id.id)]
