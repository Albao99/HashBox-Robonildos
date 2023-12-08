import tkinter as tk
import winsound
import threading
import os,pyautogui, time
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

categoria_selected = '-1'
navegador_selenium = None
produtos = [] 

def obter_escolha():
    global categoria_selected
    global produtos

    categoria_selected = var_opcao.get()

    #Encontra o caminho para carregar os links
    path = f"Links/{categoria_selected}.txt"

    produtos = ler_linhas_do_arquivo(path)

    janela.destroy()

def habilitar_botao(*args):
    escolha = var_opcao.get()
    botao_obter_escolha["state"] = tk.NORMAL if escolha else tk.DISABLED

#Carregamento em XML
def carregar_produtos_por_categoria(arquivo_xml):
    produtos = []

    tree = ET.parse(arquivo_xml)
    root = tree.getroot() 

    for categoria in root.findall(".//categoria[@nome='" + categoria_selected + "']"):
        for produto_element in categoria.findall("produto"):
            link = produto_element.text
            produtos.append(link)

    return produtos

#Carregar os links 
def ler_linhas_do_arquivo(caminho_do_arquivo):
    # Inicializa um array para armazenar as linhas
    linhas = []
    # Abre o arquivo em modo de leitura
    with open(caminho_do_arquivo, 'r') as arquivo:
        # Lê cada linha do arquivo e adiciona ao array
        for linha in arquivo:
            linhas.append(linha.strip())

    return linhas

def path_exist(path):
     caminho_completo = os.path.join(path, "dados.xml")
     if os.path.exists(caminho_completo):
      return True
     else:
      return False

def update():
    global navegador_selenium
    global produtos
   

    if navegador_selenium is None:
        navegador_selenium = NavegadorSelenium()

    navegador_selenium.maximize_window()
    gerenciador_json = ManipuladorJSONProdutos()
    path = f"Produtos/{categoria_selected}/"
    gerenciador_json.criar_json_produtos(path,"dados.json")

    manipulador_index = GestorIndex(path)

    id = manipulador_index.obter_valor_index()
# Verificar se o id é maior ou igual à quantidade de produtos
    if id >= len(produtos):
        popUp = PopupAutoClose("Todos os itens forão adicionados",3)        
        popUp.exibir()
        time.sleep(3)
        navegador_selenium.fechar_navegador()
        return

    index = id
    # Se o id for menor que a quantidade de produtos, execute o loop
    while index < len(produtos):
        nova_url = produtos[index]
        navegador_selenium.alterar_url(nova_url)
        time.sleep(4)
        retorno = navegador_selenium.criar_produto(nova_url, gerenciador_json, index)
        if retorno == -1:
            popUp = PopupAutoClose("Erro ao baixar produto dessa URL, Vamos verificar uma próxima URL",2)
            popUp.exibir()
            time.sleep(2)
            index += 1
            continue
        
        manipulador_index.incrementar_valor_index()
        index += 1

    popUp = PopupAutoClose("Ok, trabalho concluído",2)
    popUp.exibir()
    time.sleep(2)
    navegador_selenium.fechar_navegador()
    return
        


        


# iniciar o core
pyautogui.alert("A partir desse momento não mexa no seu computador!!")

    # Criar a janela principal
janela = tk.Tk()
janela.title("Escolha uma Categoria de Produtos")
janela.geometry("300x150")  # Define o tamanho da janela
janela.resizable(False, False)  # Impede o redimensionamento da janela

    # Variável para armazenar a escolha do usuário
var_opcao = tk.StringVar()
var_opcao.trace_add("write", habilitar_botao)  # Rastrear alterações na variável


    # Opções disponíveis
opcoes = ["Eletros", "Popular", "Beleza", "Carros", "Digitais"]

    # Criar o campo de opções
opcoes_menu = tk.OptionMenu(janela, var_opcao, *opcoes)
opcoes_menu.pack(pady=20)

    # Botão para obter a escolha
