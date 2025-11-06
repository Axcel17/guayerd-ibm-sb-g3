import os

def leer_documentacion(ruta_archivo):
    """
    Lee el contenido del archivo de documentación Markdown
    y lo estructura en un diccionario.
    """
    try:
        # En lugar de leer y procesar el archivo completo,
        # definimos directamente la información que necesitamos
        secciones = {
            "tema": "Mini-market Los latinos",
            "problema": (
                "El mini-market \"Los Latinos\" es un negocio de retail ubicado en una zona urbana "
                "que está enfrentando dificultades para identificar los hábitos de compra de sus clientes. "
                "Actualmente, el equipo de ventas se basa en métodos tradicionales como encuestas y observaciones, "
                "lo que resulta en un uso ineficiente de los recursos disponibles. Esta falta de análisis limita la "
                "capacidad personalizar estrategias de marketing y maximizar el valor de los clientes, lo que "
                "impacta negativamente en la efectividad de las promociones y en la fidelización a largo plazo."
            ),
            "solucion": (
                "La solución consiste en implementar un sistema de segmentación de clientes basado "
                "en el análisis RFM (Recencia, Frecuencia y Valor Monetario) y el uso de algoritmos "
                "de clustering como K-means para identificar patrones de compra. Esta propuesta se "
                "plantea porque los métodos tradicionales de observación y encuestas no permiten "
                "obtener información precisa ni aprovechar los datos disponibles. Su propósito es "
                "clasificar a los clientes en grupos homogéneos y visualizar los resultados en un "
                "dashboard interactivo en Power BI, con el fin de personalizar estrategias de marketing, "
                "optimizar recursos y mejorar la fidelización de los clientes del mini-market Los Latinos."
            ),
            "estructura_bd": (
                "La base de datos del Minimarket Los Latinos consta de cuatro tablas relacionales "
                "que conforman un modelo de datos orientado al registro de ventas y clientes. "
                "El diseño incluye dos tablas dimensionales (Clientes y Productos) que almacenan "
                "la información maestra del negocio, y dos tablas de hechos (Ventas y Detalle_ventas) "
                "que registran las transacciones. Esta estructura permite rastrear el comportamiento de "
                "compra de los clientes, el desempeño de productos por categoría, y analizar patrones "
                "de venta a lo largo del tiempo. Las relaciones entre tablas están establecidas mediante "
                "llaves foráneas que garantizan la integridad referencial de los datos."
            ),
            "tablas": {
                "clientes": (
                    "TABLA CLIENTES (DIMENSIONAL)\n\n"
                    "Esta tabla almacena la información de los clientes registrados en el sistema, "
                    "permitiendo identificar y contactar a cada cliente, así como conocer su ubicación "
                    "geográfica y antigüedad en el negocio.\n\n"
                    "- id_cliente: Identificador único asignado a cada cliente (llave primaria).\n"
                    "- nombre_cliente: Contiene el nombre completo del cliente registrado.\n"
                    "- email: Contiene la dirección de correo electrónico del cliente.\n"
                    "- ciudad: Contiene la ciudad de residencia del cliente.\n"
                    "- fecha_alta: Contiene la fecha en que el cliente fue registrado por primera vez."
                ),
                "productos": (
                    "TABLA PRODUCTOS (DIMENSIONAL)\n\n"
                    "Esta tabla contiene el catálogo completo de productos disponibles en la tienda, "
                    "incluyendo su clasificación por categoría y precio de venta.\n\n"
                    "- id_producto: Identificador único asignado a cada producto (llave primaria).\n"
                    "- nombre_producto: Contiene el nombre descriptivo del producto.\n"
                    "- categoria: Indica la categoría a la que pertenece el producto.\n"
                    "- precio_unitario: Indica el precio de venta actual del producto por unidad."
                ),
                "ventas": (
                    "TABLA VENTAS (HECHOS)\n\n"
                    "Esta tabla registra las transacciones de venta realizadas en la tienda, capturando "
                    "información sobre cuándo se realizó la compra, quién la realizó y el método de pago.\n\n"
                    "- id_venta: Identificador único asignado a cada transacción de venta (llave primaria).\n"
                    "- fecha: Indica la fecha en que se realizó la transacción de venta.\n"
                    "- id_cliente: Identificador del cliente que realizó la compra (llave foránea).\n"
                    "- nombre_cliente: Indica el nombre del cliente que realizó la compra.\n"
                    "- email: Indica el correo electrónico del cliente que realizó la compra.\n"
                    "- medio_pago: Indica el método de pago utilizado en la transacción."
                ),
                "detalle_ventas": (
                    "TABLA DETALLE_VENTAS (HECHOS - DETALLE)\n\n"
                    "Esta tabla almacena el desglose detallado de cada venta, registrando los productos "
                    "específicos comprados, cantidades, precios y el importe total por línea de venta.\n\n"
                    "- id_venta: Identificador de la venta a la que pertenece este detalle (llave foránea).\n"
                    "- id_producto: Identificador del producto vendido (llave foránea).\n"
                    "- nombre_producto: Indica el nombre del producto vendido.\n"
                    "- cantidad: Indica la cantidad de unidades vendidas del producto.\n"
                    "- precio_unitario: Indica el precio por unidad al momento de la venta.\n"
                    "- importe: Indica el monto total de esta línea de venta."
                )
            },
            "integrantes": (
            "Somos de la CAMADA 16 DE IBM IA. Nuestro equipo está conformado por:\n"
                "- John Cuji\n"
                "- Octavio Joaquin Sosa\n"
                "- Renzo Gama Peraltilla\n"
                "- Paula Rocio Miranda\n"
                "- Karla Jazmín Ramírez\n"
                "- Jean Manuel Córdova\n"
                "- Axcel Espinoza"
            )
        }
        
        return secciones
        
    except FileNotFoundError:
        print(f"¡Error! No se encontró el archivo de documentación en: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer la documentación: {str(e)}")
        return None

