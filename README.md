# Configuración de usuario: Almacén y Diario de ventas

Módulo para Odoo 19 que extiende la configuración del usuario con filtros y campos por defecto.

## Funcionalidades

### 1. Filtro automático de inventario por almacén

Al hacer clic en el icono de **Inventario** en la pantalla de inicio de Odoo, se abre el dashboard de operaciones (vista kanban de `stock.picking.type`) filtrado automáticamente por el almacén asignado al usuario.

### 2. Diario de ventas por defecto

Agrega el campo **"Diario de ventas por defecto"** en el formulario del usuario, permitiendo asignar un diario de ventas específico a cada usuario.

## Problema que resuelve

### Filtro de inventario

En Odoo, el dominio de una acción (`ir.actions.act_window`) se evalúa en el cliente JavaScript, donde **no existe el objeto `user`**. Este módulo implementa una **acción de servidor** que genera el filtro dinámicamente desde Python.

### Diario de ventas

Permite centralizar la configuración del diario de ventas por usuario, útil para escenarios donde diferentes vendedores o equipos usan diarios distintos.

## Estructura

```
econovex_almacen_asignado/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── res_users.py
│   └── stock_picking_type.py
└── views/
    ├── res_users_views.xml
    └── stock_picking_type_views.xml
```

## Campos agregados

| Modelo | Campo | Tipo | Descripción |
|--------|-------|------|-------------|
| `res.users` | `property_sale_journal_id` | Many2one | Diario de ventas por defecto (company_dependent) |

## Dependencias

- `stock` (módulo de Inventario)
- `account` (módulo de Contabilidad)

## Instalación

1. Copiar el módulo en el directorio de addons
2. Actualizar la lista de aplicaciones
3. Instalar "Configuración de usuario: Almacén y Diario de ventas"

## Configuración

En **Ajustes > Usuarios > [Usuario] > Preferencias**:

- **Almacén por defecto**: Filtra el dashboard de inventario
- **Diario de ventas por defecto**: Diario que se usará en operaciones de venta

Si el usuario no tiene almacén asignado, el dashboard mostrará todas las operaciones sin filtrar.

## Autor

guven C.G.

## Licencia

LGPL-3