botao_obter_escolha = tk.Button(janela, text="Obter Escolha", command=obter_escolha, state=tk.DISABLED)
botao_obter_escolha.pack(pady=10)

    # Centro da tela
largura_janela = janela.winfo_reqwidth()
altura_janela = janela.winfo_reqheight()
posicao_x = (janela.winfo_screenwidth() // 2) - (largura_janela // 2)
posicao_y = (janela.winfo_screenheight() // 2) - (altura_janela // 2)

janela.geometry(f"+{posicao_x}+{posicao_y}")

    # Iniciar o loop principal da interface gráfica
janela.protocol("WM_DELETE_WINDOW", lambda: None)  # Impede o fechamento da janela
janela.mainloop()

# Classes

class NavegadorSelenium:
    descricao_url = "productDescription"#div/id
    nome_url  = "productTitle"#span/id
    preco_url  = "a-price-whole"#span/class
    centavos_url = "a-price-fraction"#span/class
    sobre_url = "feature-bullets"#div/class
    url_image = "a-dynamic-image"#img/class 
    # Diretório onde as imagens serão salvas(Dinâmico)
    diretorio_destino = ""

    def __init__(self):
        # Configurar o navegador Chrome (certifique-se de ter o chromedriver instalado e configurado)

        self.navegador = webdriver.Chrome()

    def abrir_url(self, url):
        # Abrir a URL no navegador
        self.navegador.get(url)

    def alterar_url(self, nova_url):
        # Limpar a barra de endereço e digitar a nova URL
        self.navegador.get(nova_url)
        WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.ID, 'imgTagWrapperId')))

    def maximize_window(self):
        # Maximiza a janela do navegador
        self.navegador.maximize_window()

    def fechar_navegador(self):
        # Fechar o navegador
        self.navegador.quit()

    def get_soup(self, url):
            # Adicione um timeout para evitar que a solicitação fique presa por muito tempo
        webpage = requests.get(url)

        if not webpage.status_code == 200:
            return -1


        soup = BeautifulSoup(webpage.content, "html.parser")
        return soup
       
    #GET
    def get_nome_produto(self,soup):
        #nomeProduto
        nome_produto = soup.find("span",{"id":self.nome_url})
        resposta = nome_produto.text.replace(" ", "")[0:10]
        # Remove caracteres especiais usando expressão regular
        texto_sem_especiais = re.sub(r'[^a-zA-Z0-9]', '', resposta)
        respostaCompleta = re.sub(r'[^a-zA-Z0-9]', '', nome_produto.text)
        return [texto_sem_especiais,respostaCompleta]
    def get_descricao_produto(self,soup):
        #descriçãoProduto
        descricao = soup.find("div",{"id":self.descricao_url})
        if not descricao:
            return ""    
        resposta = descricao.text.replace(" ", "")
        return resposta
    def get_preco_produto(self,soup):
        #precoProduto 
        preco_produto = soup.find("span",{"class":self.preco_url})

        resposta = re.sub('[.,]','',preco_produto.text)
        return resposta  
    def get_centavos_produto(self,soup):
        #centavosProduto
        centavos_produto = soup.find("span",{"class":self.centavos_url})
        return centavos_produto  
    def get_sobre_produto(self, soup):
        # sobreProduto
        sobre_produto = soup.find("div", {"id": self.sobre_url})
        
        if sobre_produto:
            # Encontrar todos os spans com uma classe específica dentro da UL
            span_elements = sobre_produto.find_all('span', class_='a-list-item')
            
            if span_elements:
                # Adiciona uma quebra de linha no final de cada item e limita os espaços consecutivos
                resposta = [re.sub(r'\s+', ' ', f"{elemento.text}\n").strip() for elemento in span_elements]
                return resposta
        
        return ""

    def get_all_url_imagem_produto(self,soup):
        #imageProduto
        imagem_produto = soup.find_all("img", class_=self.url_image)
        return imagem_produto
    
    #Download Imagem
    def download_image(self,imagem_produto,diretorio_destino,nome_arquivo):
        if imagem_produto:
            url_imagem = imagem_produto[0].get("src")
            caminho_arquivo = os.path.join(diretorio_destino, nome_arquivo+".jpg")
            imgDownload = requests.get(url_imagem)
            with open(caminho_arquivo, "wb") as arquivo:
                arquivo.write(imgDownload.content)

    def criar_produto(self, url,gerenciado,index):
        global categoria_selected
        soup = self.get_soup(url)

        if soup == -1:
            return -1

        nome_produto = self.get_nome_produto(soup)
        preco = self.get_preco_produto(soup)
        detalhes = self.get_sobre_produto(soup)
        descricao = self.get_descricao_produto(soup)
        url_img = self.get_all_url_imagem_produto(soup)
        #criar um diretorio dentro da categoria escolhida
        dir = f"Produtos/{categoria_selected}/{nome_produto[0]}"+f"_{index}"

        if not os.path.exists(dir):
            os.makedirs(dir)           
            print(f"Diretorio criado em: {dir}")
        else:
            print(f"Já existe esse item no diretório {dir}")
            return    
        time.sleep(.5)
        
        #baixar a imagem do produto
        self.download_image(url_img,dir,nome_produto[0]+f"_{index}")
        print(f"Imagem baixado em: {dir}")
        time.sleep(.5)


        #Adicionar produto 
        novos_produtos = {
            "Id":  nome_produto[0]+f"_{index}",
            "Nome": nome_produto[1], 
            "Preco": preco, 
            "Descricao": descricao, 
            "SobreProduto": detalhes}
        gerenciado.adicionar_produto(novos_produtos)     
        print(f"produto adicionado com sucesso")

