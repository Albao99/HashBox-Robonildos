import CORE
import pyautogui, time
from bs4 import BeautifulSoup


url = "https://admin.slots777.com.br/backend/#/login"
administrador = 'operador'
senha = '123456'
captcha = ''
abastecer_caixa = False
url_base = r"C:\Users\almlc\OneDrive\Área de Trabalho\RoboLogistica\Produtos"
pastas_nome = ['Carros','Beleza','Digitais','Eletros','Popular']


navegador = CORE.initialize(url)

pyautogui.alert("Vamos lá, a partir de agora só faça o que o Robonildo falar, ok?")
time.sleep(1)

logado = False

#Logar

while(not logado):
    resultado = CORE.obter_informacoes()
    captcha = resultado
    #Logar
    logado = CORE.logar(administrador,senha,captcha)

pyautogui.alert("Logado")


#Verificar RokuExpress|D
abastecer_caixa = CORE.verifiar_tipo_abstecimento()

#Traduzir Tela
CORE.traduzir()


#Iniciar Abastecimento
CORE.iniciar_abstecimento(url_base,pastas_nome,abastecer_caixa)

