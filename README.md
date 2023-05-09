# Desafio Crawler - Justiça Fácil

Os diários oficiais são jornais criados, mantidos e administrados por governos para publicar as literaturas dos atos oficiais da administração pública executiva, legislativa e judiciária.

Todos os dias, o sistema desenvolvido pelo Justiça Fácil tem que verificar se os diários do Supremo Tribunal Federal foram baixados corretamente. Para evitar que o mesmo diário seja processado mais de uma vez, é necessário um sistema auxiliar na conferência dos diários baixados pelo sistema, ou seja, um programa que receba uma data e retorne os MD5 dos diários daquele dia. E esta é a funcionalidade do sistema.

## Funcionalidades do sistema
* Verifica se há data passada por parâmetro de execução;
* Lista os DJs e seus respectivos _hashs_ no terminal e salva o arquivo PDF da versão Integral renomeando com seu respectivo _hashs_ dentro de uma pasta com a sua respectiva data.

## Como executar
Para executar o projeto é necessário ter o Python instalado e seguir os passos:

1. Clonar o repositório:
``` bash
git clone https://github.com/thiagoluznascimento/dasafio-crawler.git
```

2. Instalar as seguintes bibliotecas:
```bash
pip install hashlib
pip install requests
pip install beautifulsoup4
```

3. Executar o projeto passando por parâmetro a data no formato "yyyy-mm-dd", como abaixo:
```bash
python script.py "2022-12-13"
```

## Dificuldades:
Uma das dificudades que tive, foi conseguir fazer a requisição com a página do STF, pois, sempre retornava o status code 403, onde em pesquisa feita, revelava que eu não tinha permissão para fazer a requisição. Logo, pedir para imprimir o response em formato de texto que me retornava a seguinte mensagem: "Seu acesso a este website foi bloqueado de forma preventiva. Por favor, tente novamente em alguns minutos. (FD)". Depois de esperar por minutos, horas e nada de conseguir fazer a requisição, foi então que procurei a mensagem no Google para verificar melhor qual seria a solução do problema, e me deparei com a resposta no site [DSD.](https://dsd.arcos.org.br/dmj02/)

Para conseguir fazer a requisição, tive que alterar a estrutura padrão do cabeçalho, sendo a seguinte:
``` python
user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
```
Esta configuração é baseada no código disponibilizado do [DSD.](https://github.com/AlexandreAraujoCosta/DSD-DataScience-Direito)


## Métodos e Bibliotecas utilizadas:
Biblioteca _**sys**_: Usada para receber argumentos passados pelo terminal.

Biblioteca _**hashlib**_: Usada para criar o _hash md5_. Na linha 62 está sendo implementada da seguinte forma:
``` python
hash_md5 = hashlib.md5(url.encode()).hexdigest()
```

Biblioteca _**requests**_: Usada fazer requisições _http_ com o método _GET_ no site do STF. Na linha 30:
``` python
resposta = requests.get(url_busca_djs, headers=user_agent)
```

E na linha 52:
``` python
html = requests.get(url, headers=user_agent)
```

Biblioteca _**os**_: Usada para acessar funções do sistema operacional, como verificar se uma pasta existe e criar uma pasta. Como nas linhas 65 e 66, onde verifica se existe uma pasta e se não existir, a cria:
``` python
if not os.path.exists(data_busca):
    os.mkdir(data_busca)
```

Biblioteca _**BeautifulSoup**_: Permite extrair informações do HTML e XML. Como exemplo nas linhas 31 a 38:
``` python
# Cria o objeto BeautifulSoup
soup = BeautifulSoup(resposta.content, 'html.parser')
# Busca o ul com lista dos DJs
ul = soup.find('ul', {'class': 'result__container--simples'})
# Cria HTML da variável ul
html = BeautifulSoup(ul.prettify(), 'html.parser')
# Busca todas as tags a existentes na variável html
links = html.find_all('a')
```

## Fontes de pesquisa:
* Stackoverflow;
* Chat-GPT;
* Youtube;
* [GitHub](https://github.com/AlexandreAraujoCosta/DSD-DataScience-Direito)
* [DSD.Arcos](https://dsd.arcos.org.br/)
* Google;


 Tive também ajuda de um colega de sala e outra coisa que me ajudou muito, foi um curso que estou fazendo, mestre pythonista, do Jhonatan do canal Dev-aprender [Resumo do Curso.](https://www.youtube.com/watch?v=T9hHdYy-teI&t=224s&ab_channel=DevAprender)
