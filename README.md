# Amazon Web Scraper

## Project description

This project offers a robust and user-friendly solution for web data extraction, specifically designed to overcome the common challenges of online information collection. By combining the power of Python, Flask, and Docker, this web scraper is capable of efficiently processing and extracting data from complex websites like Amazon, providing a superior alternative to traditional scraping tools thanks to its modular and scalable approach. It is ideal for market researchers, price comparison app developers, and anyone interested in web data mining.

## Requeriments

### Hardware

- CPU: 2 GHz dual-core or higher
- Memoria: At least 4 GB RAM
- Disk Space: At least 10 GB of free space

### Software

- Operating System: Windows 10/11, MacOS X, Linux
- Docker: Latest version (see Docker Documentation for specific installation instructions)

## Tools
- pandas
- requests
- beautifulsoup4
- flask
- asyncio
- aiofiles
- Docker
- postman
- vsCode
- Github

## Installation Guide

### Preparations

1. **Docker instalation**
   - Visit Docker Documentation and follow the specific instructions for your operating system.

2. **Repository Cloning:**
   - If you are new to Git, install Git following the instructions in the Git Installation Guide.
   - Open your terminal and execute:
   - `git clone https://github.com/Playmaker3334/ws_amazon.git`
   - `cd ws_amazon`

### Building and Running with Docker

- `docker-compose up --build`
- We just need to run this command which will activate the dockerfile and do the creation of everything else.


This starts the application on http://localhost:6000.

## Improvements in the Usage Section

To interact with the /scrap endpoint, you can use tools like curl or Postman:

- **With Curl:**
  curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.amazon.com.mx/..."}' http://localhost:6000/scrap

- **With Postman:**
  - Método: POST
  - URL: http://localhost:6000/scrap
  - Body: raw JSON
    {
      "url": "https://www.amazon.com.mx/..."
    }

## Different links
Here are different examples where the scrapper can be used

- Phone
`https://www.amazon.com.mx/Xiaomi-Celular-Redmi-13C-Midnight/dp/B0CLM9X2PP/ref=sr_1_1_sspa?crid=1BPG07FEF13S&dib=eyJ2IjoiMSJ9.Ur5lUKiD0aguIHKaZfIKfM4kJ7C-E2odEiT-WFqKeYPBnfxW1dn4SZKucbx0icEpTtugMc1Mc7VHWE55iA9-lLFgmIheDWvPlp0GjNRdh13ajLQDDIC_Ai-MQ-yMfEvuzjAGbCywUq2-FGa3-N1H3qdqsHBprWuagBaWKVBPZJG0bDsCluYpVyLNZHUeXAKWFKKed92lTIJo9cN3cj7XKpwv01R_z_pJpCSwwNR0dhwjTT7TROZ-mMhr9z13Lv-anPam1fKTqDVGs0DVpphnz5R9VJalq5OFQb2s7r_LH1Y.mBXI-6unZ7OnDUaGvoyGNxEpKnvUOkXWbE91AoIId8Y&dib_tag=se&keywords=celulares&qid=1709009202&sprefix=%2Caps%2C103&sr=8-1-spons&ufe=app_do%3Aamzn1.fos.628a2120-cf12-4882-b7cf-30e681beb181&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1`

- Laptop gamer
`https://www.amazon.com.mx/MSI-12450H-NVIDIA-GeForce-Laptop/dp/B0CNB9NW4C/ref=sr_1_2?crid=33HU0IOZJ3BR2&dib=eyJ2IjoiMSJ9.XJfUJvLr1LDbzIWVpqvV3wAVlpwyvjot8xkP0YoxeZtlRWc4XDWMmiTi-2VXx2b1kMWjCKPF654yPB4nkm-zEvLIgvrhxX8vzYETKdZus76M_bTVxo5PwjTMZIowfTAUmzRb86zwdTDx8bsdEUcEa27qu5TqCj4i_pnhD7t8NOLdrf5RJPlIi9ufKUXD6rWSshGDZKOl_p6ew-hqZhbRjp9RCfH3ezYYWukOtMO3_QJ-viO1hFb_maS8_5QnNg2l9-cC97epKxljt14gboEJJxCuSxruGOYE8qwUNrrHvic.NQOaci-jbz7XKVI-Pdq6Yjx4P-bl-gSEW8Jl7TXkKMY&dib_tag=se&keywords=laptop+gamer&qid=1709009291&sprefix=laptop%2Caps%2C15&sr=8-2&ufe=app_do%3Aamzn1.fos.8c7b929b-80a3-4a0f-851f-6de37ce634c2`

You just have to modify the link in the variable called url of the scrapper's code and it will give you a json with multiple fields that will be filled depending on the object you scrape, the json will be sent to the users directory if you use windows and if you use LinuxGOD in the same directory of your scrapper.

## Contribution Details

To contribute to the project, please follow these steps:


1. Fork the repository.
2. Create a new branch for your feature or correction.
3. Make your changes.
4. Submit a pull request with a detailed description of your changes.

## Current Contributors
- KRISHNA SANDOVAL CAMBRANIS
- JOAQUIN DE JESUS MURGUIA ORTIZ
- PEDRO ADOLFO AVILA COLLI
- ROGELIO HERBERT NOVELO ZAPATA



##  Contact Information

For questions or collaborations, please contact jikjfeippk123@gmail.com.

## License

This project is licensed under the MIT License, allowing wide latitude for personal and commercial use. A license summary includes permission to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.

