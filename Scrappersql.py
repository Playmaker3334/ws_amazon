import pandas as pd
import random
import time
import requests
import sqlite3
from bs4 import BeautifulSoup

# Establecer conexión con la base de datos SQLite
conn = sqlite3.connect('productos.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS productos
             (product TEXT, rating TEXT, rating_count TEXT, price REAL, product_url TEXT)''')

# Lista de identificaciones de navegador para simular distintos usuarios
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
]

# Palabra clave para la búsqueda en Amazon
search_query = 'Celulares'.replace(' ', '+')
base_url = f'https://www.amazon.com.mx/s?k={search_query}'

# Almacenamiento temporal para respuestas
cache = {}

# Recorrer páginas de resultados
for i in range(1, 21):
    page_url = f'{base_url}&page={i}'

    if page_url in cache:
        soup = BeautifulSoup(cache[page_url], 'html.parser')
    else:
        headers = {"User-Agent": random.choice(user_agents), "Accept-Language": "en-MX, en;q=0.9"}
        print(f'Procesando {page_url}...')
        response = requests.get(page_url, headers=headers)
        cache[page_url] = response.content
        soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        try:
            product_name = result.h2.text
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find('span', {'class': 'a-size-base'}).text
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float((price1 + price2).replace(',', ''))
            product_url = 'https://amazon.com' + result.h2.a['href']
            c.execute("INSERT INTO productos VALUES (?, ?, ?, ?, ?)",
                      (product_name, rating, rating_count, price, product_url))
        except AttributeError:
            continue

    time.sleep(random.uniform(1, 3))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()
