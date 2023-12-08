import tkinter as tk
import os,pyautogui, time
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import xmltodict
import math
import re
import pyperclip
import json
from lxml import etree
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from tkinter import simpledialog
from selenium.common.exceptions import TimeoutException
from PIL import Image





navegador_selenium = None
modo_teste = False
salvar_dados = True
chrome = True
select_image_dinamico = False
count = 0

#IA
def encontrar_imagem(caminho_imagem):
    try:
        # Captura uma captura de tela da tela inteira
        captura_tela = pyautogui.screenshot()

        # Carrega a imagem de referência
        imagem_referencia = Image.open(caminho_imagem)

        # Tenta encontrar a posição da imagem de referência na captura de tela
        localizacao = pyautogui.locate(imagem_referencia, captura_tela)

        return localizacao

    except pyautogui.ImageNotFoundException:
        # Se a imagem de referência não for encontrada, retorne None ou faça outra ação
        return None

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

def initialize(url):
    global navegador_selenium

    if navegador_selenium is None:
        navegador_selenium = NavegadorSelenium()

    navegador_selenium.abrir_url(url)

    navegador_selenium.maximize_window()

    if chrome:
        pyautogui.moveTo(1895,101,duration=.5)
        pyautogui.click()
        pyautogui.moveTo(87,53,duration=.5)
        pyautogui.click()    
    return navegador_selenium

def obter_informacoes():
    # Cria uma janela
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Pede ao usuário que digite a capacidade
    captcha = simpledialog.askstring("Input", "Digite a capacidade:")


    return captcha
    
def verificar_login():
    root = tk.Tk()
    root.withdraw()

    resultado = messagebox.askyesno("Verificar Login", "Você conseguiu logar?")

    return resultado

def verifiar_tipo_abstecimento():
    # Pede ao usuário que digite o administrador
    result = messagebox.askyesno("Abastecer as Caixas ou Individual", "Abasce por caixas?")
    return result

def logar(administrador, senha, captcha):  
    pyautogui.moveTo(1273,495,duration=.5)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.sleep = .2
    pyautogui.write(administrador)
    pyautogui.moveTo(1273,555,duration=.5)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.sleep = .2
    pyautogui.write(senha)
    pyautogui.moveTo(1239,615,duration=.5)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.sleep = .2
    pyautogui.write(captcha)
    pyautogui.sleep = .2
    pyautogui.moveTo(1279,680,duration=.5)
    pyautogui.click()
    pyautogui.sleep = 1
    
    resultado = verificar_login()
    return resultado

def traduzir():
    pyautogui.moveTo(1738,101,duration=.5)
    time.sleep(1.5)
    pyautogui.moveTo(1708,199,duration=.5)
    pyautogui.click()


def open_store(abastecer_caixa):
    pyautogui.moveTo(33,224,duration=.5)
    pyautogui.click()
    pyautogui.moveTo(127,158,duration=.5)
    pyautogui.click()
    pyautogui.moveTo(383,339,duration=.5)
    pyautogui.click()

    if abastecer_caixa:
        pyautogui.moveTo(597,354,duration=.5)
        pyautogui.click()
    else:
        pyautogui.moveTo(473,360,duration=.5)
        pyautogui.click()    

