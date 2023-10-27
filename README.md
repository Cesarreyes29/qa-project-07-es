# qa-project-07-es
## César Reyes Cohort 04



Este es un código en Python que utiliza la biblioteca Selenium para automatizar la interacción con la aplicación web de Urban.Routes, que se encarga de pedir un taxi para trasladarse de un punto a otro en diferente métodos de transporte. En la aplicación existen diferentes opciones para configurar la ruta en donde se pueden agregar helados, cobijas y otras cosas más. En la aplicación se tiene que agregar un número telefónico en donde llega un mensaje con un código de confirmación para continuar con la solicitud. Se agrega un método de pago y las configuraciones extras para poder realizar el pedido del taxi.



## Tecnologías y técnicas utilizadas

- PYCHARM
- SELENIUM
- WEBDRIVER
- KEYS
- PYTEST

Primero tuvimos que hacer la importación de bibliotecas como import data que es un módulo llamado “data” que se utiliza para almacenar datos como URLs, números de teléfono, etc. También usamos Selenium import webdriver sirve para importar la clase "webdriver" de la biblioteca Selenium, que se utiliza para interactuar con un navegador web y se usaron otras importaciones adicionales de Selenium, como Keys, By, expected_conditions, WebDriverWait, ActionChains y time import sleep para introducir pausas en la ejecución del programa.

## Retrieve_phone_code

Primero se creó una función retrieve_phone_code la cuál recopila registros de mensajes de rendimiento del controlador agregado para buscar un código de confirmación del telefóno

Se crearon 2 clases, la primera es la clase **UrbanRoutesPage** en donde se definen una serie de localizadores que representan elementos de la página web, como campos de entrada, botones, etc y a su vez contiene métodos para interactuar con estos elementos anteriormente mencionados, como establecer una dirección de inicio, establecer una dirección de destino, hacer clic en un botón para solicitar un taxi, ingresar un número de teléfono, agregar un método de pago y más. También se agregó un método wait_for_load_information que es para esperar a que se cargue cierta información en la página.

La segunda clase es **TestUrbanRoutes** en la que se utiliza para definir pruebas automatizadas utilizando el marco de pruebas Pytest, los métodos que se incluyeron son el método setup_class que se ejecuta antes de que comiencen las pruebas y configura un controlador de Selenium. El método test_set_route que realiza una serie de acciones llamando a las funciones que se crearon antes para automatizar acciones en la página web, como estabecer rutas, ingresar información de contacto, método de pago y tomar un taxi, y el método teardown_class cierra el controlador de Selenium al final de las pruebas.

Por último la sección **if__name__ == 'main'** crea una instancia de la clase TestUrbanRoutes, ejecuta las pruebas y luego las cierra.

Se usó la herramienta de **PYTEST** la cuál ayudó a realizar las pruebas y comprobar que funcionarán correctamente, se agregaron validaciones para validar que se haya cumplido la función. 
