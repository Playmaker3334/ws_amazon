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

- `docker-compose build`
- `docker-compose up`

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