def iniciar_abstecimento(url_base,pastas_nome,abastecer_caixa):
    global modo_teste
    global count
    manipuladorJson = ManipuladorJSONProdutos()
    

    # Verificar todas as categorias
    for x in range(len(pastas_nome)): 
        #obter todos os produtos
        manipuladorJson.criar_json_produtos(url_base+f"/{pastas_nome[x]}","dados.json")    
        estoque = ControleEstoque(url_base+f"/{pastas_nome[x]}")
       
        pastas = estoque.listar_pastas()

        #Filtrar as pastas que já foram criadas e retornar apenas as novas
        pastas_filtradas = estoque.pastas_nao_encontradas(pastas)

        #obtem todos os arquivos xml Formato [Dicionario,Dicionario,...]
        produtos = manipuladorJson.obter_todos_os_produtos_por_ids(pastas_filtradas)


        #verificar todos os produtos desta categoria
        for y in range(len(pastas_filtradas)):     
                count = 0
                open_store(abastecer_caixa)    
                #move o mouse para a categoria especifica
                pyautogui.moveTo(633,410,duration=.5)
                pyautogui.click()
                time.sleep(.3)
                if pastas_nome[x] == "Eletros":
                    pyautogui.moveTo(439,476,duration=.5)
                if pastas_nome[x] == "Carros":
                    pyautogui.moveTo(439,509,duration=.5)
                if pastas_nome[x] == "Popular":
                    pyautogui.moveTo(437,540,duration=.5)
                if pastas_nome[x] == "Beleza":
                    pyautogui.moveTo(440,575,duration=.5)
                if pastas_nome[x] == "Digitais":
                    pyautogui.moveTo(439,610,duration=.5)     
                pyautogui.click()                                                                  
                time.sleep(1)
                #Escolher nome do produto
                pyautogui.moveTo(673,492,duration=.5)    
                pyautogui.click() 
                time.sleep(.2)
                pyautogui.doubleClick() 
                time.sleep(.2)
                pyautogui.write(produtos[y]['Nome'][:100], interval=.01)
                
                #Escolher imagem
                pyautogui.moveTo(439,644,duration=.5)    
                pyautogui.click()  
                time.sleep(.3)
                if not modo_teste:
                    pyautogui.moveTo(759,330,duration=.5)    
                    pyautogui.click()  
                    pyautogui.moveTo(1182,56,duration=.5)  
                    pyautogui.click()  
                    path_img = f"RoboLogistica\Produtos\{pastas_nome[x]}\{pastas_filtradas[y]}"
                    letra_img = pastas_filtradas[y][0:1]
                    pyautogui.write(path_img,interval=.01)
                    pyautogui.hotkey('enter')
                    time.sleep(.3)
                    pyautogui.moveTo(1037,216,duration=.5)  
                    pyautogui.click()  
                    pyautogui.hotkey(letra_img)
                    time.sleep(.3)
                    pyautogui.hotkey('enter')
                    time.sleep(4)

                if not select_image_dinamico:    
                    #Escolhe a primeira imagem
                    pyautogui.moveTo(773,461,duration=.5)  
                    pyautogui.click()         
                else:    
                    #Escolha dinâmica
                    url_final = url_base+ f"/{pastas_nome[x]}/{pastas_filtradas[y]}"
                    caminho_imagem_referencia = os.path.join(url_final,pastas_filtradas[y]+".jpg")
                    tamanho_real_da_imagem = (100, 100) 
                    posicao_imagem = encontrar_imagem_redimensionada(caminho_imagem_referencia, tamanho_real_da_imagem)
                    if posicao_imagem:
                        coordenadas_imagem = (posicao_imagem.left + posicao_imagem.width / 2, posicao_imagem.top + posicao_imagem.height / 2)
                        pyautogui.moveTo(coordenadas_imagem, duration=0.5)
                        pyautogui.click(coordenadas_imagem)

                time.sleep(1)   
                pyautogui.moveTo(959,331,duration=.5)   
                pyautogui.click()  
                time.sleep(.4)  

                pyautogui.moveTo(464,886,duration=.5)   
                pyautogui.click()  

                #Abastecer Valores
                precoExibicao = int(produtos[y]['Preco'])
                precoFinal = math.ceil(precoExibicao + precoExibicao * 0.10)
                pontos = precoFinal * 12
                sintese = math.floor(precoFinal / 50)
                if sintese < 1:
                    sintese = 1

             
                time.sleep(2)
                pyautogui.moveTo(613,334,duration=.5)   
                pyautogui.click()
                pyautogui.hotkey('ctrl','a') 
                pyautogui.hotkey('backspace') 
                pyautogui.write(str(precoFinal),interval=.1)
                time.sleep(.1)
                pyautogui.moveTo(606,385,duration=.1)   
                pyautogui.click()
                pyautogui.hotkey('ctrl','a') 
                pyautogui.hotkey('backspace') 
                pyautogui.write(str(pontos))      
                time.sleep(.1)
                pyautogui.moveTo(619,434,duration=.1)   
                pyautogui.click()
                pyautogui.hotkey('ctrl','a') 
                pyautogui.hotkey('backspace') 
                pyautogui.write(str(precoExibicao))     
                time.sleep(.1)
                pyautogui.moveTo(560,486,duration=.1)   
                pyautogui.click()
                pyautogui.hotkey('ctrl','a') 
                pyautogui.hotkey('backspace') 
                pyautogui.write(str(precoFinal),interval=.1)      
                time.sleep(.1)
                pyautogui.moveTo(589,535,duration=.1)   
                pyautogui.click()
                pyautogui.hotkey('ctrl','a') 
                pyautogui.hotkey('backspace') 
                pyautogui.write(str(sintese),interval=.1)   
                time.sleep(.1)    
                pyautogui.moveTo(599,581,duration=.5) 
                pyautogui.click()

                #Detalhes Produto
                pyautogui.moveTo(1504,343,duration=.5) 
                pyautogui.click() 
                #Escolhe a primeira imagem
                pyautogui.moveTo(773,461,duration=.5)  
                pyautogui.click()  
                time.sleep(1)   
                pyautogui.moveTo(959,331,duration=.5)   
                pyautogui.click() 
                time.sleep(1)   
                pyautogui.moveTo(1767,517,duration=.5)   
                pyautogui.click() 
                pyautogui.hotkey('enter') 
                # Obtém a descrição do produto
                descricao_produto = produtos[y]['SobreProduto']
                # Converte a descrição para uma lista formatada
                sobre_formatada = [estoque.decode_html_entities(s) + "\n" for s in descricao_produto]
                # Verifica se a lista não está vazia
                if sobre_formatada:
                    pyautogui.moveTo(534, 344, duration=0.5)
                    pyautogui.click()
                    pyautogui.write("SobreProduto:", interval=0.1)
                    pyautogui.hotkey('enter')

                    # Escreve cada linha da descrição com uma quebra de linha ao final
                    for texto in sobre_formatada:
                        pyautogui.write(texto, interval=0.01)
                else:
                    print("A lista sobre_formatada está vazia.")                    

                descricao_formatada = estoque.decode_html_entities(produtos[y]['Descricao'])
                texto_formatado = estoque.adicionar_espacos(descricao_formatada)
                if not descricao_formatada == "":
                    pyautogui.hotkey('enter') 
                    pyautogui.write("Sobre:", interval=0.1)
                    pyautogui.moveTo(534, 344, duration=0.5)
                    pyautogui.click()
                    pyautogui.hotkey('enter')
                    pyautogui.write(texto_formatado, interval=0.01)


                time.sleep(1)  
                #Salvar dados
                if not salvar_dados:
                    pyautogui.moveTo(323,204,duration=.5)
                    pyautogui.click()        
                else:
                    pyautogui.moveTo(586,952,duration=.5)
                    pyautogui.click()                     


                time.sleep(1.5)
                passou = False
                while not passou:
                    #Verificar se Ocorreu o Erro Do sistema
                    caminho_imagem_referencia = 'imagem/Error.png'
                    posicao_imagem = encontrar_imagem(caminho_imagem_referencia)
                    if posicao_imagem:
                        #Voltar e Alterar a ultima Letra do nome
                        pyautogui.moveTo(362,288,duration=.5)
                        pyautogui.click() 
                        time.sleep(.2)
                        pyautogui.moveTo(886,505,duration=.5)
                        pyautogui.click() 
                        pyautogui.hotkey('backspace')
                        pyautogui.write(str(count))
                        count += 1
                        time.sleep(.2)
                        pyautogui.moveTo(696,284,duration=.5)
                        pyautogui.click() 
                        time.sleep(.2)
                        pyautogui.moveTo(579,953,duration=.5)
                        pyautogui.click() 
                        time.sleep(1.5)
                    else:
                        passou = True

                #Adicionar o nome da pasta em um arquivo chamado arquivos.txt
                estoque.salvar_produto(pastas_filtradas[y])    

                time.sleep(1.5)  

    pyautogui.alert("Robonildo B, Concluio o serviço")

