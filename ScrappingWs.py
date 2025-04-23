from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

url = "https://www.detonashop.com.br/camera-sony-zv-e10-ii-mirrorless-corpo-branca.html"
topico_ntfy = "monitor-zv-e10"  # Nome do canal ntfy
preco_alerta = 8000  # Preço de alerta

opcoes = Options()
opcoes.add_argument("--headless=new")
opcoes.add_argument("--no-sandbox")
opcoes.add_argument("--disable-dev-shm-usage")
opcoes.add_argument("--disable-gpu")
opcoes.add_argument("--disable-extensions")
opcoes.add_argument("--window-size=1920,1080")
opcoes.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)

driver.get(url)
time.sleep(4)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

nome_produto = soup.find("h1", class_="page-title").get_text().strip()
preco_produto = soup.find("span", class_="price").get_text().strip()
preco_produto_Avista = soup.find("span", class_="preco-com-desconto").get_text().strip()

preco_produto = float(preco_produto.replace("R$", "").replace(" ", "").replace(".", "").replace(",", "."))
preco_produto_Avista = float(preco_produto_Avista.replace("R$", "").replace(" ", "").replace(".", "").replace(",", "."))

mensagem = f"Preço do produto {nome_produto} está abaixo de {preco_alerta}"

if preco_produto_Avista <= preco_alerta:
    requests.post(f"https://ntfy.sh/{topico_ntfy}", data=mensagem.encode(encoding="utf-8"))
else:
    requests.post(f"https://ntfy.sh/{topico_ntfy}", data=f"🔍 Monitorando...\n{mensagem}".encode('utf-8'))