from bs4 import BeautifulSoup
import json
import requests

class ProductClassifier:
    @staticmethod
    def classify_product(soup):
        title_element = soup.select_one('span#productTitle')
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            title = "No encontrado"
        
        description_element = soup.select_one('meta[name="description"]')
        if description_element:
            description = description_element.get('content', '').lower()
        else:
            description = ""
        
        # Categorías basadas en palabras clave en el título o descripción
        if any(keyword in title.lower() for keyword in ['teléfono', 'smartphone', 'tablet']):
            return 'Tecnología'
        elif any(keyword in title.lower() for keyword in ['zapatos', 'ropa', 'moda', 'vestido']):
            return 'Moda'
        elif any(keyword in title.lower() for keyword in ['hogar', 'casa', 'mueble', 'decoración']):
            return 'Hogar y Cocina'
        elif any(keyword in title.lower() for keyword in ['libro', 'ebook', 'novela', 'literatura']):
            return 'Libros'
        elif any(keyword in description for keyword in ['alimentación', 'comida', 'bebida']):
            return 'Alimentación y Bebidas'
        elif any(keyword in title.lower() for keyword in ['deportes', 'ejercicio', 'fitness', 'gimnasio']):
            return 'Deportes y Aire Libre'
        elif any(keyword in title.lower() for keyword in ['juguete', 'juego', 'muñeca', 'infantil']):
            return 'Juguetes y Juegos'
        else:
            return 'Otro'

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
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clasificar el producto
        category = ProductClassifier.classify_product(soup)
        
        # Inicializar el diccionario de datos con la categoría
        data = {'category': category}

        # Extracción de datos según la categoría
        if category == 'Tecnología':
            data.update(self.extract_technology_info(soup))
        elif category == 'Moda':
            data.update(self.extract_fashion_info(soup))
        elif category == 'Hogar y Cocina':
            data.update(self.extract_home_and_kitchen_info(soup))
        elif category == 'Libros':
            data.update(self.extract_books_info(soup))
        elif category == 'Alimentación y Bebidas':
            data.update(self.extract_food_and_drink_info(soup))
        elif category == 'Deportes y Aire Libre':
            data.update(self.extract_sports_and_outdoors_info(soup))
        elif category == 'Juguetes y Juegos':
            data.update(self.extract_toys_and_games_info(soup))
        else:
            data.update(self.extract_generic_info(soup))
        
        # Guardar los datos recopilados en un archivo JSON
        with open("scraped_data.json", 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("Datos guardados en scraped_data.json")

    # Métodos para la extracción de información específica por categoría
    def extract_technology_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'modelo': self.try_extract_text(soup, 'Nombre del modelo'),
            'software': self.try_extract_text(soup, 'Sistema operativo'),
            'tecnologia_celular': self.try_extract_text(soup, 'Tecnología celular'),
            'capacidad': self.try_extract_text(soup, 'Capacidad de almacenamiento de la memoria'),
            'tecnologia_conectividad': self.try_extract_text(soup, 'Tecnología de conectividad'),
            'color': self.try_extract_text(soup, 'Color'),
            'tamano_pantalla': self.try_extract_text(soup, 'Tamaño de la pantalla'),
            'tipo_conector': self.try_extract_text(soup, 'Tipo de conector'),
            'duracion_bateria': self.try_extract_text(soup, 'Duración de la batería'),
            'resolucion_camara': self.try_extract_text(soup, 'Resolución de la cámara'),
            'tipo_procesador': self.try_extract_text(soup, 'Tipo de procesador'),
        }  
        return {'technology_info': data}

    def extract_fashion_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'material': self.try_extract_text(soup, 'Material'),
            'tamanio': self.try_extract_text(soup, 'Tamaño'),
            'deporte': self.try_extract_text(soup, 'Deporte'),
            'rango_edad': self.try_extract_text(soup, 'Rango de edad (descripción)'),
            'tipo_cierre': self.try_extract_text(soup, 'Tipo de cierre'),
            'estilo_cuello': self.try_extract_text(soup, 'Estilo del cuello'),
            'largo_manga': self.try_extract_text(soup, 'Largo de la manga'),
            'estilo_manga': self.try_extract_text(soup, 'Estilo de la manga'),
            'largo_pantalon': self.try_extract_text(soup, 'Largo del pantalón'),
            'tipo_tejido': self.try_extract_text(soup, 'Tipo de tejido'),
        }
        return {'fashion_info': data}

    def extract_home_and_kitchen_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'dimensiones': self.try_extract_text(soup, 'Dimensiones del producto'),
            'peso': self.try_extract_text(soup, 'Peso del producto'),
            'material': self.try_extract_text(soup, 'Material'),
            'capacidad': self.try_extract_text(soup, 'Capacidad'),
            'color': self.try_extract_text(soup, 'Color'),
            'tipo_superficie': self.try_extract_text(soup, 'Tipo de superficie'),
            'voltaje': self.try_extract_text(soup, 'Voltaje'),
            'potencia': self.try_extract_text(soup, 'Potencia'),
            'incluye_bateria': self.try_extract_text(soup, 'Incluye baterías'),
            'requiere_bateria': self.try_extract_text(soup, 'Requiere baterías'),
            'energia_eficiente': self.try_extract_text(soup, 'Eficiencia energética'),
        }
        return {'home_and_kitchen_info': data}

    def extract_books_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'autor': self.try_extract_text(soup, 'Autor'),
            'editorial': self.try_extract_text(soup, 'Editorial'),
            'formato': self.try_extract_text(soup, 'Formato'),
            'paginas': self.try_extract_text(soup, 'Número de páginas'),
            'idioma': self.try_extract_text(soup, 'Idioma'),
            'genero': self.try_extract_text(soup, 'Género'),
            'dimensiones': self.try_extract_text(soup, 'Dimensiones del producto'),
            'peso': self.try_extract_text(soup, 'Peso del producto'),
            'fecha_publicacion': self.try_extract_text(soup, 'Fecha de publicación'),
        }
        return {'books_info': data}

    def extract_food_and_drink_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'peso_neto': self.try_extract_text(soup, 'Peso neto'),
            'ingredientes': self.try_extract_text(soup, 'Ingredientes'),
            'origen': self.try_extract_text(soup, 'Origen'),
            'unidad_medida': self.try_extract_text(soup, 'Unidad de medida'),
            'fecha_vencimiento': self.try_extract_text(soup, 'Fecha de vencimiento'),
            'instrucciones_alergenos': self.try_extract_text(soup, 'Instrucciones de alergenos'),
            'conservacion': self.try_extract_text(soup, 'Instrucciones de conservación'),
        }
        return {'food_and_drink_info': data}

    def extract_sports_and_outdoors_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'tipo': self.try_extract_text(soup, 'Tipo de deporte'),
            'material': self.try_extract_text(soup, 'Material'),
            'dimensiones': self.try_extract_text(soup, 'Dimensiones del producto'),
            'edad_recomendada': self.try_extract_text(soup, 'Edad recomendada'),
            'color': self.try_extract_text(soup, 'Color'),
            'talla': self.try_extract_text(soup, 'Talla'),
            'genero': self.try_extract_text(soup, 'Género'),
            'estilo': self.try_extract_text(soup, 'Estilo'),
            'temporada': self.try_extract_text(soup, 'Temporada'),
        }
        return {'sports_and_outdoors_info': data}

    def extract_toys_and_games_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'edad_recomendada': self.try_extract_text(soup, 'Edad recomendada'),
            'material': self.try_extract_text(soup, 'Material'),
            'dimensiones': self.try_extract_text(soup, 'Dimensiones del paquete'),
            'genero': self.try_extract_text(soup, 'Género'),
            'numero_modelo': self.try_extract_text(soup, 'Número de modelo'),
            'requiere_baterias': self.try_extract_text(soup, 'Requiere baterías'),
            'incluye_baterias': self.try_extract_text(soup, 'Incluye baterías'),
            'numero_piezas': self.try_extract_text(soup, 'Número de piezas'),
            'instrucciones_cuidado': self.try_extract_text(soup, 'Instrucciones de cuidado'),
        }
        return {'toys_and_games_info': data}

    def extract_generic_info(self, soup):
        data = {
            'product_name': self.general_extract(soup, 'span#productTitle'),
            'rating': self.general_extract(soup, 'span.a-size-base.a-color-base'),
            'rating_count': self.general_extract(soup, 'span#acrCustomerReviewText'),
            'marca': self.try_extract_text(soup, 'Marca'),
            'descripcion': self.try_extract_text(soup, 'Descripción'),
            'dimensiones': self.try_extract_text(soup, 'Dimensiones del producto'),
            'peso': self.try_extract_text(soup, 'Peso del producto'),
            'material': self.try_extract_text(soup, 'Material'),
            'color': self.try_extract_text(soup, 'Color'),
            'otras_caracteristicas': self.try_extract_text(soup, 'Otras características'),
            'detalles_adicionales': self.try_extract_text(soup, 'Detalles adicionales'),
        }
        return {'generic_info': data}

# Uso de la clase Scrapper
url = 'https://www.amazon.com.mx/10-pulgadas-expandible-capacitivo-Bluetooth-certificación/dp/B0CL73D6ZC/?_encoding=UTF8&pd_rd_i=B0CL73D6ZC&pd_rd_w=6ZQzY&content-id=amzn1.sym.b4ded68e-339a-4958-a62e-b1a8cdc78ba9&pf_rd_p=b4ded68e-339a-4958-a62e-b1a8cdc78ba9&pf_rd_r=SHTNG0E3NRGK29EDD21A&pd_rd_wg=QG9zr&pd_rd_r=ad2e22f5-15ee-42b7-a91d-3e7227017533&ref_=oct_dx_dotd'
objeto = Scrapper(url)
objeto.scrape()