class ControleEstoque:
    def __init__(self, caminho_diretorio):
        self.caminho_diretorio = caminho_diretorio

    def listar_pastas(self):
        try:
            # Obtém a lista de itens no caminho fornecido
            itens = os.listdir(self.caminho_diretorio)

            # Filtra apenas os diretórios
            pastas = [item for item in itens if os.path.isdir(os.path.join(self.caminho_diretorio, item))]

            return pastas

        except FileNotFoundError:
            print(f'O caminho "{self.caminho_diretorio}" não foi encontrado.')
        except PermissionError:
            print(f'Permissão negada para acessar o caminho "{self.caminho_diretorio}".')   

    def decode_html_entities(self,text):
        if text is None or len(text) == 0:
            return ""
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    
    def adicionar_espacos(self,texto):
        # Utiliza expressão regular para adicionar espaços após '.' e '!'
        texto_formatado = re.sub(r'(?<=[.!])', ' ', texto)
        return texto_formatado

    def salvar_produto(self, nome_produto):
        # Cria o caminho completo para a pasta e o arquivo
        caminho_pasta = self.caminho_diretorio
        caminho_arquivo = os.path.join(caminho_pasta, "arquivo.txt")

        # Verifica se o arquivo já existe, se não existir, cria
        if not os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, "w") as novo_arquivo:
                novo_arquivo.write("")

        # Abre o arquivo em modo de leitura para verificar se o produto já existe
        with open(caminho_arquivo, "r") as arquivo:
            produtos_existentes = arquivo.read().splitlines()

        # Verifica se o produto já está na lista
        if nome_produto in produtos_existentes:
            print(f"O produto '{nome_produto}' já existe no arquivo.")
        else:
            # Abre o arquivo em modo de escrita (modo "a" para adicionar ao final do arquivo)
            with open(caminho_arquivo, "a") as arquivo:
                # Escreve o nome do produto seguido de uma quebra de linha
                arquivo.write(nome_produto + "\n")

            print(f"Produto '{nome_produto}' salvo com sucesso no arquivo {caminho_arquivo}")

    def pastas_nao_encontradas(self, lista_de_pastas):
        try:
            caminho_arquivo = os.path.join(self.caminho_diretorio, "arquivo.txt")

            # caso o arquivo não exista, retorna a própria lista de pastas
            if not os.path.isfile(caminho_arquivo):
                return lista_de_pastas

            # Abre o arquivo em modo de leitura para verificar o conteúdo
            with open(caminho_arquivo, "r") as arquivo:
                pastas_no_arquivo = arquivo.read().splitlines()

            # Encontra as pastas que não estão no arquivo
            pastas_nao_encontradas = [pasta for pasta in lista_de_pastas if pasta not in pastas_no_arquivo]

            # Se não houver pastas não encontradas, retorna a própria lista de pastas
            return pastas_nao_encontradas if pastas_nao_encontradas else lista_de_pastas

        except FileNotFoundError:
            print(f'O arquivo "{caminho_arquivo}" não foi encontrado.')
            return []
        except PermissionError:
            print(f'Permissão negada para acessar o arquivo "{caminho_arquivo}".')
            return []


