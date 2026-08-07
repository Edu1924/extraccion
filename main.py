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
from datetime import datetime, timedelta
def setup_driver():
    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--headless=new')
    opciones.add_argument('--disable-gpu')
    opciones.add_argument('--no-sandbox')
    opciones.add_argument('--disable-dev-shm-usage')
    opciones.add_argument('--window-size=1920,1080')
    opciones.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=opciones)
        print("Navegador abierto en modo rápido.")
        return driver
    except WebDriverException as e:
        print(f"Error al inicializar el navegador WebDriver: {str(e)}")
        exit(1)

Google_Sheet_Name = "trabajos-empleosya"
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
numpages = 25
logo="https://empleosya.com.pe/wp-content/uploads/500-X-500_Mesa-de-trabajo-1.webp"
web_empresa="google.com"
hoy=datetime.now()
mas30=hoy+timedelta(days=30)
fecha_expiracion=mas30.strftime("%Y-%m-%d")
#base = "https://www.bumeran.com.pe/empleos-area-comercial-ventas-y-negocios.html?recientes=true&"  #Comercial, Ventas y Negocios 
#base = "https://www.bumeran.com.pe/empleos-area-administracion-contabilidad-y-finanzas.html?recientes=true&" #Administración, Contabilidad y Finanzas
#base = "https://www.bumeran.com.pe/empleos-area-tecnologia-sistemas-y-telecomunicaciones.html?recientes=true&" #Tecnología, Sistemas y Telecomunicaciones
#base = "https://www.bumeran.com.pe/empleos-area-atencion-al-cliente-call-center-y-telemarketing.html?recientes=true&" #Atención al Cliente, Call Center y Telemarketing
#base = "https://www.bumeran.com.pe/empleos-area-abastecimiento-y-logistica.html?recientes=true&" #Abastecimiento y Logística
#base = "https://www.bumeran.com.pe/empleos-area-oficios-y-otros.html?recientes=true&" #Oficios y Otros
#base = "https://www.bumeran.com.pe/empleos-area-produccion-y-manufactura.html?recientes=true&" #Producción y Manufactura
#base = "https://www.bumeran.com.pe/empleos-area-ingenierias.html?recientes=true&" #Ingenierías
#base = "https://www.bumeran.com.pe/empleos-area-mineria-petroleo-y-gas.html?recientes=true&" #Minería, Petróleo y Gas
#base = "https://www.bumeran.com.pe/empleos-area-recursos-humanos-y-capacitacion.html?recientes=true&" #Recursos Humanos y Capacitación
#base = "https://www.bumeran.com.pe/empleos-area-ingenieria-civil-y-construccion.html?recientes=true&" #Ingeniería Civil y Construcción
#base = "https://www.bumeran.com.pe/empleos-area-marketing-y-publicidad.html?recientes=true&" #Marketing y Publicidad
#base = "https://www.bumeran.com.pe/empleos-area-salud-medicina-y-farmacia.html?recientes=true&" #Salud, Medicina y Farmacia
base = "https://www.bumeran.com.pe/empleos-area-gastronomia-y-turismo.html?recientes=true&" #Gastronomía y Turismo
#base = "https://www.bumeran.com.pe/empleos-area-educacion-docencia-e-investigacion.html?recientes=true&" #Educación, Docencia e Investigación 
#base = "https://www.bumeran.com.pe/empleos-area-legales.html?recientes=true&" #Legales 
#base = "https://www.bumeran.com.pe/empleos-area-diseno.html?recientes=true&" #Diseño
#base = "https://www.bumeran.com.pe/empleos-area-comunicacion-relaciones-institucionales-y-publicas.html?recientes=true&" #Comunicación, Relaciones Institucionales y Públicas
####base = "https://www.bumeran.com.pe/empleos-area-secretarias-y-recepcion.html?recientes=true&" #Secretarias y Recepción
#base = "https://www.bumeran.com.pe/empleos-area-aduana-y-comercio-exterior.html?recientes=true&" #Aduana y Comercio Exterior
#base = "https://www.bumeran.com.pe/empleos-area-seguros.html?recientes=true&" #Seguros
#base = "https://www.bumeran.com.pe/empleos-area-departamento-tecnico.html?recientes=true&" #Departamento Tecnico
#base = "https://www.bumeran.com.pe/empleos-area-sociologia-trabajo-social.html?recientes=true&" #Sociología / Trabajo Social
#base = "https://www.bumeran.com.pe/empleos-area-naviero-maritimo-portuario.html?recientes=true&" #Naviero, Maritimo, Portuario
#base = "https://www.bumeran.com.pe/empleos-area-enfermeria.html?recientes=true&" #Enfermería
#base = "https://www.bumeran.com.pe/empleos-area-gerencia-y-direccion-general.html?recientes=true&" #Gerencia y Dirección General
basepage="page="
lista_tabla = []
datos_totales = []

driver = setup_driver()
wait = WebDriverWait(driver, 15) 

