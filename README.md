# Proyecto Aurelion - Segmentación de Clientes

## 1. Tema, Problema y Solución

### Tema
Mini-market Los latinos

### Problema

El mini-market "Los Latinos" es un negocio de retail ubicado en una zona urbana que está enfrentando dificultades para identificar los hábitos de compra de sus clientes. Actualmente, el equipo de ventas se basa en métodos tradicionales como encuestas y observaciones, lo que resulta en un uso ineficiente de los recursos disponibles. Esta falta de análisis limita la capacidad para personalizar estrategias de marketing y maximizar el valor de los clientes, lo que impacta negativamente en la efectividad de las promociones y en la fidelización a largo plazo.

### Solución
La solución consiste en implementar un sistema de segmentación de clientes basado en el análisis RFM (Recencia, Frecuencia y Valor Monetario) y el uso de algoritmos de clustering como K-means para identificar patrones de compra. Esta propuesta se plantea porque los métodos tradicionales de observación y encuestas no permiten obtener información precisa ni aprovechar los datos disponibles. Su propósito es clasificar a los clientes en grupos homogéneos y visualizar los resultados en un dashboard interactivo en Power BI, con el fin de personalizar estrategias de marketing, optimizar recursos y mejorar la fidelización de los clientes del mini-market Los Latinos.

---

## 2. Estructura, Tipos y Escala de la Base de Datos

### 2.1. Estructura de la Base de Datos

La base de datos del Minimarket Los Latinos consta de cuatro tablas relacionales que conforman un modelo de datos orientado al registro de ventas y clientes. El diseño incluye dos tablas dimensionales (Clientes y Productos) que almacenan la información maestra del negocio, y dos tablas de hechos (Ventas y Detalle_ventas) que registran las transacciones. Esta estructura permite rastrear el comportamiento de compra de los clientes, el desempeño de productos por categoría, y analizar patrones de venta a lo largo del tiempo. Las relaciones entre tablas están establecidas mediante llaves foráneas que garantizan la integridad referencial de los datos.

---

#### 2.1.1. Clientes (Tabla Dimensional)

Esta tabla almacena la información de los clientes registrados en el sistema, permitiendo identificar y contactar a cada cliente, así como conocer su ubicación geográfica y antigüedad en el negocio.

- **id_cliente**
Identificador único asignado a cada cliente (llave primaria). Permite diferenciar de manera inequívoca a cada cliente en el sistema.

- **nombre_cliente**
Contiene el nombre completo del cliente registrado.

- **email**
Contiene la dirección de correo electrónico del cliente para comunicaciones y marketing.

- **ciudad**
Contiene la ciudad de residencia del cliente, útil para análisis geográficos y logística.

- **fecha_alta**
Contiene la fecha en que el cliente fue registrado por primera vez en el sistema, permitiendo calcular su antigüedad.

---

#### 2.1.2. Productos (Tabla Dimensional)

Esta tabla contiene el catálogo completo de productos disponibles en la tienda, incluyendo su clasificación por categoría y precio de venta.

- **id_producto**
Identificador único asignado a cada producto (llave primaria). Permite identificar de manera inequívoca cada artículo del inventario.

- **nombre_producto**
Contiene el nombre descriptivo del producto tal como se presenta al cliente.

- **categoria**
Indica la categoría a la que pertenece el producto (ej: Alimentos, Limpieza, etc.), facilitando el análisis por grupos de productos.

- **precio_unitario**
Indica el precio de venta actual del producto por unidad.

---

#### 2.1.3. Ventas (Tabla de Hechos)

Esta tabla registra las transacciones de venta realizadas en la tienda, capturando información sobre cuándo se realizó la compra, quién la realizó y el método de pago utilizado.

- **id_venta**
Identificador único asignado a cada transacción de venta (llave primaria). Permite rastrear cada operación comercial de manera individual.

- **fecha**
Indica la fecha en que se realizó la transacción de venta, fundamental para análisis temporales y estacionalidad.

- **id_cliente**
Identificador del cliente que realizó la compra (llave foránea). Establece la relación con la tabla Clientes.

- **nombre_cliente**
Indica el nombre del cliente que realizó la compra (campo redundante para consultas rápidas).

- **email**
Indica el correo electrónico del cliente que realizó la compra (campo redundante para consultas rápidas).

- **medio_pago**
Indica el método de pago utilizado en la transacción (qr, efectivo, tarjeta, transferencia, etc.).

---

#### 2.1.4. Detalle_ventas (Tabla de Hechos - Detalle)

Esta tabla almacena el desglose detallado de cada venta, registrando los productos específicos comprados, cantidades, precios y el importe total por línea de venta.

- **id_venta**
Identificador de la venta a la que pertenece este detalle (llave foránea). Establece la relación con la tabla Ventas.

- **id_producto**
Identificador del producto vendido (llave foránea). Establece la relación con la tabla Productos.

