import sys
import hashlib
import os

import requests
from bs4 import BeautifulSoup


class CrawlerStf:
    '''Classe CrawlerStf para fazer extrações das publicações no STF'''
    HEADERS = {
        "User-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/89.0.4389.90 Safari/537.36"
        )
    }
    URL_BUSCA = ( 
        "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ="
        "periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={data}&dataFinal={data}"
        "&tipoPesquisaDJ=&argumento="
    )
# Método construtor

    def __init__(self, data):
        self._data_busca = data

# Chamando os métodos utilitarios

    def baixa_cadernos(self):
        pagina_resultado_busca = self._busca_cadernos()
        links_cadernos = self._parser_links_cadernos(pagina_resultado_busca)
        #print(links_cadernos)
        #slugs_pdfs = self._obtem_slugs_cadernos(pagina_resultado_busca)
        #arquivos_pdf = self._baixa_arquivos_pdf(slugs_pdfs)
        #self._salva_arquivos(arquivos_pdf)
        #self._exibe_conteudo_baixado(arquivos_pdf)

# Métodos utilitários
    def _busca_cadernos(self):
        """Faz requisição no tribunal e retorna resultado"""
        link = self.URL_BUSCA.format(data=self._data_busca)
        resposta = requests.get(link, headers=self.HEADERS)
        return resposta.text

    def _parser_links_cadernos(self, pagina_resultado_busca):
        '''Obtem os links dos cadernos do tribunal'''
        soup = BeautifulSoup(pagina_resultado_busca, "html.parser")
        ul = soup.find("ul", {"class": "result__container--simples"})
        lista_anchor = ul.find_all('a')
        lista_slugs = [anchor['href'] for anchor in lista_anchor]
        # for anchor in lista_anchor:
        #     lista_slugs.append(anchor['href'])
        return lista_slugs


    def _parser_links_pdfs(self):
        """Parsea conteudo HTML e retorna lista de slugs(parte legivél da url) dos cadernos PDF"""


    def _baixa_arquivos_pdf(self, slugs_pdfs):
#        """Itera os slugs dos pdfs e baixa faz requisição para obter o conteudo do pdf
#        e retorna dicionario relacionando seu mdc com o seu conteudo."""
#
#        dicionario = {}
#        for slug in slugs_pdfs:
#            response = requests.get(url=slug)
#            dicionario[self._obtem_md5(response.content)] = response.content
#
#    def _obtem_md5(conteudo_pdf):
#        """recebe conteúdo pdf e calcula o hashMd5"""
#        pass


#############################################################################################################
# Codigo antigo
"""""
def main():
    # Verifica se foi passada uma data como argumento
    if len(sys.argv) < 2:
        print("Por favor, informe uma data no formato YYYY-MM-DD")
        return

    # Obtém a data informada
    data_busca = sys.argv[1]

    #Formata para dd/mm/yyyy
    md_data = data_busca.split("-")
    data_formatada = md_data[2] + "/" + md_data[1] + "/" + md_data[0]

    # Definine informações do cabeçalho de soliticação
    user_agent = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }

    # URL de busca de arquivos referentes à data passada por parâmetro
    url_busca_djs = f"https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ={md_data[0]}&dataInicial={data_busca}&dataFinal={data_busca}&tipoPesquisaDJ=&argumento="

    # Retorna página com todos os DJs referentes à data
    resposta = requests.get(url_busca_djs, headers=user_agent)
    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(resposta.content, "html.parser")
    # Busca o ul com lista dos DJs
    ul = soup.find("ul", {"class": "result__container--simples"})
    # Cria HTML da variável ul
    html = BeautifulSoup(ul.prettify(), "html.parser")
    # Busca todas as tags a existentes na variável html
    links = html.find_all("a")

    for link in links:
        # Divifine o conteúdo do href
        split_link = link.get("href").split("&")
        # Difine o conteúdo da variável split_link
        split_dj = split_link[1].split("=")
        # Atribui à variável a posição 1 do array split_dj que é referente ao número DJ
        num_dj = split_dj[1]

        if (num_dj != "0"):
            # Link para a busca do PDF, de acordo com o numero do DJ e a data, passados por parâmetro
            url = f"https://portal.stf.jus.br/servicos/dje/verDiarioEletronico.asp?numero={num_dj}&data={data_formatada}"

            # Retorna página com o PDF
            html = requests.get(url, headers=user_agent)
            # Atribui à variável status o valor do status code
            status = html.status_code

            # Verifica se o status code é diferente de 200
            if status != 200:
                print("Não foi possível obter o arquivo PDF do Diário Oficial da União do STF")
                return

            # Cria o hash MD5 do arquivo PDF  ...  passei como encode() pq a funcao hashlib.md5() espera um obj tipo bytes
            hash_md5 = hashlib.md5(url.encode()).hexdigest()

            # Verifica se existe a pasta com nome igual ao dia do arquivo e o cria se não existir
            if not os.path.exists(data_busca):
                os.mkdir(data_busca)

            # Abre e salva o arquivo PDF com o nome sendo o valor do seu respectivo hash
            with open(data_busca + "/" + hash_md5 + ".pdf", "wb") as f:
                f.write(html.content)

            # Imprime o hash MD5 na saída padrão
            print("No. DJ: " + num_dj + "\nHash: " + hash_md5 + "\n")

        
# verificando se a variavel __name__ == __main__,(verifica se este aquivo está sendo execultado) entao execulta o main() lá de cima.
if __name__ == "__main__":
    main()
"""