def mostrar_tabla(nombre_tabla, contenido):
    """
    Muestra la información detallada de una tabla específica.
    """
    print(f"\n{'=' * 80}")
    print(f"TABLA: {nombre_tabla.upper()}")
    print(f"{'=' * 80}")
    print(contenido)
    print(f"{'=' * 80}")
    input("\nPresione Enter para continuar...")

def mostrar_seccion(titulo, contenido):
    """
    Muestra una sección de la documentación con un formato amigable.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{'=' * 80}")
    print(f"{titulo.upper().center(80)}")
    print(f"{'=' * 80}")
    print(contenido)
    print(f"{'=' * 80}")
    input("\nPresione Enter para continuar...")

def submenu_estructura(docs):
    """
    Muestra un submenú para la sección de Estructura de la Base de Datos.
    """
    while True:
        print("\n" + "=" * 80)
        print("ESTRUCTURA DE LA BASE DE DATOS")
        
        print(docs["estructura_bd"])
        print("\nDetalles de tablas disponibles:")
        print("1. Tabla Clientes")
        print("2. Tabla Productos")
        print("3. Tabla Ventas")
        print("4. Tabla Detalle_ventas")
        print("5. Volver al menú principal")
        
        opcion = input("\n¿Qué tabla desea consultar? (1-5): ").strip()
        
        if opcion == "1":
            mostrar_tabla("Clientes", docs["tablas"]["clientes"])
        elif opcion == "2":
            mostrar_tabla("Productos", docs["tablas"]["productos"])
        elif opcion == "3":
            mostrar_tabla("Ventas", docs["tablas"]["ventas"])
        elif opcion == "4":
            mostrar_tabla("Detalle_ventas", docs["tablas"]["detalle_ventas"])
        elif opcion == "5":
            return
        else:
            input("Opción no válida. Presione Enter para intentar de nuevo...")

def mostrar_resumen_proyecto(docs):
    """
    Muestra un resumen completo del proyecto con toda la información clave.
    """
    print("\n" + "=" * 80)
    
    print("\n📌 TEMA DEL PROYECTO")
    print("-" * 80)
    print(docs["tema"])
    
    print("\n📌 PROBLEMA IDENTIFICADO")
    print("-" * 80)
    print(docs["problema"])
    
    print("\n📌 SOLUCIÓN PROPUESTA")
    print("-" * 80)
    print(docs["solucion"])
    

def main():
    """
    Función principal que ejecuta el menú interactivo del sistema.
    """
    # Ruta al archivo de documentación
    ruta_documentacion = os.path.join(os.path.dirname(__file__), "Documentación.md")
    
    # Leer la documentación
    docs = leer_documentacion(ruta_documentacion)
    if not docs:
        print("No se pudo cargar la documentación. El programa no puede continuar.")
        return
    
    # Menú principal
    while True:
        print("MINI-MARKET 'LOS LATINOS' - SISTEMA DE CONSULTA DE DOCUMENTACIÓN")
        
        print("\n¡Bienvenido al sistema de consulta de documentación del Mini-market 'Los Latinos'!")
        print("Aquí puede obtener información sobre nuestro proyecto de segmentación de clientes.")
        
        print("\nMenú de opciones:")
        print("1. Ver resumen completo del proyecto")
        print("2. Tema del proyecto")
        print("3. Problema identificado")
        print("4. Solución propuesta")
        print("5. Estructura de la base de datos")
        print("6. Integrantes del equipo")
        print("7. Salir")

        try:
            opcion = input("\nPor favor, seleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                mostrar_resumen_proyecto(docs)
            elif opcion == "2":
                mostrar_seccion("Tema del Proyecto", docs["tema"])
            elif opcion == "3":
                mostrar_seccion("Problema Identificado", docs["problema"])
            elif opcion == "4":
                mostrar_seccion("Solución Propuesta", docs["solucion"])
            elif opcion == "5":
                submenu_estructura(docs)
            elif opcion == "6":
                mostrar_seccion("Integrantes del Equipo", docs["integrantes"])
            elif opcion == "7":
                print("\n¡Gracias por utilizar nuestro sistema de consulta de documentación!")
                print("¡Hasta pronto!")
                break
            else:
                input("\nOpción no válida. Presione Enter para intentar de nuevo...")
        
        except KeyboardInterrupt:
            print("\n\nOperación interrumpida por el usuario. Saliendo del programa...")
            break
        except Exception as e:
            print(f"\nOcurrió un error inesperado: {str(e)}")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()
