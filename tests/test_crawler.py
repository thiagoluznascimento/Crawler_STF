from unittest.mock import patch, Mock
from unittest import TestCase

from pytest import mark
import pytest

from src.crawler import CrawlerStf

"""Estamos utilizando a metodologia agil (Given-When-Then)'givem uen dem' 
    Given = Dado(contexto)... dado determinado contexto...alguma coisa acontece
    When = Quando(Ação)... alguma coisa
    Then = Então(Resultado)... alguma coisa ocorre e o resultado é esperado
"""


class TestCrawlerStf(TestCase):

    def setUp(self):
        self.instacia_crawler = CrawlerStf('2022-12-14')
        self.url = ( 
            'https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ='
            'periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={data}&dataFinal={data}'
            '&tipoPesquisaDJ=&argumento='
        )
        self.headers = {
            'User-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                ' Chrome/89.0.4389.90 Safari/537.36'
            )
        }

    def test_quando_decompoem_data_recebe_data_deve_retornar_dicionario(self):
        entrada = "2022-12-14"  # given(Dado contexto)
        esperado = {
            'ano': '2022',
            'mes': '12',
            'dia': '14'
        }
        # instanciando
        data_teste = CrawlerStf(entrada)
        # when a acao
        resultado = data_teste._decompoem_data(entrada)  # chamando o método que calcula o bonus

        assert resultado == esperado  # Then o resultado esperado (desfecho)

    def test_quando_valida_data_recebe_decompoem_data_retorna_boleano(self):
        entrada = {
            'ano': '2022',
            'mes': '12',
            'dia': '14'
        }
        esperado = True

        data_teste01 = CrawlerStf(entrada)
        resultado = data_teste01._valida_data()
        assert resultado == esperado

    def test_busca_cadernos(self):
        with open('./tests/fixtures/pagina.html', 'r') as arquivo:
            html_esperado = arquivo.read()
        with patch('requests.get', return_value=Mock(text=html_esperado)) as mock_get:
            html_obtido = self.instacia_crawler._busca_cadernos()
        self.assertEqual(html_esperado, html_obtido)
        mock_get.assert_called_once_with(self.url.format(data='2022-12-14'), headers=self.headers)
        # import pdb; pdb.set_trace()
    