- **nombre_producto**
Indica el nombre del producto vendido (campo redundante para consultas rápidas).

- **cantidad**
Indica la cantidad de unidades vendidas del producto en esta línea de venta.

- **precio_unitario**
Indica el precio por unidad al momento de la venta (puede diferir del precio actual en la tabla Productos).

- **importe**
Indica el monto total de esta línea de venta, calculado como cantidad × precio_unitario.


#### 2.2. Tipos de Datos y Escalas


1. **Tabla Clientes**
    - `id_cliente`: Número entero, escala **Razón** (identificador único con cero absoluto).
    - `nombre_cliente`: Cadena de texto, escala **Nominal** (nombre categórico sin orden).
    - `email`: Cadena de texto, escala **Nominal** (correo electrónico categórico sin orden).
    - `ciudad`: Cadena de texto, escala **Nominal** (ciudad categórica sin orden).
    - `fecha_alta`: Fecha, escala **Intervalo** (fecha sin cero real).

2. **Tabla Ventas**
    - `id_venta`: Número entero, escala **Razón** (identificador único con cero absoluto).
    - `fecha`: Fecha, escala **Intervalo** (fecha sin cero real).
    - `id_cliente`: Número entero, escala **Razón** (identificador con cero absoluto, clave foránea).
    - `nombre_cliente`: Cadena de texto, escala **Nominal** (nombre categórico sin orden, redundante).
    - `email`: Cadena de texto, escala **Nominal** (correo categórico sin orden, redundante).
    - `medio_pago`: Cadena de texto, escala **Nominal** (método de pago categórico sin orden).

3. **Tabla Detalle_ventas**
    - `id_venta`: Número entero, escala **Razón** (identificador con cero absoluto, clave foránea).
    - `id_producto`: Número entero, escala **Razón** (identificador con cero absoluto, clave foránea).
    - `nombre_producto`: Cadena de texto, escala **Nominal** (nombre categórico sin orden, redundante).
    - `cantidad`: Número entero, escala **Razón** (cantidad numérica con cero absoluto).
    - `precio_unitario`: Número decimal, escala **Razón** (precio numérico con cero absoluto).
    - `importe`: Número decimal, escala **Razón** (importe numérico con cero absoluto).

4. **Tabla Productos**
    - `id_producto`: Número entero, escala **Razón** (identificador único con cero absoluto).
    - `nombre_producto`: Cadena de texto, escala **Nominal** (nombre categórico sin orden).
    - `categoria`: Cadena de texto, escala **Nominal** (categoría categórica sin orden).
    - `precio_unitario`: Número decimal, escala **Razón** (precio numérico con cero absoluto).

        ## 6. Información, pasos y pseudocódigo mejorados

        ### Información
        - **Entrada:** Solicitud del usuario para consultar una sección específica de la documentación.
        - **Proceso:** Mostrar un menú interactivo, permitir al usuario seleccionar una opción, buscar la información correspondiente en la documentación y mostrarla.
        - **Salida:** Contenido de la sección seleccionada o un mensaje de error si la opción no es válida.

        ### Pasos
        1. Mostrar un mensaje de bienvenida al usuario.
        2. Presentar un menú con las opciones disponibles: "Tema", "Problema", "Solución", "Estructura de la Base de Datos", "Integrantes del Equipo", "Salir".
        3. Solicitar al usuario que seleccione una opción del menú.
        4. Según la opción seleccionada:
            - Si es una sección válida, buscar y mostrar el contenido correspondiente.
            - Si la opción no es válida, mostrar un mensaje de error.
        5. Repetir el proceso hasta que el usuario seleccione "Salir".
        6. Mostrar un mensaje de despedida y finalizar el programa.

        ### Pseudocódigo
        ```plaintext
        INICIO
          MOSTRAR "Bienvenido al sistema de consulta de Documentación"
          
          REPETIR
             MOSTRAR "Menú de opciones:"
             MOSTRAR "1. Tema"
             MOSTRAR "2. Problema"
             MOSTRAR "3. Solución"
             MOSTRAR "4. Estructura de la Base de Datos"
             MOSTRAR "5. Integrantes del Equipo"
             MOSTRAR "6. Salir"
             SOLICITAR "Seleccione una opción: " -> opcion
             
             SI opcion = 6 ENTONCES
                  MOSTRAR "Gracias por usar el sistema. ¡Hasta luego!"
                  TERMINAR
             FIN SI
             
             SEGÚN opcion HACER
                  CASO 1:
                        MOSTRAR "Tema: Mini-market Los Latinos"
                  CASO 2:
                        MOSTRAR "Problema: El mini-market enfrenta dificultades para identificar los hábitos de compra de sus clientes..."
                  CASO 3:
                        MOSTRAR "Solución: Implementar un sistema de segmentación de clientes basado en análisis RFM..."
                  CASO 4:
                        MOSTRAR "Estructura de la Base de Datos: La base de datos consta de cuatro tablas relacionales..."
                  CASO 5:
                        MOSTRAR "Integrantes del Equipo: Somos de la CAMADA 16 DE IBM IA y somos: Octavio Joaquin Sosa, Renzo Gama Peraltilla, Paula Rocio Miranda, Jhon Cuji, Axcel Espinoza."
                  OTRO CASO:
                        MOSTRAR "Opción no válida. Intente nuevamente."
             FIN SEGÚN
          HASTA opcion = 6
        FIN
        ```

        ### Diagrama de flujo
        ```mermaid
        flowchart TD
            A[Inicio] --> B[Mostrar mensaje de bienvenida]
            B --> C[Mostrar menú de opciones]
            C --> D[Solicitar selección del usuario]
            D --> E{Salir?}
            E -- Sí --> F[Mostrar mensaje de despedida]
            F --> G[Fin]
            E -- No --> H{Opcion válida?}
            H -- No --> I[Mostrar 'Opción no válida']
            I --> C
            H -- Sí --> J{Es 'Integrantes del Equipo'?}
            J -- Sí --> K[Mostrar integrantes del equipo]
            K --> C
            J -- No --> L[Mostrar contenido de la sección seleccionada]
            L --> C
        ```

