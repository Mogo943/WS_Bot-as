import time
import schedule
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.keys import Keys 


# Ruta al controlador de Chrome
filepath = 'V2 selenium\Recursos\whatsapp_session.txt'
driver = RemoteWebDriver

#intervalo de difusion modificable desde un txt
intervalo = open('V2 selenium\Recursos\intervalo_de_difusion.txt', mode = 'r', encoding = 'utf-8')
intervalo = intervalo.read()
intervalo = int(intervalo)

# Conectarse a la sesion de keepSession.py
def create_driver_session():
    global executor_url
    with open (filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return{'success': 0,'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    org_command_execute = RemoteWebDriver.execute
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver

#Establecer instancias en el navegador para evitar fallos
def instancias():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('debuggerAddress', executor_url)

#Funcion para mediante un contacto pasado por parametro buscarlo en el buscador de WS
def buscar_chats(nombre):
    print('\n Buscando chat')
    buscar = driver.find_element(By.XPATH,'//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
    buscar.send_keys(nombre)
    time.sleep(2)

#Funcion para definir mensaje modificable desde txt, copiarlo, buscar el box message de WS y pegar
#de esta forma es posible enviar emojis en el mensaje
#cierra el archivo para evitar fallos en la proxima ejecucion
def enviar_mensaje():
    print('\n Enviando mensaje')
    mensaje = open('V2 selenium\Recursos\mensaje.txt', mode = 'r', encoding = 'utf-8')
    texto = mensaje.read()
    mensaje.close()
    pyperclip.copy(texto)
    box = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    box.send_keys(Keys.CONTROL + "v")
    box.send_keys(Keys.ENTER)
    time.sleep(2)

#Funcion para una vez conseguido el chat abrirlo y enviar el mensaje
def abrir_chat(nombre):
    print('\n Abriendo chat')
    conver = driver.find_element(By.XPATH,f'//span[@title="{nombre}"]')
    conver.click()
    time.sleep(2)
    enviar_mensaje()

#Funcion principal para la ejecucion, hace una lista de contactos desde un txt modificable
#ejecuta un ciclo que recorre la lista donde normaliza el nombre del contacto
#este nombre es pasado por parametro a las funciones anteriormente definidas
#cierra el archivo para evitar fallos en la proxima ejecucion
def difundir():
    print('\n Difundiendo la palabra')
    contacto = open('V2 selenium\Recursos\contactos.txt', mode = 'r', encoding='utf-8')
    chats = contacto.readlines()
    for i in range(0, len(chats)):
        nombre = chats[i].strip()
        buscar_chats(nombre)
        abrir_chat(nombre)
    contacto.close()

#programa principal se definen las variables driver y contacto de forma global, se establece la conexion con keepSession.py
#se establece donde estan los contactos, las instancias y se ejecuta la funcion principal
def whatsapp_boot_init():
    global driver
    driver = create_driver_session()
    instancias()
    difundir()

whatsapp_boot_init()

#funcion para establecer un intervalo de ejecucion de la funcion difundir
schedule.every(intervalo).hours.do(difundir)

#mientras el programa este abierto va a quedar en espera de la siguiente ejecucion de la funcion difundir
while True:
    schedule.run_pending()
    time.sleep(1)