import csv

def loadInventario() -> list[dict]:
    try:
        with open("inventario.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            inventario = list(reader)         
    except:
        inventario = []
    return inventario

inventario = loadInventario()


def saveInventario(inventario : list[dict]):
    try:
        with open("inventario.csv", "w", newline="", encoding="utf-8") as file:
            if inventario:
                fields = inventario[0].keys()
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(inventario)
    except: print("error al guardar inventario")

#-----------------------------------------------------------------------------------------------------------------

def loadNuevoInventario(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            nuevoInventario = list(reader)
            return nuevoInventario
    except:
            print("ruta no encontrada")
            return None
    
def fucionarInventarios(nuevoInventario):
    for producto in nuevoInventario:
        inventario.append(producto)
    saveInventario(inventario)
    return inventario

def sobrescribirInventario(nuevoInventario):

    inventario.clear()
    inventario.extend(nuevoInventario)
    saveInventario(inventario)
    return inventario

def exportarArchivo(archivo):
    with open(archivo, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=["nombre","precio","cantidad"])
        writer.writeheader()
        writer.writerows(inventario)
   
    
