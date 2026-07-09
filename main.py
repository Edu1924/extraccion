import os
import time
import gspread
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def formatear_telefono(telefono_sucio):
    limpio = telefono_sucio.replace("(", "").replace(")", "").replace(" ", "")
    resultado = f"+34{limpio}"
    return resultado

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

Google_Sheet_Name = "personas db"
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
ruta_json = os.path.join(os.path.dirname(__file__), "credentials.json")
creds = Credentials.from_service_account_file(ruta_json, scopes=scopes)
gs = gspread.authorize(creds)

sh = gs.open(Google_Sheet_Name).sheet1
records = sh.get_all_records()

print("Conexión exitosa a Google Sheets.")

# Variables principales
numpages = 30
nombres_buscar = ["MARIA","JOSE","ANTONIO","JUAN","FRANCISCO","MANUEL","LUIS","JESUS","ANGEL","JAVIER"]
base = "https://tel.opendi.es/asturias/gijon/"
lista_tabla = []
datos_totales = []

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
                    telefono=formatear_telefono(telefono)
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
            
            if lista_tabla:
                valores_insertar = [[d["Nombre"], d["Telefono"]] for d in lista_tabla]
                
                try:
                    # append_rows busca automáticamente la última fila con valores y agrega los registros
                    sh.append_rows(valores_insertar)
                    print(f"Se insertaron {len(valores_insertar)} registros del lote en Google Sheets.")
                except Exception as e:
                    print(f"Error al insertar el lote en Google Sheets: {e}")
                
                # Guardar en datos_totales para exportar luego el CSV
                datos_totales.extend(lista_tabla)
                # Vaciar la lista_tabla para recolectar los datos de la siguiente página
                lista_tabla = []

        else:
            break

driver.quit()

if datos_totales:
    df = pd.DataFrame(datos_totales)
    nombre_archivo = f"Data_Contactos_{len(nombres_buscar)}_asturias-gijon.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Archivo '{nombre_archivo}' guardado correctamente.")
else:
    print("No se encontraron tablas para guardar.")

print("Scrapping finalizado correctamente.")