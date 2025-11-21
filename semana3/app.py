from servicios import ingresarDatosProducto, mostrarInventario,actualizarProductoMenu
from servicios import eliminarProducto,validarNombre, mostrarProducto, estadisticas,menuCargarArchivo, menuGuardarArchivo


def saltoDeLinea():
    print("---------------------------------------------\n")
while True:
    saltoDeLinea()
    print("1: agregar nuevo producto")
    print("2: monstrar inventario")
    print("3: monstrar producto")
    print("4: actualizar producto")
    print("5: eliminar producto")
    print("6: estadisticas")
    print("7: exportar inventario")
    print("8: cargar nuevo inventario")
    print("9: salir")

    opcion = input()
   
    match opcion:
        case "1":
            saltoDeLinea()
            print("agregar nuevo producto\n")
            ingresarDatosProducto()
            saltoDeLinea()
        case "2":
            saltoDeLinea()
            print("mostrar inventario")
            mostrarInventario()
            saltoDeLinea()
        case "3":
            saltoDeLinea()
            print("mostrar producto")
            nombre = validarNombre()
            mostrarProducto(nombre)
            saltoDeLinea()
        case "4":
            saltoDeLinea()
            print("acutalizar producto")
            actualizarProductoMenu()
            saltoDeLinea()
        case "5":
            saltoDeLinea()
            print("eliminar producto")
            nombre = validarNombre()
            eliminarProducto(nombre)
            saltoDeLinea()
   
        case "6":
            saltoDeLinea()
            print("estadisticas")
            estadisticas()
            saltoDeLinea()

        case "7":
            menuGuardarArchivo()
        
        case "8":
            menuCargarArchivo()
        case "9":
            break
        
        case  _case:
            print("opción inválida")
            saltoDeLinea()
            
    