class GestorIndex:
    def __init__(self, diretorio):
        self.diretorio = diretorio
        self.caminho_index = os.path.join(self.diretorio, 'index.txt')

    def obter_valor_index(self):
        # Verifica se o arquivo "index.txt" existe
        if os.path.exists(self.caminho_index):
            with open(self.caminho_index, 'r') as arquivo:
                # Lê o valor do arquivo e converte para inteiro
                valor = int(arquivo.read().strip())
                return valor
        else:
            # Se o arquivo não existe, retorna 0
            return 0

    def incrementar_valor_index(self):
        valor_atual = self.obter_valor_index()
        novo_valor = valor_atual + 1

        # Salva o novo valor no arquivo "index.txt"
        with open(self.caminho_index, 'w') as arquivo:
            arquivo.write(str(novo_valor))

        return novo_valor

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
    def obter_todos_os_produtos(self):
        if not self.arquivo_json:
            raise ValueError("O arquivo JSON não foi criado. Chame criar_json_produtos antes de obter produtos.")

        with open(self.arquivo_json, "r") as json_file:
            produtos_json = json.load(json_file)

        return produtos_json["produtos"]
    
class PopupAutoClose:
    def __init__(self, mensagem, tempo_fechar=3000):  # Tempo em milissegundos (3 segundos padrão)
        self.root = tk.Tk()
        self.root.withdraw()  # Esconde a janela principal
        self.root.title("Popup")
        self.root.geometry("300x150")  # Ajusta o tamanho da janela

        self.label = tk.Label(self.root, text=mensagem, font=("Arial", 12))
        self.label.pack(padx=10, pady=10)

        # Configura um temporizador para fechar a janela após um tempo específico
        self.root.after(tempo_fechar, self.fechar_popup)

    def fechar_popup(self):
        self.root.destroy()

    def exibir(self):
        # Toca o som do sistema (substitua 'path/do/seu/som.wav' pelo caminho do seu arquivo de som)
        winsound.PlaySound('path/do/seu/som.wav', winsound.SND_FILENAME)

        # Centraliza a janela na tela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

        self.root.deiconify()  # Torna a janela visível
        self.root.mainloop()    