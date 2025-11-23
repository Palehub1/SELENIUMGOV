from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
import os # <-- ¡NUEVA IMPORTACIÓN NECESARIA!

SEARCH = 'Morbilidad atendida en salud mental en Bogotá D.C'
SEARCH_SELECTOR = (By.CSS_SELECTOR, 'input[placeholder="Buscar"]')

# Selector ROBUSTO para el enlace de la BD (Busca por texto)
BD_SELECTOR = (By.XPATH, "//a[contains(text(), 'Morbilidad atendida en salud mental')]") 
BD_HREF = 'https://www.datos.gov.co/d/ic2q-68qq'

# Selector y URL del botón de descarga final
DOWNLOAD_HREF = 'https://datosabiertos.bogota.gov.co/dataset/aaf76e31-6a9b-402b-8e87-6b8e61c91265/resource/b1f29caa-b7a3-46a2-837a-ff0959f80f01/download/osb_salud-mental_morbilidad.csv'
DOWNLOAD_SELECTOR = (By.CSS_SELECTOR, f'a[href="{DOWNLOAD_HREF}"]') 


def main():
  
    download_dir = os.path.join(os.getcwd(), "descargas_csv")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir) 
    print(f"Los archivos se guardarán en: {download_dir}")
    
    prefs = {
        "download.default_directory": download_dir, 
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True # Evita que abra en una nueva pestaña
    }

    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_experimental_option("prefs", prefs)
    option.add_argument("--window-size=1024,720")
    
    driver = Chrome(service=service, options=option)
    driver.get("https://www.datos.gov.co/")
    

    try:
        # Pasos 2, 3, 4: Búsqueda y Enter
        Wait(driver, 15).until(EC.visibility_of_element_located(SEARCH_SELECTOR))
        user_input = driver.find_element(*SEARCH_SELECTOR)
        user_input.send_keys(SEARCH)
        user_input.send_keys(Keys.ENTER)
        print("Búsqueda ejecutada.")
        
        # Paso 5: Espera la carga de la página de resultados
        Wait(driver, 15).until(EC.url_contains("q=")) 
        print("Página de resultados cargada.")
        
        # Paso 6: Clic en el enlace de la BD
        Wait(driver, 15).until(EC.visibility_of_element_located(BD_SELECTOR))
        enlace_bd = driver.find_element(*BD_SELECTOR)
        enlace_bd.click() 
        print("Clic en el enlace de la base de datos.")
        
        # Paso 7: Espera a que la página de destino cargue el botón de descarga
        print("Esperando a que el botón de descarga sea visible...")
        Wait(driver, 30).until(
            EC.visibility_of_element_located(DOWNLOAD_SELECTOR)
        )
        print("Página de la BD cargada con éxito.")
        
        # Paso 8: Haz clic en el botón de descarga (Debería funcionar ahora)
        download_button = driver.find_element(*DOWNLOAD_SELECTOR)
        download_button.click()
        print("Clic en el botón de descarga CSV.")
        
        # Espera un momento para que la descarga comience
        time.sleep(60) 
        
    except Exception as e:
        print(f"\n❌ ERROR: Fallo en la navegación o interacción. Detalle: {e}", file=sys.stderr)
        
    finally:
        print("Cerrando navegador...")
        driver.quit()

if __name__== "__main__":
    main()