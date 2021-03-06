# WebScrapping Project - G1 Latest News
# Author: duvrdx (Eduardo Henrique)
# 
# Libs: Selenium - BeautifulSoup - pandas

# Importações
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import re
from datetime import date, timedelta

def main():
    # Variáveis
    browser_url = "https://g1.globo.com/"
    search_title = ""
    archive_name = ""
    html_browser = ""
    data_list = []
    dataframe = ""
    
    # Criando configurações
    Config = Options()
    Config.add_argument('window-size=1280,720') #Definido tamanho de tela do Navegador
    #Config.add_argument('--headless') #Deixando a automação invisivel
    
    # Instanciando Navegador
    Browser = webdriver.Chrome('project\chromedriver', options=Config)
    
    # Abrindo Navegador
    Browser.get(browser_url)
    
    # Entrada de dados para pesquisa das noticias
    search_title = str(input("Insira o termo que deseja buscar:\n"))
        
    # Inserindo valor no input
    search_input = Browser.find_element_by_id('busca-campo')
    search_input.send_keys(search_title)
    search_input.submit()  
    sleep(1)
    
    # Rolando a página para atualizar as noticias
    for i in range(0,4):
        Browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1) 
    
    # Automatizando clique nos botões para obter mais noticias
    for i in range(0,5):
        more_button = Browser.find_element_by_class_name('pagination__load-more')
        more_button.click()
        sleep(1) 
        Browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    # Transformando conteúdo da página para objeto BeautifulSoup
    html_browser = Browser.page_source.replace("\u200b", "")
    Site = BeautifulSoup(html_browser, 'html.parser')
    
    # Buscando cards de Notícia
    for Card in Site.find_all("li", attrs={"class":"widget widget--card widget--info"}):
        title = Card.find("div", attrs={"class":"widget--info__title product-color"}).text
        description = Card.find("p", attrs={"class":"widget--info__description"}).text
        pub_date = Card.find("div", attrs={"class":"widget--info__meta"}).text[0:10]
        link = Card.find("a")["href"]
        
        # Modificando Data de Publicação
        
        # Para modificar a data, detectei o padrão das datas contidas no site_config_dir
        
        # Verificando se existe 'h' no meio da string, como mostrado no site. Ex: "há 6 dias" ou "há 2 horas"
        if 'h' not in pub_date:
            pub_date = pub_date
        else:
            
            # Caso tenha 'd', pelo padrão significa dias, para isso pegamos
            # quantos dias atrás foram, e subtraimos da data atual 
            if 'd' in pub_date:
                # Usando regex para pegar apenas numeros da string
                num = re.sub('[^0-9]', '', pub_date)
                
                # Retornando data
                pub_date = date.today() - timedelta(days=int(num))
                pub_date = f"{pub_date.day:02d}/{pub_date.month:02d}/{pub_date.year}"
            
            # Caso contrário, adicionamos a data de atual
            else:
                # Tranformando data no dia atual
                pub_date = f"{date.today.day:02d}/{date.today.month:02d}/{date.today.year}"
                    
        # Adicionando dados a lista
        data_list.append([title[9:-7],description,pub_date,link])
    
    # Criando dataframe com as informações obtidas
    dataframe = pd.DataFrame(data_list, columns=["title","description","date","link"])
    print(dataframe)
    
    # Exportando DF como CSV e XLSX
    archive_name = str(input("Qual nome deseja dar ao seu arquivo?:\n"))
    dataframe.to_csv(f"project/{archive_name}.csv", encoding='utf-8', index=False)
    dataframe.to_excel(f'project/{archive_name}.xlsx', index = False)
    
if __name__ == "__main__":
    main()