for page in range(1, numpages + 1):
    URL_SCRAPP = f"{base}{basepage}{page}"
    print(f"Accediendo a la pagina: {URL_SCRAPP}")
    driver.get(URL_SCRAPP)    
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listado-avisos"]//a[contains(@href, "/empleos/")]')))
    except TimeoutException:
        print("No se encontraron anuncios o tardó demasiado en cargar la página.")
        break 
    except WebDriverException as e:
        print(f"Error al cambiar de URL: {str(e)}")
        continue

    trabajos = driver.find_elements(By.XPATH, '//*[@id="listado-avisos"]//a[contains(@href, "/empleos/")]')
                                                
    print(f"Cargando {len(trabajos)} registros de trabajos")

    if trabajos: 
        for trabajo in trabajos:
            try:
                puesto = trabajo.find_element(By.TAG_NAME, 'h2').text.strip()
            except Exception:
                continue

            try:
                empresa = trabajo.find_element(By.XPATH, ".//span/h3").text.strip()
            except NoSuchElementException:
                empresa = "No disponible"
            
            try:
                ubicacion = trabajo.find_element(By.XPATH, ".//*[@aria-label='Ubicación']/following-sibling::*/h3").text.strip()
            except NoSuchElementException:
                ubicacion = "No disponible"

            try:
                modalidad = trabajo.find_element(By.XPATH, ".//*[@aria-label='Modalidad']/following-sibling::*/h3").text.strip()
            except NoSuchElementException:
                modalidad = "No disponible"

            accesibilidad = "Si"
            vacantes = "Disponible"
            #categoria = "Comercial, Ventas y Negocios"
            #categoria = "Administración, Contabilidad y Finanzas"
            #categoria = "Tecnología, Sistemas y Telecomunicaciones"
            #categoria = "Atención al Cliente, Call Center y Telemarketing"
            #categoria = "Abastecimiento y Logística"
            #categoria = "Oficios y Otros"
            #categoria = "Producción y Manufactura"
            #categoria = "Ingenierías"
            #categoria = "Minería, Petróleo y Gas"
            #categoria = "Recursos Humanos y Capacitación"
            #categoria = "Ingeniería Civil y Construcción"
            #categoria = "Marketing y Publicidad"
            #categoria = "Salud, Medicina y Farmacia"
            categoria = "Gastronomía y Turismo"
            #categoria = "Educación, Docencia e Investigación"
            #categoria = "Legales"
            #categoria = "Diseño"
            #categoria = "Comunicación, Relaciones Institucionales y Públicas"
            #categoria = "Secretarias y Recepción"
            #categoria = "Aduana y Comercio Exterior"
            #categoria = "Seguros"
            #categoria = "Departamento Tecnico"
            #categoria = "Sociología / Trabajo Social"
            #categoria = "Naviero, Maritimo, Portuario"
            #categoria = "Enfermería"
            #categoria = "Gerencia y Dirección General"

            try:
                link_postulacion = trabajo.get_attribute('href')
            except Exception:
                link_postulacion = "No disponible"

            try:
                descripcion = trabajo.find_element(By.XPATH, ".//span[@aria-hidden='true']/p").text.strip()
            except NoSuchElementException:
                descripcion = "No disponible"

            if descripcion == "No disponible" and link_postulacion != "No disponible":
                try:
                    driver.execute_script("window.open(arguments[0], '_blank');", link_postulacion)
                    driver.switch_to.window(driver.window_handles[1])
                    
                    wait_detail = WebDriverWait(driver, 5)
                    desc_element = wait_detail.until(EC.presence_of_element_located((By.ID, "descripcion-aviso")))
                    descripcion = desc_element.text.strip()
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except Exception:
                    if len(driver.window_handles) > 1:
                        driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                
            lista_tabla.append({
                "Puesto": puesto,
                "Empresa": empresa,
                "logo": logo,
                "Descripcion": descripcion,
                "Ubicacion": ubicacion,
                "Modalidad": modalidad,
                "Categoria": categoria,
                "Accesibilidad": accesibilidad,
                "Vacantes": vacantes,
                "Link de Postulacion": link_postulacion,
                "Web de la empresa": web_empresa,
                "Fecha de expiracion": fecha_expiracion,
            })
            
        if lista_tabla:
            valores_insertar = [[d["Puesto"], d["Empresa"], d["logo"], d["Descripcion"], d["Ubicacion"], d["Modalidad"], d["Categoria"], d["Accesibilidad"], d["Vacantes"], d["Link de Postulacion"], d["Web de la empresa"], d["Fecha de expiracion"]] for d in lista_tabla]
            
            try:
                sh.append_rows(valores_insertar)
                print(f"Se insertaron {len(valores_insertar)} registros del lote en Google Sheets.")
            except Exception as e:
                print(f"Error al insertar el lote en Google Sheets: {e}")
            
            datos_totales.extend(lista_tabla)
            lista_tabla = []
    else:
        break

driver.quit()

if datos_totales:
    df = pd.DataFrame(datos_totales)
    nombre_archivo = f"Empleos-Bumeran_{hoy}.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Archivo '{nombre_archivo}' guardado correctamente.")
else:
    print("No se encontraron tablas para guardar.")

print("Scrapping finalizado correctamente.")