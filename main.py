import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    ask_taxi_button = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[1]/div[3]/div[1]/button")
    comfort_button = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[1]/div[5]")
    phone_button = (By.CLASS_NAME, "np-button")
    phone_fill = (By.NAME, 'phone')
    next_button = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[1]/form/div[2]/button")
    code_field = (By.ID, "code")
    next_button_code = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[2]/form/div[2]/button[1]")
    way_pay = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[2]")
    add_card_button = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[3]")
    card_number_field = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/input")
    card_code_field = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input")
    enlace_button = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]")
    close_button = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/button")
    comment_field = (By.ID, "comment")
    check_slider = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    counter_plus = (By.CLASS_NAME, "counter-plus")
    take_taxi_button = (By.XPATH, "/html/body/div/div/div[3]/div[4]/button")
    header_travel_information = (By.XPATH, "/html/body/div/div/div[5]/div[2]/div[2]/div[1]/div[1]/div[2]")
    order_header_time = (By.XPATH, "/html/body/div/div/div[5]/div[2]/div[1]/div/div[2]")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_ask_taxi(self):
        self.driver.find_element(*self.ask_taxi_button).click()

    def click_comfort_option(self):
        self.driver.find_element(*self.comfort_button).click()

    def set_phone_number(self, the_phone):

        self.driver.find_element(*self.phone_button).click() #Dar click a agregar número

        self.driver.find_element(*self.phone_fill).send_keys(the_phone) #Colocar número telefónico

        self.driver.find_element(*self.next_button).click() #Dar click al boton siguiente

        self.driver.find_element(*self.code_field).send_keys(retrieve_phone_code(self.driver)) #Agregar código de telefono

        self.driver.find_element(*self.next_button_code).click() #Click botón para confirmar código

    def set_payment_method(self, the_card, the_code):

        self.driver.find_element(*self.way_pay).click() #Click botón agregar método de pago

        self.driver.find_element(*self.add_card_button).click() #Click botón agregar tarjeta

        self.driver.find_element(*self.card_number_field).send_keys(the_card) #Agregar número de tarjeta

        self.driver.find_element(*self.card_code_field).send_keys(the_code) #Agregar Codigo de la tarjeta
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB) #Dar click en Teclado TAB

        self.driver.find_element(*self.enlace_button).click() #Dar click botón enlace

        self.driver.find_element(*self.close_button).click() #Cerrar Ventana de agregar metodo de pago

    def add_extra_details(self, comment_for_driver):

        self.driver.find_element(*self.comment_field).send_keys(comment_for_driver) #Agregar comentario al conductor

        self.driver.find_element(*self.check_slider).click() #Agregar manta y pañuelos

        action_chains = ActionChains(self.driver)
        action_chains.double_click(self.driver.find_element(*self.counter_plus)).perform() #Agregar Helado

    def take_taxi(self):
        self.driver.find_element(*self.take_taxi_button).click()

    def wait_for_load_information(self):
        WebDriverWait(self.driver, 35).until(EC.presence_of_element_located(self.header_travel_information))

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.click_ask_taxi()
        routes_page.click_comfort_option()
        the_phone = data.phone_number
        routes_page.set_phone_number(the_phone)
        the_card = data.card_number
        the_code = data.card_code
        routes_page.set_payment_method(the_code, the_card)
        comment_for_driver = data.message_for_driver
        routes_page.add_extra_details(comment_for_driver)
        routes_page.take_taxi()
        routes_page.wait_for_load_information()

    @classmethod
    def teardown_class(cls):
        sleep(2)
        cls.driver.quit()


if __name__ == '__main__':
    test_valid_data = TestUrbanRoutes()
    test_valid_data.setup_class()
    test_valid_data.teardown_class()
