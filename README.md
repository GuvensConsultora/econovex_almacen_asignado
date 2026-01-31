# Configuración de usuario: Almacén y Diario de ventas

Módulo para Odoo 19 que filtra automáticamente inventario y facturas de venta según configuración del usuario.

---

## 📋 Tabla de contenidos

- [Problemas que resuelve](#-problemas-que-resuelve)
- [Solución funcional](#-solución-funcional)
- [Solución técnica](#-solución-técnica)
- [Instalación y configuración](#-instalación-y-configuración)
- [Estructura del módulo](#-estructura-del-módulo)

---

## 🎯 Problemas que resuelve

### Problema 1: Filtrado de inventario por almacén

**Contexto funcional:**
Empresas con múltiples almacenes necesitan que cada usuario vea solo las operaciones de su almacén asignado.

**Problema técnico:**
El dominio de `ir.actions.act_window` se evalúa en JavaScript del cliente, donde **no existe el objeto `user`**. Por lo tanto, no se puede usar `[('warehouse_id', '=', user.property_warehouse_id.id)]`.

### Problema 2: Filtrado de facturas por diario

**Contexto funcional:**
Empresas con múltiples diarios de venta (por sucursal, vendedor, tipo de cliente) necesitan que:
- Cada usuario vea **solo las facturas de su diario**
- Solo pueda **crear facturas en su diario**
- Solo pueda **confirmar facturas de su diario**

**Problema técnico:**
Mismo que inventario: el evaluador de dominios en JS no tiene acceso al objeto `user`, y además se necesita validación server-side al confirmar.

---

## ✅ Solución funcional

### 1. Filtro de inventario

Al hacer clic en **Inventario** → se muestra el dashboard filtrado por el almacén del usuario.

- Usuario **con almacén asignado** → Ve solo operaciones de su almacén
- Usuario **sin almacén asignado** → Ve todas las operaciones

### 2. Filtro de facturas de cliente

Al abrir **Facturación > Clientes > Facturas** → se muestran solo las facturas del diario del usuario.

- Usuario **con diario asignado** → Ve solo facturas de su diario
- Usuario **sin diario asignado** → Ve todas las facturas

### 3. Creación automática con diario

Al crear una factura de venta, el campo **Diario** se completa automáticamente con el diario del usuario.

### 4. Validación al confirmar

Si el usuario intenta confirmar una factura de un diario que no es el suyo, **se bloquea con error descriptivo**.

---

## 🔧 Solución técnica

### Patrón: `ir.actions.server` + Override de menú

En lugar de usar dominios estáticos en `ir.actions.act_window`, se usa un **Server Action** que ejecuta código Python:

```xml
<record id="action_invoices_my_journal" model="ir.actions.server">
    <field name="model_id" ref="account.model_account_move"/>
    <field name="state">code</field>
    <field name="code">action = model.action_invoices_my_journal()</field>
</record>

<record id="account.menu_action_move_out_invoice_type" model="ir.ui.menu">
    <field name="action" ref="action_invoices_my_journal"/>
</record>
```

### Flujo de ejecución

```
Usuario hace clic en menú
    ↓
ir.actions.server ejecuta código Python
    ↓
Método Python lee user.sale_journal_id
    ↓
Retorna acción con domain dinámico: [('journal_id', '=', journal_id)]
    ↓
Vista se abre con filtro aplicado
```

### Implementación por módulo

| Funcionalidad | Modelo | Método | Vista XML |
|---------------|--------|--------|-----------|
| Filtro inventario | `stock.picking.type` | `action_inventory_overview_my_wh()` | `stock_picking_type_views.xml` |
| Filtro facturas | `account.move` | `action_invoices_my_journal()` | `account_move_views.xml` |
| Diario por defecto | `account.move` | `default_get()` override | - |
| Validación confirmación | `account.move` | `action_post()` override | - |

### Código clave: Filtrado de facturas

**models/account_move.py:**
```python
@api.model
def action_invoices_my_journal(self):
    """Filtra facturas por diario del usuario"""
    action = self.env["ir.actions.act_window"]._for_xml_id(
        "account.action_move_out_invoice_type"
    )

    user_journal = self.env.user.sale_journal_id

    if user_journal:
        action["domain"] = [("journal_id", "=", user_journal.id)]
        action["context"]["default_journal_id"] = user_journal.id

    return action
```

### Código clave: Validación al confirmar

**models/account_move.py:**
```python
def action_post(self):
    """Valida que solo se confirmen facturas del diario del usuario"""
    user_journal = self.env.user.sale_journal_id

    if user_journal:
        for move in self:
            if move.move_type in ("out_invoice", "out_refund"):
                if move.journal_id != user_journal:
                    raise UserError(
                        "No puede confirmar facturas del diario '%s'.\n"
                        "Su diario asignado es: '%s'"
                        % (move.journal_id.name, user_journal.name)
                    )

    return super().action_post()
```

---

## 📦 Instalación y configuración

### Dependencias

- `sale_stock` (para `property_warehouse_id` en usuarios)
- `account` (para `account.journal`)

### Instalación

```bash
# 1. Copiar módulo a addons
cp -r econovex_almacen_asignado /path/to/odoo/addons/

# 2. Reiniciar Odoo y actualizar módulo
odoo -d DATABASE -u econovex_almacen_asignado --stop-after-init

# 3. Verificar logs
grep "FILTRO DIARIO\|FILTRO ALMACEN" /var/log/odoo/odoo.log
```

### Configuración de usuario

**Ajustes > Usuarios > [Usuario] > Preferencias:**

1. **Almacén por defecto** → Filtra dashboard de inventario
2. **Diario de ventas por defecto** → Filtra facturas de cliente

Si no se asigna ningún valor, el usuario ve todos los registros (sin restricciones).

---

## 📁 Estructura del módulo

```
econovex_almacen_asignado/
├── __init__.py
├── __manifest__.py
├── README.md
├── CLAUDE.md                      # Documentación para Claude Code
├── models/
│   ├── __init__.py
│   ├── account_move.py            # Filtro + validación de facturas
│   ├── res_users.py               # Campo sale_journal_id
│   └── stock_picking_type.py      # Filtro de inventario
└── views/
    ├── account_move_views.xml     # Server action para facturas
    ├── res_users_views.xml        # Campo en vista de usuario
    └── stock_picking_type_views.xml  # Server action para inventario
```

### Campos agregados

| Modelo | Campo | Tipo | Descripción |
|--------|-------|------|-------------|
| `res.users` | `sale_journal_id` | Many2one(account.journal) | Diario de ventas asignado al usuario |

---

## 🐛 Troubleshooting

### El filtro no se aplica

1. Verificar que el usuario tenga asignado un valor en el campo correspondiente
2. Revisar logs de Odoo: `grep "FILTRO DIARIO" /var/log/odoo/odoo.log`
3. Verificar que la acción del menú esté correctamente sobreescrita

### Error al confirmar facturas

Si aparece "No puede confirmar facturas del diario X":
- El usuario está intentando confirmar una factura de un diario que no es el suyo
- Verificar en Preferencias del usuario qué diario tiene asignado
- Solo puede confirmar facturas creadas con su diario

### El campo no aparece en la vista de usuario

```bash
# Actualizar módulo
odoo -d DATABASE -u econovex_almacen_asignado --stop-after-init

# Limpiar caché del navegador
Ctrl + Shift + R
```

---

## 👨‍💻 Autor

**guven C.G.**

## 📄 Licencia

LGPL-3

---

## 🔗 Referencias técnicas

- [Odoo Actions Documentation](https://www.odoo.com/documentation/19.0/developer/reference/backend/actions.html)
- [Server Actions](https://www.odoo.com/documentation/19.0/developer/reference/backend/actions.html#server-actions)
- [Record Rules](https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html#record-rules)
