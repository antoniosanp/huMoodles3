# INSTRUCCIONES
# Guarda cada bloque en un archivo con el nombre indicado en el encabezado (por ejemplo: main.py, usuarios.py, equipos.py, prestamos.py, reportes.py)
# Ejecuta: python main.py

# ---------------------- usuarios.py ----------------------
import csv
import os
import getpass

USUARIOS_CSV = 'usuarios.csv'

def asegurar_usuarios():
    """Crear archivo usuarios.csv si no existe y añadir un admin por defecto (usuario: admin, contrasena: admin123)."""
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['usuario','contrasena','rol'])
            writer.writerow(['admin','admin123','ADMIN'])

def cargar_usuarios():
    usuarios = []
    if not os.path.exists(USUARIOS_CSV):
        return usuarios
    with open(USUARIOS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            usuarios.append(row)
    return usuarios

def validar_login():
    """Pide credenciales hasta 3 intentos. Devuelve usuario (dict) si OK, None si falla."""
    asegurar_usuarios()
    usuarios = cargar_usuarios()
    intentos = 0
    while intentos < 3:
        usuario = input('Usuario: ').strip()
        contr = getpass.getpass('Contrasena: ').strip()
        for u in usuarios:
            if u['usuario'] == usuario and u['contrasena'] == contr and u['rol'].upper() == 'ADMIN':
                print('Inicio de sesion exitoso.\n')
                return u
        intentos += 1
        print(f'Credenciales incorrectas. Intentos restantes: {3-intentos}')
    print('Se agotaron los intentos. Saliendo...')
    return None

# ---------------------- equipos.py ----------------------
import csv
import os
from datetime import datetime

EQUIPOS_CSV = 'equipos.csv'

def asegurar_equipos():
    if not os.path.exists(EQUIPOS_CSV):
        with open(EQUIPOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['equipo_id','nombre_equipo','categoria','estado_actual','fecha_registro'])

def cargar_equipos():
    asegurar_equipos()
    equipos = []
    with open(EQUIPOS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            equipos.append(row)
    return equipos

def guardar_equipos(equipos):
    with open(EQUIPOS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['equipo_id','nombre_equipo','categoria','estado_actual','fecha_registro'])
        for e in equipos:
            writer.writerow([e['equipo_id'], e['nombre_equipo'], e['categoria'], e['estado_actual'], e['fecha_registro']])

def generar_id_equipos():
    equipos = cargar_equipos()
    if not equipos:
        return '1'
    ids = [int(e['equipo_id']) for e in equipos]
    return str(max(ids)+1)

def registrar_equipo():
    equipos = cargar_equipos()
    equipo_id = generar_id_equipos()
    nombre = input('Nombre del equipo: ').strip()
    categoria = input('Categoria: ').strip()
    fecha = datetime.now().strftime('%Y-%m-%d')
    estado = 'DISPONIBLE'
    equipos.append({'equipo_id': equipo_id, 'nombre_equipo': nombre, 'categoria': categoria, 'estado_actual': estado, 'fecha_registro': fecha})
    guardar_equipos(equipos)
    print(f'Equipo registrado con ID {equipo_id}.')

def listar_equipos(mostrar_todos=True):
    equipos = cargar_equipos()
    if not equipos:
        print('No hay equipos registrados.')
        return
    print('\nLista de equipos:')
    for e in equipos:
        if mostrar_todos or e['estado_actual'] == 'DISPONIBLE':
            print(f"ID: {e['equipo_id']} | {e['nombre_equipo']} | {e['categoria']} | {e['estado_actual']} | {e['fecha_registro']}")
    print()

def consultar_equipo_por_id(equipo_id):
    equipos = cargar_equipos()
    for e in equipos:
        if e['equipo_id'] == str(equipo_id):
            return e
    return None

def actualizar_estado_equipo(equipo_id, nuevo_estado):
    equipos = cargar_equipos()
    cambiado = False
    for e in equipos:
        if e['equipo_id'] == str(equipo_id):
            e['estado_actual'] = nuevo_estado
            cambiado = True
            break
    if cambiado:
        guardar_equipos(equipos)
    return cambiado

# ---------------------- prestamos.py ----------------------
import csv
import os
from datetime import datetime, timedelta

PRESTAMOS_CSV = 'prestamos.csv'

# Los tiempos maximos por tipo de usuario (dias)
TIEMPOS = {
    'ESTUDIANTE': 3,
    'INSTRUCTOR': 7,
    'ADMINISTRATIVO': 10
}

def asegurar_prestamos():
    if not os.path.exists(PRESTAMOS_CSV):
        with open(PRESTAMOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','fecha_solicitud','fecha_inicio','fecha_fin_esperada','fecha_devolucion','dias','retraso','estado','mes','anio'])

def cargar_prestamos():
    asegurar_prestamos()
    prestamos = []
    with open(PRESTAMOS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prestamos.append(row)
    return prestamos

def guardar_prestamos(prestamos):
    with open(PRESTAMOS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','fecha_solicitud','fecha_inicio','fecha_fin_esperada','fecha_devolucion','dias','retraso','estado','mes','anio'])
        for p in prestamos:
            writer.writerow([p.get('prestamo_id',''), p.get('equipo_id',''), p.get('nombre_equipo',''), p.get('usuario_prestatario',''), p.get('tipo_usuario',''), p.get('fecha_solicitud',''), p.get('fecha_inicio',''), p.get('fecha_fin_esperada',''), p.get('fecha_devolucion',''), p.get('dias',''), p.get('retraso',''), p.get('estado',''), p.get('mes',''), p.get('anio','')])

def generar_id_prestamo():
    prestamos = cargar_prestamos()
    if not prestamos:
        return '1'
    ids = [int(p['prestamo_id']) for p in prestamos if p['prestamo_id']]
    return str(max(ids)+1)

def solicitar_prestamo():
    from equipos import consultar_equipo_por_id, actualizar_estado_equipo
    equipos = consultar_equipo_por_id
    equipo_id = input('ID del equipo a solicitar: ').strip()
    equipo = consultar_equipo_por_id(equipo_id)
    if not equipo:
        print('Equipo no encontrado.')
        return
    if equipo['estado_actual'] != 'DISPONIBLE':
        print('El equipo no está disponible para prestamo.')
        return
    nombre_prestatario = input('Nombre del prestatario: ').strip()
    tipo = input('Tipo de usuario (Estudiante/Instructor/Administrativo): ').strip().upper()
    if tipo not in TIEMPOS:
        print('Tipo de usuario invalido.')
        return
    prestamo_id = generar_id_prestamo()
    fecha_solicitud = datetime.now().strftime('%Y-%m-%d')
    dias_permitidos = TIEMPOS[tipo]
    fecha_inicio = ''  # quedará vacía hasta aprobación
    fecha_fin_esperada = ''
    estado = 'PENDIENTE'
    mes = datetime.now().month
    anio = datetime.now().year
    prestamos = cargar_prestamos()
    prestamos.append({'prestamo_id': prestamo_id,
                      'equipo_id': equipo_id,
                      'nombre_equipo': equipo['nombre_equipo'],
                      'usuario_prestatario': nombre_prestatario,
                      'tipo_usuario': tipo,
                      'fecha_solicitud': fecha_solicitud,
                      'fecha_inicio': fecha_inicio,
                      'fecha_fin_esperada': fecha_fin_esperada,
                      'fecha_devolucion': '',
                      'dias': '',
                      'retraso': '',
                      'estado': estado,
                      'mes': str(mes),
                      'anio': str(anio)})
    guardar_prestamos(prestamos)
    print(f'Solicitud registrada con ID {prestamo_id} y estado PENDIENTE.')

def listar_prestamos(filtro_estado=None):
    prestamos = cargar_prestamos()
    if not prestamos:
        print('No hay prestamos registrados.')
        return
    for p in prestamos:
        if filtro_estado and p['estado'] != filtro_estado:
            continue
        print(f"ID:{p['prestamo_id']} | Equipo:{p['nombre_equipo']}({p['equipo_id']}) | Usuario:{p['usuario_prestatario']} | Tipo:{p['tipo_usuario']} | Estado:{p['estado']} | Solicitud:{p['fecha_solicitud']}")

def aprobar_rechazar():
    from equipos import actualizar_estado_equipo
    prestamos = cargar_prestamos()
    pend = [p for p in prestamos if p['estado']=='PENDIENTE']
    if not pend:
        print('No hay solicitudes pendientes.')
        return
    print('Solicitudes pendientes:')
    for p in pend:
        print(f"ID:{p['prestamo_id']} - Equipo:{p['nombre_equipo']} - Usuario:{p['usuario_prestatario']} - Tipo:{p['tipo_usuario']}")
    sel = input('ID de la solicitud a procesar: ').strip()
    encuentro = None
    for p in prestamos:
        if p['prestamo_id'] == sel and p['estado']=='PENDIENTE':
            encuentro = p
            break
    if not encuentro:
        print('Solicitud no encontrada.')
        return
    accion = input('Aprobar (A) / Rechazar (R): ').strip().upper()
    if accion == 'A':
        # setear fechas y estado
        inicio = datetime.now()
        dias = TIEMPOS.get(encuentro['tipo_usuario'], 0)
        fin_esperado = inicio + timedelta(days=dias)
        encuentro['fecha_inicio'] = inicio.strftime('%Y-%m-%d')
        encuentro['fecha_fin_esperada'] = fin_esperado.strftime('%Y-%m-%d')
        encuentro['estado'] = 'ACTIVO'
        # cambiar estado equipo a PRESTADO
        actualizado = actualizar_estado_equipo(encuentro['equipo_id'], 'PRESTADO')
        if not actualizado:
            print('Error actualizando estado del equipo.')
        guardar_prestamos(prestamos)
        print('Solicitud aprobada y equipo marcado como PRESTADO.')
    elif accion == 'R':
        encuentro['estado'] = 'RECHAZADO'
        guardar_prestamos(prestamos)
        print('Solicitud rechazada.')
    else:
        print('Accion invalida.')

def registrar_devolucion():
    from equipos import actualizar_estado_equipo
    prestamos = cargar_prestamos()
    activos = [p for p in prestamos if p['estado']=='ACTIVO']
    if not activos:
        print('No hay prestamos activos.')
        return
    print('Prestamos activos:')
    for p in activos:
        print(f"ID:{p['prestamo_id']} | Equipo:{p['nombre_equipo']} | Usuario:{p['usuario_prestatario']} | Inicio:{p['fecha_inicio']} | Fin esperado:{p['fecha_fin_esperada']}")
    sel = input('ID del prestamo a devolver: ').strip()
    encontrado = None
    for p in prestamos:
        if p['prestamo_id'] == sel and p['estado']=='ACTIVO':
            encontrado = p
            break
    if not encontrado:
        print('Prestamo no encontrado.')
        return
    fecha_dev = datetime.now()
    fecha_inicio = datetime.strptime(encontrado['fecha_inicio'], '%Y-%m-%d') if encontrado['fecha_inicio'] else datetime.strptime(encontrado['fecha_solicitud'],'%Y-%m-%d')
    dias_usados = (fecha_dev - fecha_inicio).days
    # calcular retraso
    fecha_fin_esperada = datetime.strptime(encontrado['fecha_fin_esperada'], '%Y-%m-%d') if encontrado['fecha_fin_esperada'] else fecha_inicio
    retraso = (fecha_dev - fecha_fin_esperada).days
    if retraso < 0:
        retraso = 0
    # actualizar registro
    encontrado['fecha_devolucion'] = fecha_dev.strftime('%Y-%m-%d')
    encontrado['dias'] = str(dias_usados)
    encontrado['retraso'] = str(retraso)
    encontrado['estado'] = 'DEVUELTO'
    # actualizar equipo a DISPONIBLE
    actualizado = actualizar_estado_equipo(encontrado['equipo_id'], 'DISPONIBLE')
    if not actualizado:
        print('Advertencia: no se pudo actualizar estado del equipo.')
    guardar_prestamos(prestamos)
    print(f'Devolucion registrada. Dias usados: {dias_usados}. Retraso: {retraso} dias.')

def historial_por_usuario():
    prestamos = cargar_prestamos()
    nombre = input('Nombre del usuario: ').strip()
    encontrados = [p for p in prestamos if p['usuario_prestatario'].lower() == nombre.lower()]
    if not encontrados:
        print('No se encontraron prestamos para ese usuario.')
        return
    for p in encontrados:
        print(f"ID:{p['prestamo_id']} | Equipo:{p['nombre_equipo']} | Estado:{p['estado']} | Solicitud:{p['fecha_solicitud']} | Inicio:{p['fecha_inicio']} | Devolucion:{p['fecha_devolucion']} | Retraso:{p['retraso']}")

def historial_por_equipo():
    prestamos = cargar_prestamos()
    equipo_id = input('ID del equipo: ').strip()
    encontrados = [p for p in prestamos if p['equipo_id']==equipo_id]
    if not encontrados:
        print('No se encontraron prestamos para ese equipo.')
        return
    for p in encontrados:
        print(f"ID:{p['prestamo_id']} | Usuario:{p['usuario_prestatario']} | Estado:{p['estado']} | Inicio:{p['fecha_inicio']} | Devolucion:{p['fecha_devolucion']} | Retraso:{p['retraso']}")

# ---------------------- reportes.py ----------------------
import csv
from datetime import datetime
from prestamos import cargar_prestamos

REPORTES_DIR = 'reportes'
import os

def asegurar_directorio_reportes():
    if not os.path.exists(REPORTES_DIR):
        os.makedirs(REPORTES_DIR)

def exportar_reporte_mes(mes, anio):
    asegurar_directorio_reportes()
    prestamos = cargar_prestamos()
    filas = [p for p in prestamos if p.get('mes') == str(mes) and p.get('anio') == str(anio)]
    if not filas:
        print('No hay registros para ese mes/año.')
        return
    nombre = f"{REPORTES_DIR}/reporte_{anio}_{mes:02d}.csv"
    with open(nombre, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','fecha_solicitud','fecha_inicio','fecha_fin_esperada','fecha_devolucion','dias','retraso','estado','mes','anio'])
        for p in filas:
            writer.writerow([p.get('prestamo_id',''), p.get('equipo_id',''), p.get('nombre_equipo',''), p.get('usuario_prestatario',''), p.get('tipo_usuario',''), p.get('fecha_solicitud',''), p.get('fecha_inicio',''), p.get('fecha_fin_esperada',''), p.get('fecha_devolucion',''), p.get('dias',''), p.get('retraso',''), p.get('estado',''), p.get('mes',''), p.get('anio','')])
    print(f'Reporte mensual exportado: {nombre}')

def exportar_reporte_anio(anio):
    asegurar_directorio_reportes()
    prestamos = cargar_prestamos()
    filas = [p for p in prestamos if p.get('anio') == str(anio)]
    if not filas:
        print('No hay registros para ese año.')
        return
    nombre = f"{REPORTES_DIR}/reporte_{anio}.csv"
    with open(nombre, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','fecha_solicitud','fecha_inicio','fecha_fin_esperada','fecha_devolucion','dias','retraso','estado','mes','anio'])
        for p in filas:
            writer.writerow([p.get('prestamo_id',''), p.get('equipo_id',''), p.get('nombre_equipo',''), p.get('usuario_prestatario',''), p.get('tipo_usuario',''), p.get('fecha_solicitud',''), p.get('fecha_inicio',''), p.get('fecha_fin_esperada',''), p.get('fecha_devolucion',''), p.get('dias',''), p.get('retraso',''), p.get('estado',''), p.get('mes',''), p.get('anio','')])
    print(f'Reporte anual exportado: {nombre}')

# ---------------------- main.py ----------------------
from usuarios import validar_login
from equipos import registrar_equipo, listar_equipos, consultar_equipo_por_id
from prestamos import solicitar_prestamo, listar_prestamos, aprobar_rechazar, registrar_devolucion, historial_por_usuario, historial_por_equipo
from reportes import exportar_reporte_mes, exportar_reporte_anio

def menu_equipos():
    while True:
        print('\n--- Gestion de equipos ---')
        print('1. Registrar equipo')
        print('2. Listar equipos')
        print('3. Consultar equipo por ID')
        print('0. Volver')
        opc = input('> ').strip()
        if opc == '1':
            registrar_equipo()
        elif opc == '2':
            listar_equipos()
        elif opc == '3':
            eid = input('ID del equipo: ').strip()
            e = consultar_equipo_por_id(eid)
            if e:
                print(e)
            else:
                print('Equipo no encontrado.')
        elif opc == '0':
            break
        else:
            print('Opcion invalida.')

def menu_prestamos():
    while True:
        print('\n--- Gestion de prestamos ---')
        print('1. Solicitar prestamo (queda PENDIENTE)')
        print('2. Listar solicitudes/Prestamos')
        print('3. Aprobar/Rechazar solicitudes')
        print('4. Registrar devolucion')
        print('5. Historial por usuario')
        print('6. Historial por equipo')
        print('0. Volver')
        opc = input('> ').strip()
        if opc == '1':
            solicitar_prestamo()
        elif opc == '2':
            listar_prestamos()
        elif opc == '3':
            aprobar_rechazar()
        elif opc == '4':
            registrar_devolucion()
        elif opc == '5':
            historial_por_usuario()
        elif opc == '6':
            historial_por_equipo()
        elif opc == '0':
            break
        else:
            print('Opcion invalida.')

def menu_reportes():
    while True:
        print('\n--- Reportes ---')
        print('1. Exportar reporte mensual')
        print('2. Exportar reporte anual')
        print('0. Volver')
        opc = input('> ').strip()
        if opc == '1':
            mes = int(input('Mes (1-12): ').strip())
            anio = int(input('Año (YYYY): ').strip())
            exportar_reporte_mes(mes, anio)
        elif opc == '2':
            anio = int(input('Año (YYYY): ').strip())
            exportar_reporte_anio(anio)
        elif opc == '0':
            break
        else:
            print('Opcion invalida.')

def main():
    user = validar_login()
    if not user:
        return
    while True:
        print('\n=== TechLab - Menu Principal ===')
        print('1. Gestion de equipos')
        print('2. Gestion de prestamos')
        print('3. Reportes')
        print('0. Salir')
        opc = input('> ').strip()
        if opc == '1':
            menu_equipos()
        elif opc == '2':
            menu_prestamos()
        elif opc == '3':
            menu_reportes()
        elif opc == '0':
            print('Adios.')
            break
        else:
            print('Opcion invalida.')

if __name__ == '__main__':
    main()
