import tkinter as tk
import os,pyautogui, time
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.amazon.com.br/dp/6555478365/ref=s9_acsd_al_bw_c2_x_8_t?pf_rd_m=A1ZZFT5FULY4LN&pf_rd_s=merchandised-search-12&pf_rd_r=HJH38M4ZBX3VWCG3VFRH&pf_rd_t=101&pf_rd_p=928d1fdd-66d3-4932-a5f1-64d96899d32b&pf_rd_i=6740748011"
url2 = "https://www.amazon.com.br/dp/6555478365/ref=s9_acsd_al_bw_c2_x_8_t?pf_rd_m=A1ZZFT5FULY4LN&pf_rd_s=merchandised-search-12&pf_rd_r=HJH38M4ZBX3VWCG3VFRH&pf_rd_t=101&pf_rd_p=928d1fdd-66d3-4932-a5f1-64d96899d32b&pf_rd_i=6740748011"
# Verifica o status da requisição

webpage = requests.get(url2)
if webpage.status_code == 200:
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Encontrando o nome do produto
    nome_produto = soup.find("span", {"id": "productTitle"})
    
    # Verifica se o nome do produto foi encontrado
    if nome_produto:
        resposta = nome_produto.text.strip()[:10]
        print(resposta)
    else:
        print("Nome do produto não encontrado.")
else:
    print(f"Falha na requisição. Status code: {webpage.status_code}")