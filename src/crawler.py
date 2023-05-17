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
        links_pdfs = self._obtem_links_dj(links_cadernos)
        baixa_pdfs = self._baixa_arquivos_pdf(links_pdfs)
        hashs_md5 = self._obtem_md5(baixa_pdfs)

# Métodos utilitários
    def _busca_cadernos(self):
        """Faz requisição no tribunal e retorna resultado
        """
        link = self.URL_BUSCA.format(data=self._data_busca)
        resposta = requests.get(link, headers=self.HEADERS)
        return resposta.text

    def _parser_links_cadernos(self, pagina_resultado_busca):
        '''Obtem os links dos cadernos do tribunal
        '''
        soup = BeautifulSoup(pagina_resultado_busca, "html.parser")
        ul = soup.find("ul", {"class": "result__container--simples"})
        lista_anchor = ul.find_all('a')
        lista_slugs = [anchor['href'] for anchor in lista_anchor]
        # for anchor in lista_anchor:
        #     lista_slugs.append(anchor['href'])
        return lista_slugs

    def _obtem_links_dj(self, links_cadernos):
        """Parsea os links que contém DJs do dia
        """
        links = links_cadernos
        listas_slugs_pdfs = []
        for link in links:
            url = 'https://portal.stf.jus.br/servicos/dje/' + link
            response = requests.get(url, headers=self.HEADERS)
            slug = self._parser_links_dj(response.text)
            if slug:
                listas_slugs_pdfs.append(slug)
        return listas_slugs_pdfs

    def _parser_links_dj(self, pagina_html_dj):
        soup = BeautifulSoup(pagina_html_dj, "html.parser")
        ancor_pdf = soup.find("a", string="Integral")
        if not ancor_pdf:
            return ''
        return ancor_pdf['href']

    def _baixa_arquivos_pdf(self, links_pdfs):
        """Verifica se existe a pasta com nome igual ao dia do arquivo e o cria se não existir;
        itera os slugs dos pdfs e baixa, faz requisição para obter o conteúdodo pdf.
        """
        if not os.path.exists(self._data_busca):
            os.mkdir(self._data_busca)
        url = links_pdfs
        self.nome_arquivo = 'teste.pdf'
        response = requests.get(url, headers=self.HEADERS)
        with open(self.nome_arquivo, "wb") as file:
            file.write(response.content)
        return response.content

    def _obtem_md5(self, baixa_pdfs):
        """recebe conteúdo pdf e calcula o hashMd5
        """
        response = requests.get(url=baixa_pdfs, headers=self.HEADERS)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        self.dicionario[md5_hash] = baixa_pdfs
        return self.dicionario
