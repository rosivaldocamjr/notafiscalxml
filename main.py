import xmltodict # biblioteca para converter XML em dicionários Python
import os # biblioteca para manipulação de arquivos e diretórios
import pandas as pd # biblioteca para manipulação de dados

# função para ler o arquivo XML e converter em dicionário
def pegar_infos(nome_arquivo, valores):
    with open(f'nf/{nome_arquivo}', 'rb') as arquivo_xml:
        dic_arquivo = xmltodict.parse(arquivo_xml)
        
        # verifica se é NFe ou NFS-e e pega as informações necessárias
        if 'NFe' in dic_arquivo:
            infos_nf = dic_arquivo['NFe']['infNFe']
            numero_nota =  infos_nf['@Id']
            empresa_emissora = infos_nf['emit']['xNome']
            nome_cliente = infos_nf['dest']['xNome']
            endereco = infos_nf['dest']['enderDest']
        elif 'CompNfse' in dic_arquivo:
            infos_nf = dic_arquivo['CompNfse']['Nfse']['InfNfse']
            numero_nota =  infos_nf['@Id']
            empresa_emissora = infos_nf['PrestadorServico']['RazaoSocial']
            nome_cliente = infos_nf['TomadorServico']['RazaoSocial']
            endereco = infos_nf['PrestadorServico']['Endereco']

        # adiciona os valores extraídos na lista
        valores.append([numero_nota, empresa_emissora, nome_cliente, endereco])

# lista todos os arquivos no diretório "nf"
lista_arquivos = os.listdir('nf') 

# define as colunas do DataFrame
colunas = ['numero_nota', 'empresa_emissora', 'nome_cliente', 'endereco']

valores = [] # lista para armazenar os valores extraídos

# função para pegar informações do XML
for arquivo in lista_arquivos:
    pegar_infos(arquivo, valores)

# cria o DataFrame com os valores extraídos
tabela = pd.DataFrame(columns=colunas, data=valores)

# exporta o DataFrame para um arquivo Excel
tabela.to_excel('NotasFiscais.xlsx', index=False)

