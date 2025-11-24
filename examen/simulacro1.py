"""
Gestión de inventario y ventas (sin POO).
Todas las operaciones (excepto el menú) son funciones.
Estructuras: dicts anidados y listas.
"""

from datetime import datetime
from collections import defaultdict, Counter
import sys

# ---------- FUNCIONES DE VALIDACIÓN ----------

def leer_entero(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt).strip())
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Valor fuera de rango. Debe ser entre {min_val} y {max_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")

def leer_flotante(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).strip())
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Valor fuera de rango. Debe ser entre {min_val} y {max_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Ingresa un número (ej. 12.5)")

def leer_texto_no_vacio(prompt):
    while True:
        txt = input(prompt).strip()
        if txt == "":
            print("No puede estar vacío.")
            continue
        return txt

def confirmar(prompt="¿Confirmar? (s/n): "):
    r = input(prompt).strip().lower()
    return r in ("s", "si", "y", "yes")

# ---------- GESTIÓN DEL INVENTARIO ----------

def generar_id_producto(productos):
    """Genera un id único incremental para productos."""
    if not productos:
        return 1
    return max(productos.keys()) + 1

def registrar_producto(productos):
    """
    Agrega un producto al diccionario productos.
    productos: dict: id -> {nombre, marca, categoria, precio, cantidad, garantia}
    Devuelve productos actualizado.
    """
    print("\n--- Registrar producto ---")
    nombre = leer_texto_no_vacio("Nombre del producto: ")
    # validar unicidad por nombre y marca
    marca = leer_texto_no_vacio("Marca: ")
    categoria = leer_texto_no_vacio("Categoría: ")
    precio = leer_flotante("Precio unitario: ", min_val=0.0)
    cantidad = leer_entero("Cantidad en stock: ", min_val=0)
    garantia = leer_entero("Garantía (meses): ", min_val=0)

    # verificar no duplicado exacto (nombre+marca)
    for pid, p in productos.items():
        if p['nombre'].lower() == nombre.lower() and p['marca'].lower() == marca.lower():
            print("Error: ya existe un producto con ese nombre y marca.")
            return productos

    pid = generar_id_producto(productos)
    productos[pid] = {
        "nombre": nombre,
        "marca": marca,
        "categoria": categoria,
        "precio": precio,
        "cantidad": cantidad,
        "garantia_meses": garantia
    }
    print(f"Producto registrado con ID {pid}.")
    return productos

def consultar_producto(productos, por_id=True):
    """
    Consulta productos. Si por_id True pide id, sino busca por nombre.
    Devuelve None.
    """
    print("\n--- Consultar producto ---")
    if not productos:
        print("No hay productos registrados.")
        return
    if por_id:
        pid = leer_entero("ID del producto: ", min_val=1)
        p = productos.get(pid)
        if p:
            imprimir_producto(pid, p)
        else:
            print("Producto no encontrado.")
    else:
        nombre = leer_texto_no_vacio("Nombre (busca parcial): ").lower()
        encontrados = [(pid, p) for pid,p in productos.items() if nombre in p['nombre'].lower()]
        if not encontrados:
            print("No se encontraron coincidencias.")
            return
        for pid, p in encontrados:
            imprimir_producto(pid, p)

def imprimir_producto(pid, p):
    print(f"\nID: {pid}")
    print(f"  Nombre: {p['nombre']}")
    print(f"  Marca: {p['marca']}")
    print(f"  Categoría: {p['categoria']}")
    print(f"  Precio unitario: {p['precio']}")
    print(f"  Cantidad en stock: {p['cantidad']}")
    print(f"  Garantía (meses): {p['garantia_meses']}")

def actualizar_producto(productos):
    """
    Actualiza datos de un producto.
    Devuelve productos actualizado.
    """
    print("\n--- Actualizar producto ---")
    if not productos:
        print("No hay productos.")
        return productos
    pid = leer_entero("ID del producto a actualizar: ", min_val=1)
    if pid not in productos:
        print("ID no encontrado.")
        return productos
    p = productos[pid]
    imprimir_producto(pid, p)
    print("Dejar vacío para mantener valor actual.")
    nombre = input("Nuevo nombre: ").strip()
    marca = input("Nueva marca: ").strip()
    categoria = input("Nueva categoría: ").strip()
    precio_raw = input("Nuevo precio unitario: ").strip()
    cantidad_raw = input("Nueva cantidad en stock: ").strip()
    garantia_raw = input("Nueva garantía (meses): ").strip()

    if nombre:
        p['nombre'] = nombre
    if marca:
        p['marca'] = marca
    if categoria:
        p['categoria'] = categoria
    if precio_raw:
        try:
            precio = float(precio_raw)
            if precio < 0: raise ValueError
            p['precio'] = precio
        except ValueError:
            print("Precio inválido. No se actualizó el precio.")
    if cantidad_raw:
        try:
            cantidad = int(cantidad_raw)
            if cantidad < 0: raise ValueError
            p['cantidad'] = cantidad
        except ValueError:
            print("Cantidad inválida. No se actualizó la cantidad.")
    if garantia_raw:
        try:
            garantia = int(garantia_raw)
            if garantia < 0: raise ValueError
            p['garantia_meses'] = garantia
        except ValueError:
            print("Garantía inválida. No se actualizó la garantía.")
    productos[pid] = p
    print("Producto actualizado.")
    return productos

def eliminar_producto(productos, ventas):
    """
    Elimina producto si no hay ventas relacionadas o si el usuario confirma.
    Devuelve productos actualizado.
    """
    print("\n--- Eliminar producto ---")
    if not productos:
        print("No hay productos.")
        return productos
    pid = leer_entero("ID del producto a eliminar: ", min_val=1)
    if pid not in productos:
        print("ID no encontrado.")
        return productos
    # comprobar ventas relacionadas
    ventas_rel = [v for v in ventas if v['producto_id'] == pid]
    imprimir_producto(pid, productos[pid])
    if ventas_rel:
        print(f"Hay {len(ventas_rel)} ventas relacionadas con este producto.")
        if not confirmar("¿Eliminar de todas formas? Esto no eliminará las ventas automáticamente. (s/n): "):
            print("Operación cancelada.")
            return productos
    if confirmar("Confirmar eliminación (s/n): "):
        del productos[pid]
        print("Producto eliminado.")
    else:
        print("Operación cancelada.")
    return productos

def listar_productos(productos):
    print("\n--- Listado de productos ---")
    if not productos:
        print("No hay productos.")
        return
    for pid, p in productos.items():
        print(f"{pid}: {p['nombre']} | Marca: {p['marca']} | Cat: {p['categoria']} | Precio: {p['precio']} | Stock: {p['cantidad']}")

# ---------- VENTAS ----------

def registrar_venta(productos, ventas):
    """
    Registra una venta verificando stock y actualizando inventario.
    ventas: lista de dicts: {id_venta, cliente, tipo_cliente, producto_id, cantidad, fecha, descuento_pct, precio_unitario, ingreso_bruto, ingreso_neto}
    Devuelve (productos, ventas) actualizados.
    """
    print("\n--- Registrar venta ---")
    if not productos:
        print("No hay productos disponibles para vender.")
        return productos, ventas

    cliente = leer_texto_no_vacio("Nombre del cliente: ")
    tipo_cliente = leer_texto_no_vacio("Tipo de cliente (ej. regular, mayorista, nuevo): ")
    listar_productos(productos)
    pid = leer_entero("ID del producto a vender: ", min_val=1)
    if pid not in productos:
        print("Producto no encontrado.")
        return productos, ventas
    prod = productos[pid]
    print(f"Producto seleccionado: {prod['nombre']} (stock: {prod['cantidad']})")
    cantidad = leer_entero("Cantidad a vender: ", min_val=1)
    if cantidad > prod['cantidad']:
        print("Stock insuficiente. Venta cancelada.")
        return productos, ventas
    descuento_pct = leer_flotante("Descuento aplicado (%) [0 si ninguno]: ", min_val=0.0, max_val=100.0)
    fecha_str = input("Fecha de venta (YYYY-MM-DD) [enter = hoy]: ").strip()
    if fecha_str == "":
        fecha = datetime.now().date()
    else:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            print("Fecha inválida. Se usará fecha de hoy.")
            fecha = datetime.now().date()

    # calcular ingresos: bruto = precio * cantidad; neto = bruto * (1 - descuento/100)
    precio_unit = prod['precio']
    bruto_calc = lambda pu, q: pu * q
    neto_calc = lambda bruto, d: bruto * (1 - d/100.0)

    ingreso_bruto = bruto_calc(precio_unit, cantidad)
    ingreso_neto = neto_calc(ingreso_bruto, descuento_pct)

    venta_id = len(ventas) + 1
    venta = {
        "venta_id": venta_id,
        "cliente": cliente,
        "tipo_cliente": tipo_cliente,
        "producto_id": pid,
        "producto_nombre": prod['nombre'],
        "marca": prod['marca'],
        "cantidad": cantidad,
        "fecha": fecha.isoformat(),
        "descuento_pct": descuento_pct,
        "precio_unitario": precio_unit,
        "ingreso_bruto": ingreso_bruto,
        "ingreso_neto": ingreso_neto
    }
    ventas.append(venta)
    # actualizar inventario
    productos[pid]['cantidad'] -= cantidad
    print(f"Venta registrada (ID {venta_id}). Ingreso neto: {ingreso_neto:.2f}")
    return productos, ventas

def consultar_ventas(ventas, por_fecha=False):
    print("\n--- Historial de ventas ---")
    if not ventas:
        print("No hay ventas registradas.")
        return
    if por_fecha:
        fecha_str = leer_texto_no_vacio("Fecha (YYYY-MM-DD) a consultar: ")
        try:
            fecha_q = datetime.strptime(fecha_str, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Fecha inválida.")
            return
        filtradas = [v for v in ventas if v['fecha'] == fecha_q]
    else:
        filtradas = ventas
    if not filtradas:
        print("No hay ventas en ese criterio.")
        return
    for v in filtradas:
        print(f"ID VENTA {v['venta_id']}: {v['fecha']} | {v['producto_nombre']} x{v['cantidad']} | Cliente: {v['cliente']} | Bruto: {v['ingreso_bruto']:.2f} | Neto: {v['ingreso_neto']:.2f}")

# ---------- REPORTES ----------

def top_3_productos_mas_vendidos(ventas):
    """
    Retorna lista de tuplas (producto_nombre, cantidad_vendida) ordenadas desc, top 3.
    """
    contador = Counter()
    for v in ventas:
        contador[v['producto_nombre']] += v['cantidad']
    top3 = contador.most_common(3)
    return top3

def ventas_agrupadas_por_marca(ventas):
    """
    Retorna dict marca -> {'unidades': x, 'ingreso_neto': y, 'ingreso_bruto': z}
    """
    resumen = defaultdict(lambda: {"unidades":0, "ingreso_bruto":0.0, "ingreso_neto":0.0})
    for v in ventas:
        m = v.get('marca', 'SinMarca')
        resumen[m]['unidades'] += v['cantidad']
        resumen[m]['ingreso_bruto'] += v['ingreso_bruto']
        resumen[m]['ingreso_neto'] += v['ingreso_neto']
    return dict(resumen)

def calculo_ingresos(ventas):
    """
    Calcula ingreso bruto total y neto total.
    Aquí usamos una lambda para sumar ingreso_neto de cada venta (ejemplo de cálculo agregado).
    Devuelve (bruto_total, neto_total)
    """
    bruto_total = sum(map(lambda v: v['ingreso_bruto'], ventas))
    neto_total = sum(map(lambda v: v['ingreso_neto'], ventas))
    return bruto_total, neto_total

def reporte_rendimiento_inventario(productos, ventas, umbral_bajo=5):
    """
    Reporte que identifica:
    - productos con stock bajo (cantidad <= umbral_bajo)
    - productos sin movimiento (nunca vendidos)
    - rotación: cantidad vendida / stock_inicial_estimada (no tenemos histórico de stock inicial,
      así que mostramos ventas totales vs stock actual)
    Devuelve dict con secciones.
    """
    ventas_por_producto = Counter()
    for v in ventas:
        ventas_por_producto[v['producto_id']] += v['cantidad']
    low_stock = []
    sin_mov = []
    rotacion = {}
    for pid, p in productos.items():
        sold = ventas_por_producto.get(pid, 0)
        if p['cantidad'] <= umbral_bajo:
            low_stock.append((pid, p['nombre'], p['cantidad']))
        if sold == 0:
            sin_mov.append((pid, p['nombre']))
        # rotación aproximada: vendidas / (vendidas + stock actual) -> proporción de lo que salió vs total disponible ahora+vendido
        denom = sold + p['cantidad']
        rot = (sold / denom) if denom > 0 else 0.0
        rotacion[pid] = {"nombre": p['nombre'], "rotacion": rot, "vendido": sold, "stock_actual": p['cantidad']}
    return {
        "low_stock": low_stock,
        "sin_movimiento": sin_mov,
        "rotacion": rotacion
    }

def imprimir_reporte(productos, ventas):
    print("\n=== REPORTE GENERAL ===")
    top3 = top_3_productos_mas_vendidos(ventas)
    print("\nTop 3 productos más vendidos:")
    if top3:
        for i,(nombre,cant) in enumerate(top3, start=1):
            print(f"  {i}. {nombre} -> {cant} unidades")
    else:
        print("  No hay ventas registradas.")

    print("\nVentas agrupadas por marca:")
    por_marca = ventas_agrupadas_por_marca(ventas)
    if por_marca:
        for marca, datos in por_marca.items():
            print(f"  Marca: {marca} | Unidades: {datos['unidades']} | Bruto: {datos['ingreso_bruto']:.2f} | Neto: {datos['ingreso_neto']:.2f}")
    else:
        print("  No hay ventas registradas.")

    bruto, neto = calculo_ingresos(ventas)
    print(f"\nIngresos totales: Bruto = {bruto:.2f} | Neto = {neto:.2f}")

    print("\nRendimiento del inventario:")
    rend = reporte_rendimiento_inventario(productos, ventas)
    print("  Productos con stock bajo:")
    if rend['low_stock']:
        for pid, nombre, stock in rend['low_stock']:
            print(f"    ID {pid}: {nombre} (stock: {stock})")
    else:
        print("    Ninguno")
    print("  Productos sin movimiento:")
    if rend['sin_movimiento']:
        for pid, nombre in rend['sin_movimiento']:
            print(f"    ID {pid}: {nombre}")
    else:
        print("    Ninguno")
    print("  Rotación (0..1) de productos (muestra hasta 5):")
    for pid, info in list(rend['rotacion'].items())[:5]:
        print(f"    ID {pid}: {info['nombre']} | rotación: {info['rotacion']:.2f} | vendidos: {info['vendido']} | stock_actual: {info['stock_actual']}")

# ---------- UTILIDADES ----------

def inicializar_demo(productos, ventas):
    """Agrega algunos datos demo para probar (opcional)."""
    if productos:
        return productos, ventas
    productos[1] = {"nombre":"Cargador USB", "marca":"BrandA", "categoria":"Accesorios", "precio":15.0, "cantidad":20, "garantia_meses":12}
    productos[2] = {"nombre":"Auriculares", "marca":"BrandB", "categoria":"Audio", "precio":45.0, "cantidad":10, "garantia_meses":6}
    productos[3] = {"nombre":"Teclado", "marca":"BrandA", "categoria":"Periféricos", "precio":30.0, "cantidad":5, "garantia_meses":24}
    # ventas vacías
    return productos, ventas

# ---------- MENÚ PRINCIPAL (fuera de funciones) ----------

def menu():
    productos = {}  # id -> producto dict
    ventas = []     # lista de ventas
    # opcional: inicializar demo
    if confirmar("¿Cargar datos demo de ejemplo? (s/n): "):
        productos, ventas = inicializar_demo(productos, ventas)

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrar producto")
        print("2. Consultar producto (por ID)")
        print("3. Buscar producto (por nombre)")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Listar productos")
        print("7. Registrar venta")
        print("8. Consultar historial de ventas")
        print("9. Consultar ventas por fecha")
        print("10. Reporte general")
        print("0. Salir")
        opc = input("Elige una opción: ").strip()
        if opc == "1":
            productos = registrar_producto(productos)
        elif opc == "2":
            consultar_producto(productos, por_id=True)
        elif opc == "3":
            consultar_producto(productos, por_id=False)
        elif opc == "4":
            productos = actualizar_producto(productos)
        elif opc == "5":
            productos = eliminar_producto(productos, ventas)
        elif opc == "6":
            listar_productos(productos)
        elif opc == "7":
            productos, ventas = registrar_venta(productos, ventas)
        elif opc == "8":
            consultar_ventas(ventas, por_fecha=False)
        elif opc == "9":
            consultar_ventas(ventas, por_fecha=True)
        elif opc == "10":
            imprimir_reporte(productos, ventas)
        elif opc == "0":
            print("Saliendo... ¡hasta pronto!")
            sys.exit(0)
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
