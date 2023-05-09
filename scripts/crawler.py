import sys
import hashlib
import requests
import os
from bs4 import BeautifulSoup


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

#teste 