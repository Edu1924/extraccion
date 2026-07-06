from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from io import StringIO
import os

def setup_driver():
    try:
        driver = webdriver.Chrome(options=opciones)
        time.sleep(5)
        driver.get("https://google.com")
        time.sleep(3)
        print("Navegador abierto correctamente.")
        return driver
    except WebDriverException as e:
        print(f"Error al inicializar el navegador WebDriver: {str(e)}")
        exit(1)

def cambiarurl(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        print("Navegador abierto correctamente.")
        return True
    except WebDriverException as e:
        print(f"Error al cambiar de URL: {str(e)}")
        return False

url_base=input("Ingresa la UL base: ")
numpages=input("Ingresa el numero de paginas que tiene la URL base: ")
opciones = webdriver.ChromeOptions()
lista_tabla=[]
driver=setup_driver()

for page in range(1, int(numpages)+1):
    URL_SCRAPP= url_base + "-" + str(page)
    print("Accediendo a la pagina ", URL_SCRAPP)
    
    if not cambiarurl(driver, URL_SCRAPP):
        print("Error al cambiar de URL")
        continue

    personas = driver.find_elements(By.CSS_SELECTOR, "li[itemtype='https://schema.org/Person']")
    print(f"Cargando {len(personas)} registros de personas")

    for persona in personas:
        try:
            nombre=persona.find_element(By.CSS_SELECTOR, "[itemprop='name']").text.strip()
            print(nombre)
            
        except Exception as e:
            print("Error al procesar la pagina: ", e)
            continue

        try:
            telefono = persona.find_element(By.CSS_SELECTOR, "[itemprop='telephone']").text.strip()
        except NoSuchElementException:
            telefono = "No disponible"
        
        try:
            localidad = persona.find_element(By.CSS_SELECTOR, "[itemprop='addressLocality']").text.strip()
        except NoSuchElementException:
            localidad = "No disponible"
        
        lista_tabla.append({
            "Nombre": nombre,
            "Telefono": telefono,
            "Localidad": localidad
        })

driver.quit()

if lista_tabla:
    df=pd.DataFrame(lista_tabla)
    nombre=input("Ingresa el nombre del archivo: ")
    nombre_archivo=nombre+".csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print("Archivo guardado correctamente.")
else:
    print("No se encontraron tablas para guardar.")

print("Scrapping finalizado correctamente.")