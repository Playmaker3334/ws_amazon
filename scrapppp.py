from bs4 import BeautifulSoup
import json
import requests

class Scrapper:
    def __init__(self, url):
        self.url = url

    def try_extract_text(self, soup, identifier, method='find', tag_type='span', class_name=None, default="No encontrado"):
        try:
            if method == 'find':
                if class_name:
                    element = soup.find(tag_type, class_=class_name)
                else:
                    element = soup.find(tag_type, string=identifier).find_next('td')
            elif method == 'find_all':
                element = soup.find_all(tag_type, string=identifier)[0].find_next('td')
            return element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            return default

    def general_extract(self, soup, search_params, default="No encontrado"):
        try:
            element = soup.select_one(search_params) if search_params else None
            return element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            return default

    def scrape(self):
        data = {}
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracción de datos usando las funciones de extracción
        data['product_name'] = self.general_extract(soup, 'span#productTitle')
        data['rating'] = self.general_extract(soup, 'span.a-size-base.a-color-base')
        data['rating_count'] = self.general_extract(soup, 'span#acrCustomerReviewText')
        data['marca'] = self.try_extract_text(soup, 'Marca')
        data['modelo'] = self.try_extract_text(soup, 'Nombre del modelo')
        data['software'] = self.try_extract_text(soup, 'Sistema operativo')
        data['tecnologia'] = self.try_extract_text(soup, 'Tecnología celular')
        data['capacidad'] = self.try_extract_text(soup, 'Capacidad de almacenamiento de la memoria')
        data['Tamano'] = self.try_extract_text(soup, 'Tamaño de la pantalla')

        # Nuevos elementos a extraer con manejo de errores
        fields = [
            ('Tipo de tejido', 'tejido'),
            ('Instrucciones de cuidado del material', 'washing'),
            ('Tipo de cierre', 'zipper'),
            ('Tipo de manga', 'manga'),
            ('Material', 'material'),
            ('País de origen', 'Pais de origen'),
            ('Forma del producto', 'Forma del producto'),
            ('Tecnología de conectividad', 'Tipo de conexion'),
            ('Fragancia', 'Fragancia'),
            ('Tipo de piel', 'Tipo de piel '),
            ('Componentes incluidos', 'Incluidos')
        ]

        for field_name, field_key in fields:
            try:
                row = soup.find('span', string=field_name).find_parent('div', {'class': 'a-fixed-left-grid-inner'})
                data[field_key] = row.find('div', class_='a-fixed-left-grid-col a-col-right').get_text(strip=True) if row else f"{field_name} no encontrado"
            except AttributeError:
                data[field_key] = f"{field_name} no encontrado"
        
        # Guardar los datos recopilados en un archivo JSON
        with open("scraped_data.json", 'w', encoding='utf-8') as json_file:
            json.dump([data], json_file, indent=4, ensure_ascii=False)
        print("Datos guardados en scraped_data.json")

# Uso de la clase Scrapper
url = 'https://www.amazon.com.mx/Xiaomi-Smartphone-Poco-Mediatek-Android/dp/B0C5KDVKKP/ref=sr_1_1?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=6F87KX8H27P5&keywords=celulares&qid=1707529365&sprefix=celulares%2Caps%2C163&sr=8-1&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&th=1'
objeto = Scrapper(url)
objeto.scrape()


