import hashlib
import os

import requests
from bs4 import BeautifulSoup
from re import match


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

    RE_DATA = re_data = r'^(?P<ano>\d{4})\D(?P<mes>\d{2})\D(?P<dia>\d{2})\Z'

    MESES_ANO = {
            1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun', 7: 'jul', 8: 'ago', 9: 'set',
            10: 'out', 11: 'nov', 12: 'dez'
        }

    # Método construtor
    def __init__(self, data):
        self._data_busca = data

    # Chamando os métodos utilitarios
    def baixa_cadernos(self) -> None:
        if not self._valida_data(self._data_busca):
            return
        pagina_resultado_busca = self._busca_cadernos()
        links_cadernos = self._parser_links_cadernos(pagina_resultado_busca)
        if not links_cadernos:
            return
        links_pdfs = self._obtem_links_dj(links_cadernos)
        self._baixa_arquivos_pdf(links_pdfs)

    def _valida_data(self, data: str) -> bool:
        data_separada = self._decompoem_data(data)
        if data_separada:
            if data_separada['ano'] <= '2022' and data_separada['mes'] <= '12' and \
                  data_separada['dia'] <= '31':
                return True
        print('Data invalida! \n A informada deve possuir o formato AAAA-MM-DD e ser inferior "31-12-2022".')
        return False

    def _decompoem_data(self, data: str) -> dict:
        match_obj = match(self.RE_DATA, data)
        if match_obj:
            return match_obj.groupdict()
        else:
            return {}

    # Métodos utilitários
    def _busca_cadernos(self):
        """Faz requisição no tribunal e retorna resultado
        """
        link = self.URL_BUSCA.format(data=self._data_busca)
        resposta = requests.get(link, headers=self.HEADERS)
        #import pdb; pdb.set_trace()
        return resposta.text

    def _parser_links_cadernos(self, pagina_resultado_busca):
        '''Obtem os links dos cadernos do tribunal
        '''
        soup = BeautifulSoup(pagina_resultado_busca, "html.parser")
        section = soup.find("section", {"id": "conteudo"})
        lista_anchor = section.find_all('a')
        if not lista_anchor:
            print('Não existem diarios na data informada.')
            return []
        lista_slugs = [anchor['href'] for anchor in lista_anchor]
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
        caminho = self._obtem_caminho()
        os.makedirs(caminho, exist_ok=True)
        for link in links_pdfs:
            url = r'https://portal.stf.jus.br' + link
            response = requests.get(url, headers=self.HEADERS)
            nome_arquivo = self._obtem_md5(response.content) + ".pdf"
            if not os.path.exists(caminho + "/" + nome_arquivo):
                with open(caminho + "/" + nome_arquivo, "wb") as file:
                    file.write(response.content)
                print(f'Caderno com o "{nome_arquivo}" salvo com sucesso!')
            else:
                print(f'Caderno com o "{nome_arquivo}" já existe!')

    def _obtem_caminho(self) -> str:
        data_decomposta = self._decompoem_data(self._data_busca)
        caminho = r'./cadernos/{ano}/{mes}/{dia}/'
        mes = self.MESES_ANO[int(data_decomposta['mes'])]
        return caminho.format(ano=data_decomposta['ano'], mes=mes, dia=data_decomposta['dia'])

    def _obtem_md5(self, conteudo_pdf):
        """recebe conteúdo pdf e calcula o hashMd5
        """
        md5_hash = hashlib.md5(conteudo_pdf).hexdigest()
        return md5_hash
