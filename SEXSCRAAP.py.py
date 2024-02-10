from bs4 import BeautifulSoup
import json
import requests

class Scrapper:
    """
    A class for scraping data from specific web pages.

    Attributes:
    ----------
    urls : list
        A list of URLs of the web pages to scrape.

    Methods:
    --------
    try_extract_text(soup, identifier, method='find', tag_type='span', class_name=None, default="Not found"):
        Attempts to extract text based on identifiers and returns a default text if not found.
    
    general_extract(soup, search_params, default="Not found"):
        Extracts text in a general manner based on CSS search parameters.

    scrape():
        Performs the scraping of the provided URLs and saves the extracted data in JSON files.
    """

    def __init__(self, urls):
        """
        Initializes the Scrapper class with a list of URLs.

        Parameters:
        -----------
        urls : list
            List of URLs to scrape.
        """
        self.urls = urls

    def try_extract_text(self, soup, identifier, method='find', tag_type='span', class_name=None, default="Not found"):
        """
        Attempts to extract text from a BeautifulSoup object based on specific criteria.

        Parameters:
        -----------
        soup : BeautifulSoup
            BeautifulSoup object of the current page.
        identifier : str
            Identifier to find the element (can be text or class name).
        method : str, optional
            BeautifulSoup method to use ('find' or 'find_all').
        tag_type : str, optional
            Type of HTML tag to search for.
        class_name : str, optional
            Class name of the element to search for.
        default : str, optional
            Default text if the element is not found.

        Returns:
        --------
        str
            Extracted text or default text.
        """
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

    def general_extract(self, soup, search_params, default="Not found"):
        """
        Extracts information in a general manner using CSS search parameters.

        Parameters:
        -----------
        soup : BeautifulSoup
            BeautifulSoup object of the current page.
        search_params : str
            CSS search parameters to select the desired element.
        default : str, optional
            Default text if the element is not found.

        Returns:
        --------
        str
            Extracted text or default text.
        """
        try:
            element = soup.select_one(search_params) if search_params else None
            return element.get_text(strip=True) if element else default
        except (AttributeError, IndexError):
            return default

    def scrape(self):
        """
        Performs the scraping of the provided URLs and saves the data in JSON files.

        This method navigates through each URL, extracts specific product information, and
        saves the extracted data into JSON files, one for each URL.
        """
        for url in self.urls:
            data = {}
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Data extraction using extraction functions
            data['product_name'] = self.general_extract(soup, 'span#productTitle')
            data['rating'] = self.general_extract(soup, 'span.a-size-base.a-color-base')
            data['rating_count'] = self.general_extract(soup, 'span#acrCustomerReviewText')
            data['brand'] = self.try_extract_text(soup, 'Marca')
            data['model'] = self.try_extract_text(soup, 'Nombre del modelo')
            data['software'] = self.try_extract_text(soup, 'Sistema operativo')
            data['technology'] = self.try_extract_text(soup, 'Tecnología celular')
            data['storage_capacity'] = self.try_extract_text(soup, 'Capacidad de almacenamiento de la memoria')
            data['screen_size'] = self.try_extract_text(soup, 'Tamaño de la pantalla')

            # New elements to extract with error handling
            fields = [
                ('Tipo de tejido', 'fabric_type'),
                ('Instrucciones de cuidado del material', 'care_instructions'),
                ('Tipo de cierre', 'closure_type'),
                ('Tipo de manga', 'sleeve_type'),
                ('Estilo de cuello', 'collar_style'),
                ('Tipo de ajuste', 'fit_type')
            ]

            for field_name, field_key in fields:
                try:
                    row = soup.find('span', string=field_name).find_parent('div', {'class': 'a-fixed-left-grid-inner'})
                    data[field_key] = row.find('div', class_='a-fixed-left-grid-col a-col-right').get_text(strip=True) if row else f"{field_name} not found"
                except AttributeError:
                    data[field_key] = f"{field_name} not found"
            
            # Generate a unique filename for each URL
            filename = "scraped_data_" + url.split('/')[-1].split('?')[0] + ".json"
            
            # Save the data in a unique JSON file for each URL
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump([data], json_file, indent=4, ensure_ascii=False)
            print(f"Data saved in {filename}")

# Usage of the Scrapper class with multiple URLs
urls = [
    'https://www.amazon.com.mx/Xiaomi-Smartphone-Poco-Mediatek-Android/dp/B0C5KDVKKP',
    'https://www.amazon.com.mx/Nautica-Wrinkle-Resistant-Sleeve-Shoreline/dp/B07BN565V5',
    'https://www.amazon.com.mx/Reloj-GUESS-Hombres-pulsera-Inoxidable/dp/B00V49K740/ref=sr_1_1?crid=2KU8BHAOKF2HV&keywords=reloj&qid=1707530721&sprefix=re%2Caps%2C126&sr=8-1&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47'
]

scraper = Scrapper(urls)
scraper.scrape()




