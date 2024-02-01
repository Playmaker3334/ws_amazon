import pandas as pd
import random
import time
import requests
from bs4 import BeautifulSoup

# Lista de identificaciones de navegador para simular accesos como distintos usuarios
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
    # Más identificaciones de navegador pueden ser añadidas aquí
]

# Palabra clave para la búsqueda en Amazon
search_query = 'Celulares'.replace(' ', '+')
base_url = 'https://www.amazon.com.mx/s?k={0}'.format(search_query)
items = []
cache = {}  # Almacenamiento temporal para evitar repetir descargas de la misma página

# Bucle para recorrer varias páginas de resultados
for i in range(1, 21):
    page_url = base_url + '&page={0}'.format(i)
    
    # Verifica si la página ya fue descargada previamente y almacenada en el caché
    if page_url in cache:
        soup = BeautifulSoup(cache[page_url], 'html.parser')
    else:
        # Configuración de encabezados para la solicitud, incluyendo una identificación de navegador aleatoria
        headers = {"User-Agent": random.choice(user_agents), "Accept-Language": "en-MX, en;q=0.9"} # Cosas turbias
        print('Procesando {0}...'.format(page_url))
        response = requests.get(page_url, headers=headers)
        cache[page_url] = response.content  # Guardar la respuesta en caché
        soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer datos de cada producto encontrado en la página
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text
        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find('span', {'class': 'a-size-base'}).text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float((price1 + price2).replace(',', ''))
            product_url = 'https://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue

    # Espera un tiempo aleatorio entre 1 y 3 segundos antes de procesar la siguiente página
    time.sleep(random.uniform(1, 3))

# Crear un DataFrame de pandas con la información recopilada
df = pd.DataFrame(items, columns=['product', 'rating', 'rating_count', 'price', 'product_url'])
# Guardar el DataFrame en un archivo CSV (Estoy viendo como modificarlo xd)
df.to_csv('Celulares.csv')
