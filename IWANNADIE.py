from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import mysql.connector
import random
import time

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='n1n2n0qslaSH',  
    database='products_aws'   
)
c = conn.cursor()

# Configuración de Selenium para usar Edge
edge_options = Options()
edge_options.use_chromium = True


edge_options.add_argument("start-maximized")
edge_options.add_argument("disable-infobars")
edge_options.add_argument("--disable-extensions")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--no-sandbox")
service = Service(EdgeChromiumDriverManager().install())

# Iniciar el navegador Edge con las opciones configuradas
driver = webdriver.Edge(service=service, options=edge_options)

# Lista de identificaciones de navegador para simular distintos usuarios
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
]

# Palabra clave para la búsqueda en Amazon
search_query = 'Celulares'.replace(' ', '+')
base_url = f'https://www.amazon.com.mx/s?k={search_query}'

# Recorrer páginas de resultados con Selenium
for i in range(1, 10):
    page_url = f'{base_url}&page={i}'
    print(f'Procesando {page_url}...')
    driver.get(page_url)

    # Espera para que la página cargue. Puedes ajustar el tiempo según sea necesario.
    time.sleep(random.uniform(5, 10))

    # Obtener el contenido de la página y procesarlo con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    for result in results:
        try:
            product_name = result.h2.text.strip()
            rating = result.find('i', {'class': 'a-icon'}).text.strip() if result.find('i', {'class': 'a-icon'}) else 'N/A'
            rating_count = result.find('span', {'class': 'a-size-base'}).text.strip() if result.find('span', {'class': 'a-size-base'}) else '0'
            price_whole = result.find('span', {'class': 'a-price-whole'})
            price_fraction = result.find('span', {'class': 'a-price-fraction'})

            if price_whole and price_fraction:
                price = float(price_whole.text.replace(',', '').replace('.', '') + '.' + price_fraction.text)
            else:
                price = 0.0  # O un valor predeterminado si no se encuentra el precio

            product_url = 'https://www.amazon.com.mx' + result.h2.a['href']

            c.execute("INSERT INTO products_aws (product, rating, rating_count, price, product_url) VALUES (%s, %s, %s, %s, %s)",
                      (product_name, rating, rating_count, price, product_url))
        except AttributeError as e:
            print(f'Error al extraer datos del resultado: {e}')
        except ValueError as e:
            print(f'Error al convertir el precio: {e}')
        except mysql.connector.Error as err:
            print(f"Error en SQL: {err}")
            conn.rollback()

    time.sleep(random.uniform(1, 3))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

# Cerrar el navegador al finalizar
driver.quit()

