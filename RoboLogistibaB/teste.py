import tkinter as tk
import os,pyautogui, time
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import xmltodict
import math
from lxml import etree
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from tkinter import simpledialog    
from CORE import ManipuladorJSONProdutos
from CORE import ControleEstoque
from CORE import NavegadorSelenium
from PIL import Image
import keyboard
import threading
import time

                                
caminho_completo = os.path.join(r"C:\Users\almlc\OneDrive\Área de Trabalho\RoboLogistica\Produtos\Carros\SmartTV32_5", "SmartTV32_5.jpg")
def encontrar_imagem_redimensionada(caminho_imagem_referencia, tamanho_real):
    try:
        # Captura uma captura de tela da tela inteira
        captura_tela = pyautogui.screenshot()

        # Carrega a imagem de referência
        imagem_referencia = Image.open(caminho_imagem_referencia)

        # Redimensiona a imagem de referência para o tamanho real
        imagem_referencia_redimensionada = imagem_referencia.resize(tamanho_real)

        # Tenta encontrar a posição da imagem de referência redimensionada na captura de tela
        localizacao = pyautogui.locate(imagem_referencia_redimensionada, captura_tela)

        return localizacao

    except pyautogui.ImageNotFoundException:
        print(caminho_imagem_referencia)
        return None
# Verifica se o arquivo é uma imagem e se o nome corresponde ao procurado
tamanho_real_da_imagem = (100, 100) 

time.sleep(5)
path = encontrar_imagem_redimensionada(caminho_completo,tamanho_real_da_imagem)
print(path)
