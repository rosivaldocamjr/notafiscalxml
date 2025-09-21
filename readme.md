# notafiscalxml

Sistema em Python para **ler notas fiscais em XML (NFe e NFS‑e)**, **extrair campos-chave** e **gerar uma planilha Excel** consolidada.

---

## 📦 Visão geral

O projeto percorre todos os arquivos XML dentro da pasta `nf/`, identifica se cada arquivo é **NFe (modelo 55)** ou **NFS‑e**, extrai informações básicas e salva o resultado em `NotasFiscais.xlsx` na raiz do projeto.

**Campos exportados**

* `numero_nota`
* `empresa_emissora`
* `nome_cliente`
* `endereco` (objeto/dicionário conforme presente no XML)

---

## 🗂️ Estrutura sugerida de pastas

```
notafiscalxml/
├─ nf/                      # Coloque aqui os XMLs de NFe e NFS‑e
│  ├─ nfe_produto_pf.xml
│  ├─ nfe_produto_pj.xml
│  ├─ nfse_servico_pf.xml
│  └─ nfse_servico_pj.xml
├─ main.py                  # Script principal
├─ .gitignore               # Itens ignorados pelo Git
└─ NotasFiscais.xlsx        # Saída gerada (criada após a execução)
```

> **Importante:** a pasta `nf/` precisa existir e conter os XMLs. O script lista os arquivos com `os.listdir('nf')`.

---

## ✅ Pré‑requisitos

* Python 3.10+
* Pip e (opcional) ambiente virtual (venv)

### Instalação

```bash
# 1) Clone o repositório
# git clone <url>
# cd notafiscalxml

# 2) (Opcional) Crie e ative um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 3) Instale as dependências
pip install -U pandas xmltodict openpyxl
```

* **pandas**: manipulação da tabela e exportação para Excel
* **xmltodict**: conversão de XML para dicionários Python
* **openpyxl**: engine para `DataFrame.to_excel()`

---

## ▶️ Como usar

1. Coloque os arquivos `.xml` dentro da pasta `nf/` (pode misturar NFe e NFS‑e).
2. Execute o script:

```bash
python main.py
```

3. A planilha `NotasFiscais.xlsx` será criada/atualizada na raiz do projeto.

---

## 🔍 O que o script extrai (regra atual)

### Quando o arquivo é **NFe**

* Raiz: `NFe` → `infNFe`
* Campos:

  * `numero_nota`: atributo `@Id`
  * `empresa_emissora`: `emit/xNome`
  * `nome_cliente`: `dest/xNome`
  * `endereco`: `dest/enderDest` (objeto com logradouro, bairro, etc.)

### Quando o arquivo é **NFS‑e**

* Raiz: `CompNfse` → `Nfse` → `InfNfse`
* Campos:

  * `numero_nota`: atributo `@Id`
  * `empresa_emissora`: `PrestadorServico/RazaoSocial`
  * `nome_cliente`: `TomadorServico/RazaoSocial`
  * `endereco`: `PrestadorServico/Endereco` (objeto com logradouro, bairro, etc.)

> Observação: o campo `endereco` é mantido como dicionário no DataFrame; ao exportar para Excel, será serializado como string.

---

## 📄 Exemplo de saída (colunas)

| numero\_nota | empresa\_emissora             | nome\_cliente          | endereco |
| ------------ | ----------------------------- | ---------------------- | -------- |
| NFe...0010   | Empresa Exemplo LTDA          | João da Silva          | {...}    |
| NFS-e-0002   | Empresa Serviços Exemplo LTDA | Cliente PJ Exemplo S/A | {...}    |

> Os valores acima variam conforme o conteúdo dos seus XMLs.

---

## ⚠️ Limitações e observações

* **Namespaces**: se seus XMLs usam *namespaces* padrão (`xmlns="..."`), o `xmltodict` normalmente funciona sem configuração extra. Em casos específicos, pode ser necessário ajustar a parsing (ex.: `process_namespaces=True`) e os caminhos das chaves.
* **Variedade de layouts**: NFe e NFS‑e possuem variantes municipais/UF. Se o layout divergir dos caminhos mostrados, será preciso adaptar os acessos no código (`main.py`).
* **Endereço como objeto**: atualmente não há *flatten* do `endereco`. Se quiser colunas separadas (logradouro, número, bairro, cidade, UF, CEP), veja a seção “Customizações”.

---

## 🛠️ Customizações sugeridas

### 1) Tratar endereço em colunas

Você pode “achatar” o endereço para colunas próprias (ex.: `logradouro`, `numero`, `bairro`, `municipio`, `uf`, `cep`), convertendo o dicionário em campos simples antes de criar o DataFrame.

### 2) Normalizar chaves por município/UF

Para NFS‑e, crie *mapeadores* por provedor/município, garantindo extração robusta mesmo quando o XML muda de nome de tag.

### 3) Lidando com erros

* Verificar se a pasta `nf` existe
* Ignorar arquivos não‑XML
* Tentar/except para `KeyError` quando alguma chave não existe

---

## 🧪 Testes rápidos

* Inclua 2 NFe e 2 NFS‑e na pasta `nf/` e rode o script
* Abra `NotasFiscais.xlsx` e verifique se há 4 linhas e 4 colunas

---

## 🤝 Contribuição

Sinta‑se à vontade para abrir *issues* e *pull requests* com melhorias (por exemplo: suportar mais campos, realizar *flatten* do endereço, validar schemas XSD, etc.).

---

## 📄 Licença

Defina a licença de sua preferência (MIT, Apache‑2.0, etc.).