## 3. Análisis Exploratorio de Datos (EDA) y Resultados Clave

Una vez completada la limpieza, consolidación y cálculo de las métricas RFM, se procedió al Análisis Exploratorio de Datos (EDA) para validar los supuestos y obtener *insights* críticos antes de la modelación con K-means.

### 3.1. Métricas RFM y Distribución de Variables

#### Estadísticas descriptivas básicas calculadas
Se calcularon las estadísticas descriptivas para las métricas RFM de cada cliente. Los resultados iniciales mostraron que la **media** de **Frecuencia** y **Monetario** es significativamente más alta que su respectiva **mediana (50%)**.

#### Identificación del tipo de distribución de variables
* Se visualizó la distribución de **Frecuencia** y **Monetario** (histogramas), confirmando que ambas presentan una **fuerte asimetría positiva** (sesgo a la derecha).
* **Conclusión Clave:** Esta asimetría prueba que solo una pequeña proporción de clientes (la "cola larga") concentra el mayor valor y la mayor cantidad de compras. Esto justifica plenamente la necesidad de la segmentación.

### 3.2. Correlaciones, Outliers y Patrones de Negocio

#### Análisis de correlaciones entre variables principales
Se analizó la correlación lineal entre las variables de comportamiento:
* **Frecuencia vs. Monetario:** Se observó una correlación **altamente positiva** (índice > 0.70). Esto demuestra que si la estrategia de marketing logra que un cliente **vuelva más seguido (aumentar Frecuencia)**, su Valor Monetario aumentará de manera significativa.
* **Recencia vs. Frecuencia:** La correlación **negativa** indica que los clientes que han comprado más recientemente (R baja) son, de hecho, los más frecuentes, lo cual es un indicador de salud en la fidelización.

#### Detección de outliers (valores extremos)
Mediante el uso de Boxplots, se identificaron dos grupos de clientes atípicos que requieren atención inmediata:
* **Outliers en Frecuencia y Monetario:** Son los **clientes 'Campeones' o 'VIP'**. Estos clientes, estadísticamente anómalos por su alto valor, deben ser el foco de programas de lealtad premium.
* **Outliers en Recencia:** Son los **clientes 'En Riesgo de Fuga' o 'Perdidos'** (los que tienen una Recencia muy alta), y son el objetivo primario de las campañas de reactivación.

#### Al menos 3 gráficos representativos y patrones adicionales
Se crearon visualizaciones clave para la interpretación de negocio:
1.  **Ventas Totales a lo largo del Tiempo:** Permitió identificar **patrones de estacionalidad** (días o meses pico de compra).
2.  **Valor Monetario Total por Ciudad:** Identificó las **ciudades geográficas que concentran el mayor ingreso** (ej., Rio Cuarto, Carlos Paz), permitiendo la **focalización de los recursos de marketing**.
3.  **Frecuencia de Métodos de Pago:** Reveló la **preferencia de hábito de pago** (ej., predominio de QR o Tarjeta), clave para el diseño de promociones y la optimización de infraestructura.

#### Interpretación de resultados orientada al problema
Los hallazgos del EDA ofrecen una solución directa al problema de negocio:
* **Validación:** Se confirma que el **uso ineficiente de recursos** se debe a la distribución desigual de clientes (pocos valiosos vs. muchos de bajo valor), haciendo obligatoria la segmentación.
* **Estrategia:** La evidencia de correlación F vs. M define que la prioridad estratégica es la **recurrencia y la retención**.
* **Acción Inmediata:** La identificación de outliers y patrones geográficos permite al minimarket generar campañas dirigidas y altamente eficientes **incluso antes de aplicar el algoritmo K-means**.