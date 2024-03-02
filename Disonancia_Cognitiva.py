from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import csv
import random
import time
from Robertdeniro import Scrapper  # Importa tu clase Scrapper aquí

# Configuración de Selenium para minimizar detección
edge_options = Options()
edge_options.use_chromium = True
edge_options.add_argument("start-maximized")  # Maximizar ventana
edge_options.add_argument("disable-blink-features=AutomationControlled")  # Evitar que la página detecte el control por automatización
edge_options.add_argument("--disable-extensions")  # Desactivar extensiones
edge_options.add_argument('--no-sandbox')  # Desactivar sandbox (útil para sistemas Linux)
edge_options.add_argument('--disable-dev-shm-usage')  # Evitar el uso de /dev/shm temporal
# Opcional: configurar un user-agent personalizado (puedes obtener uno de tu navegador)
# edge_options.add_argument("user-agent=YOUR_USER_AGENT_HERE")

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

search_query = 'Celulares'.replace(' ', '+')
base_url = f'https://www.amazon.com.mx/s?k={search_query}'

# Preparar archivo CSV para escritura
with open('productos.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Escribir fila de encabezados
    writer.writerow(['product', 'rating', 'rating_count', 'price', 'product_url', 'marca', 'modelo', 'software', 'tecnologia', 'capacidad', 'Tamano'])

    for i in range(1, 3):  # Reducido para demostración
        page_url = f'{base_url}&page={i}'
        print(f'Procesando {page_url}...')
        driver.get(page_url)
        time.sleep(random.uniform(5, 10))  # Espera aleatoria para simular actividad humana
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for result in results:
            product_url = 'https://www.amazon.com.mx' + result.h2.a['href']
            scrapper = Scrapper(product_url)  # Instanciar Scrapper para la URL del producto
            product_data = scrapper.scrape_sync()  # Extraer datos del producto con Scrapper

            # Escribir datos del producto en el archivo CSV
            writer.writerow([
                product_data['product_name'], product_data['rating'], product_data['rating_count'],
                product_data.get('price', 0.0), product_url, product_data.get('marca', ''),
                product_data.get('modelo', ''), product_data.get('software', ''),
                product_data.get('tecnologia', ''), product_data.get('capacidad', ''), product_data.get('Tamano', '')
            ])

driver.quit()


