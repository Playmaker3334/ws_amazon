import requests
from bs4 import BeautifulSoup
import time

class TextExtractor:
    """
    Clase diseñada para extraer información de texto específica de HTML utilizando BeautifulSoup.
    """
    @staticmethod
    def try_extract_text(soup, identifier, method='find', tag_type='span', class_name=None, default="No encontrado"):
        try:
            if method == 'find':
                if class_name:
                    element = soup.find(tag_type, class_=class_name)
                else:
                    element = soup.find(tag_type, string=identifier).find_next('td')
            elif method == 'find_all':
                element = soup.find_all(tag_type, string=identifier)[0].find_next('td')
            result = element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            result = default
        return result

class GeneralExtractor:
    """
    Clase para la extracción general de texto de HTML usando selectores CSS con BeautifulSoup.
    """
    @staticmethod
    def general_extract(soup, search_params, default="No encontrado"):
        try:
            element = soup.select_one(search_params) if search_params else None
            result = element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            result = default
        return result

class Scrapper:
    """
    Clase para el scraping de páginas web.
    """
    def __init__(self, url):
        self.url = url

    def scrape_sync(self):
        """
        Realiza el scraping de la página web de manera sincrónica y extrae datos.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'product_name': GeneralExtractor.general_extract(soup, 'span#productTitle'),
            'rating': GeneralExtractor.general_extract(soup, 'span.a-icon-alt'),
            'rating_count': GeneralExtractor.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': TextExtractor.try_extract_text(soup, 'Marca'),
            'modelo': TextExtractor.try_extract_text(soup, 'Nombre del modelo'),
            'software': TextExtractor.try_extract_text(soup, 'Sistema operativo'),
            'tecnologia': TextExtractor.try_extract_text(soup, 'Tecnología celular'),
            'capacidad': TextExtractor.try_extract_text(soup, 'Capacidad de almacenamiento de la memoria'),
            'Tamano': TextExtractor.try_extract_text(soup, 'Tamaño de la pantalla'),
            'tejido': TextExtractor.try_extract_text(soup, 'Tipo de tejido', default="Tipo de tejido no encontrado"),
            'washing': TextExtractor.try_extract_text(soup, 'Instrucciones de cuidado del material', default="Instrucciones de cuidado del material no encontrado"),
            'zipper': TextExtractor.try_extract_text(soup, 'Tipo de cierre', default="Tipo de cierre no encontrado"),
            'manga': TextExtractor.try_extract_text(soup, 'Tipo de manga', default="Tipo de manga no encontrado"),
            'neck': TextExtractor.try_extract_text(soup, 'Estilo de cuello', default="Estilo de cuello no encontrado"),
            'fit': TextExtractor.try_extract_text(soup, 'Tipo de ajuste', default="Tipo de ajuste no encontrado")
        }
        return data