class NavegadorSelenium:

    def __init__(self):
        # Configurar o navegador Chrome (certifique-se de ter o chromedriver instalado e configurado)

        self.navegador = webdriver.Chrome()   

    def abrir_url(self, url):
        # Abrir a URL no navegador
        self.navegador.get(url)        

    def maximize_window(self):
        # Maximiza a janela do navegador
        self.navegador.maximize_window()        

    def find_element_by_name(self, texto):
        try:
            # Espera até que o elemento seja visível
            opt = WebDriverWait(self.navegador, 30).until(
                EC.visibility_of_element_located((By.XPATH, f"//*[text()='{texto}']"))
            )

            print("HELLO HORDI")
        
            # Move o mouse para as coordenadas do elemento
            cordenadas = opt.location_once_scrolled_into_view
            pyautogui.moveTo(cordenadas['x'] + 30, cordenadas['y'] + 30, duration=0.5)

            # Clica no elemento
            pyautogui.click()
            return True
        except TimeoutException:
            # Se ocorrer um timeout, imprime uma mensagem indicando que o elemento não foi encontrado
            print(f"Elemento com o texto '{texto}' não foi encontrado. Movendo para posição alternativa.")
            
            # Move o mouse para a posição alternativa
            pyautogui.moveTo(cordenadas['x'] + 10, cordenadas['y'] + 110, duration=0.5)
            
            # Clica na posição alternativa
            pyautogui.click()
            
            return False

class ManipuladorJSONProdutos:
    def __init__(self):
        self.arquivo_json = None

    def criar_json_produtos(self, pasta, nome_arquivo):
        self.arquivo_json = os.path.join(pasta, nome_arquivo)

        # Verifica se o arquivo já existe
        if os.path.exists(self.arquivo_json):
            print(f"O arquivo '{self.arquivo_json}' já existe. Nenhuma ação adicional foi realizada.")
            return

        # Inicializa a estrutura JSON
        produtos_json = {"produtos": []}

        # Salva o JSON em um arquivo
        with open(self.arquivo_json, "w") as json_file:
            json.dump(produtos_json, json_file, indent=2)

        print(f"Arquivo '{self.arquivo_json}' criado com sucesso.")

    def adicionar_produto(self, campos):
        if not isinstance(campos, dict):
            raise ValueError("O argumento 'campos' deve ser um dicionário.")

        if not os.path.exists(self.arquivo_json):
            self.criar_json_produtos(os.path.dirname(self.arquivo_json), os.path.basename(self.arquivo_json))

        with open(self.arquivo_json, "r", encoding="utf-8") as json_file:
            produtos_json = json.load(json_file)

        produtos_json["produtos"].append(campos)

        with open(self.arquivo_json, "w", encoding="utf-8") as json_file:
            json.dump(produtos_json, json_file, ensure_ascii=False, indent=4)

    def visualizar_produtos(self):
        # Verifica se o arquivo JSON foi criado
        if not self.arquivo_json:
            raise ValueError("O arquivo JSON não foi criado. Chame criar_json_produtos antes de visualizar produtos.")

        # Lê o JSON existente
        with open(self.arquivo_json, "r") as json_file:
            produtos_json = json.load(json_file)

        # Exibe os produtos
        for produto in produtos_json["produtos"]:
            print(json.dumps(produto, indent=2))
            print("---")
   
    def obter_todos_os_produtos_por_ids(self, lista_de_ids):
        if not self.arquivo_json:
            raise ValueError("O arquivo JSON não foi criado. Chame criar_json_produtos antes de obter produtos.")

        with open(self.arquivo_json, "r", encoding='utf-8') as json_file:
            produtos_json = json.load(json_file)

        produtos_filtrados = [produto for produto in produtos_json["produtos"] if produto["Id"] in lista_de_ids]

        return produtos_filtrados
    
