from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def setup_driver():
    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--headless=new')
    opciones.add_argument('--disable-gpu')
    opciones.page_load_strategy = 'eager' 
    
    try:
        driver = webdriver.Chrome(options=opciones)
        print("Navegador abierto en modo rápido.")
        return driver
    except WebDriverException as e:
        print(f"Error al inicializar el navegador WebDriver: {str(e)}")
        exit(1)

# Variables principales
numpages = 20
nombres_buscar = ["MARIA","JOSE","ANTONIO","JUAN","FRANCISCO","MANUEL","CARMEN","LUIS","MIGUEL","VICENTE"]
base = "https://tel.opendi.es/alicante-alacant/elche-elx/"
lista_tabla = []

driver = setup_driver()
wait = WebDriverWait(driver, 5) 

for nombre_b in nombres_buscar:
    for page in range(1, numpages + 1):
        inicial = nombre_b[0].upper()
        URL_SCRAPP = f"{base}{inicial}/{nombre_b}-{page}"
        print(f"Accediendo a la pagina: {URL_SCRAPP}")
        
        try:
            driver.get(URL_SCRAPP)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[itemtype='https://schema.org/Person']")))
        except TimeoutException:
            print("No se encontraron más registros en esta página o demoró mucho.")
            break 
        except WebDriverException as e:
            print(f"Error al cambiar de URL: {str(e)}")
            continue

        personas = driver.find_elements(By.CSS_SELECTOR, "li[itemtype='https://schema.org/Person']")
        print(f"Cargando {len(personas)} registros de personas")

        if personas: 
            for persona in personas:
                try:
                    nombre = persona.find_element(By.CSS_SELECTOR, "[itemprop='name']").text.strip()
                except Exception:
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
        else:
            break   

driver.quit()

if lista_tabla:
    df = pd.DataFrame(lista_tabla)
    # Creamos un nombre de archivo más sencillo o basado en la cantidad de datos
    nombre_archivo = f"Data_Contactos_{len(nombres_buscar)}_nombres.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Archivo '{nombre_archivo}' guardado correctamente al toque.")
else:
    print("No se encontraron tablas para guardar.")

print("Scrapping finalizado correctamente.")