import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiofiles
import time

class TextExtractor:
    """
    A utility class designed to extract specific text information from HTML using BeautifulSoup.
    This class employs static methods to allow direct calling without instantiation.

    Attributes:
        None

    Methods:
        try_extract_text(soup, identifier, method='find', tag_type='span', class_name=None, default="No encontrado"):
            Extracts text based on various search parameters and returns the text or a default value if not found.
    """
    @staticmethod
    def try_extract_text(soup, identifier, method='find', tag_type='span', class_name=None, default="No encontrado"):
        """
        Attempts to extract text from a BeautifulSoup object based on specified criteria.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object to search through.
            identifier (str): The identifier used to locate the target element. This could be a string for text search or a class name.
            method (str): The method to use for searching ('find' or 'find_all').
            tag_type (str): The type of HTML tag to search for (e.g., 'span', 'div').
            class_name (str): The class name of the tag to find. Optional and used only if specified.
            default (str): The default text to return if the search fails to find the target element.

        Returns:
            str: The extracted text or the default value if the target element is not found.
        """
        extract_start_time = time.time()
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
        print(f"Extraction time for {identifier}: {time.time() - extract_start_time:.2f} seconds")
        return result

class GeneralExtractor:
    """
    A utility class for general text extraction from HTML using CSS selectors with BeautifulSoup.

    Attributes:
        None

    Methods:
        general_extract(soup, search_params, default="No encontrado"):
            Extracts text using a CSS selector and returns it or a default value if not found.
    """
    @staticmethod
    def general_extract(soup, search_params, default="No encontrado"):
        """
        Extracts text from a BeautifulSoup object using CSS selectors.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object to search through.
            search_params (str): The CSS selector to use for finding the target element.
            default (str): The default text to return if the search fails to find the target element.

        Returns:
            str: The extracted text or the default value if the target element is not found.
        """
        extract_start_time = time.time()
        try:
            element = soup.select_one(search_params) if search_params else None
            result = element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            result = default
        print(f"Extraction time for {search_params}: {time.time() - extract_start_time:.2f} seconds")
        return result

class Scrapper:
    """
    A class for scraping web pages synchronously and saving extracted data asynchronously.

    Attributes:
        url (str): The URL of the web page to scrape.

    Methods:
        scrape_sync(): Performs the web scraping synchronously and triggers asynchronous saving of data.
        save_data_async(data): Asynchronously saves extracted data to a file.
    """
    def __init__(self, url):
        """
        Initializes the Scrapper with a URL.

        Parameters:
            url (str): The URL of the web page to scrape.
        """
        self.url = url

    def scrape_sync(self):
        """
        Scrapes the web page synchronously, extracts data, and saves it asynchronously.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        start_time = time.time()
        response = requests.get(self.url)
        print(f"HTTP request time: {time.time() - start_time:.2f} seconds")

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

        asyncio.run(self.save_data_async([data]))
        print(f"Total Execution Time: {time.time() - start_time:.2f} seconds")
        return data

    async def save_data_async(self, data):
        """
        Asynchronously saves extracted data to a JSON file.

        Parameters:
            data (list): A list of dictionaries containing the extracted data.
        """
        save_start_time = time.time()
        async with aiofiles.open("scraped_data_async.json", 'w', encoding='utf-8') as outfile:
            await outfile.write(json.dumps(data, ensure_ascii=False, indent=4))
        print(f"Save to file time: {time.time() - save_start_time:.2f} seconds")

# URL of the web page to scrape
url = 'https://www.amazon.com.mx/HP-procesador-i5-1135G7-generaci%C3%B3n-Bluetooth/dp/B09LM6SZKG/ref=sr_1_7?crid=KWKTKN6OPHQS&dib=eyJ2IjoiMSJ9.mvJh-CBqHpJNE0St7UH7lB1R5FvbR0R_Yrw5mXgh-4T4NU04zHRiRsb-j5Y6C5mpLdQrfXuUlZbuWokHB5SdgWNKO7LHW1HJsRtqeEXsQAFyX8VJqqg0snSule9rS5vELSccOFVP9tEVV_k2O0p9S_ztOiivc_9R0BtmxcnfiJAqy_xm_PLLcXFxdKwDdyfGBI3oiZ1F4uu0k6quPhvgeALqm6paaUFPtP4RMEu4JYRq9r89UmTCLHYRkSc3zxV7Z9ucAbDXpABpVEQLn4BPyiUYEjYst_WjzcvqL6w_QV4.7jQbxscJZcHexwAPa9uaDwxU9r6l3h3UZeJXTgkgm0U&dib_tag=se&keywords=laptops&qid=1708739984&s=electronics&sprefix=%2Celectronics%2C115&sr=1-7&ufe=app_do%3Aamzn1.fos.628a2120-cf12-4882-b7cf-30e681beb181'
# Instance of Scrapper with the specified URL
scrapper = Scrapper(url)
# Execute the scrape_sync method to scrape the web page and save data
scrapper.scrape_sync()

