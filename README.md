# Inventory Overview: My Default Warehouse

Módulo para Odoo 19 que filtra automáticamente el **Resumen de inventario** por el almacén por defecto del usuario.

## Descripción

Al hacer clic en el icono de **Inventario** en la pantalla de inicio de Odoo, se abre el dashboard de operaciones (vista kanban de `stock.picking.type`) filtrado automáticamente por el almacén asignado al usuario (`res.users.property_warehouse_id`).

## Problema que resuelve

En Odoo, el dominio de una acción (`ir.actions.act_window`) se evalúa en el cliente JavaScript, donde **no existe el objeto `user`**. Por lo tanto, un dominio como:

```python
[('warehouse_id', '=', user.property_warehouse_id.id)]
```

**no funciona** directamente en una acción de ventana.

## Solución

Este módulo implementa una **acción de servidor** (`ir.actions.server`) que:

1. Lee la acción estándar de inventario (`stock.stock_picking_type_action`)
2. Obtiene el almacén por defecto del usuario desde `env.user.property_warehouse_id`
3. Aplica dinámicamente el filtro `[('warehouse_id', '=', wh.id)]`
4. Sobreescribe el menú raíz de Inventario para usar esta acción

## Estructura

```
econovex_almacen_asignado/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── stock_picking_type.py
└── views/
    └── stock_picking_type_views.xml
```

## Dependencias

- `stock` (módulo de Inventario estándar de Odoo)

## Instalación

1. Copiar el módulo en el directorio de addons
2. Actualizar la lista de aplicaciones
3. Instalar "Inventory Overview: My Default Warehouse"

## Configuración

Asegurate de que cada usuario tenga configurado su **almacén por defecto** en:

`Ajustes > Usuarios > [Usuario] > Preferencias > Almacén por defecto`

Si el usuario no tiene almacén asignado, el dashboard mostrará todas las operaciones sin filtrar.

## Autor

guven C.G.

## Licencia

LGPL-3
