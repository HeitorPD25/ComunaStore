# ComunaStore

Sistema desktop de controle de estoque e fechamento de vendas, feito em Python. O caixa escaneia (ou digita) o código de um produto, o sistema calcula o total da compra e atualiza o estoque automaticamente, salvando tudo numa planilha Excel.

Projeto criado com fins de aprendizado — praticando Programação Orientada a Objetos em Python (incluindo herança e tratamento de exceções), organização em camadas, e desenvolvimento de interface gráfica com CustomTkinter.

## Funcionalidades (v1)

- Consultar/acessar o estoque
- Iniciar uma venda
- Adicionar itens à venda por código (com suporte a quantidade)
- Cálculo automático do total
- Baixa automática de estoque ao finalizar a venda
- Tratamento de código não encontrado, sem travar a venda

## Tecnologias

- **Python** — linguagem principal, orientada a objetos
- **pandas** — leitura e escrita da planilha Excel
- **CustomTkinter** — interface gráfica

## Arquitetura

O projeto é organizado em camadas, cada uma com uma responsabilidade única:

| Arquivo | Responsabilidade |
|---|---|
| `model.py` | Entidades: `Produto`, `Livro`, `Roupa`, `ItemVenda`, `Venda` |
| `data.py` | Leitura/escrita da planilha Excel (`Repository`) |
| `service.py` | Regras de negócio: validar código, calcular total, dar baixa em estoque (`VendaService`) |
| `exceptions.py` | Exceções customizadas do domínio |
| `ui.py` | Interface gráfica (CustomTkinter), organizada como classe |

## Modelo de dados

Os produtos são modelados com herança: `Produto` é a classe base (código, categoria, nome, preço, estoque), especializada em `Livro` (autor, editora, páginas) e `Roupa` (modelo, tamanho, cor).

## Como rodar

```bash
pip install pandas openpyxl customtkinter
python ui.py
```

> É necessário um arquivo `estoque.xlsx` na mesma pasta, com as colunas: `Codigo`, `Categoria`, `Nome`, `Preco`, `QuantidadeEstoque`, `Autor`, `Editora`, `Paginas`, `Modelo`, `Tamanho`, `Cor`.

## Backlog futuro

- Cadastro de novo produto pela interface
- Exportação de relatórios de vendas
- Cálculo de descontos
- Consulta de preço sem iniciar venda
- Login de usuário
- Múltiplas formas de pagamento
- Integração com leitor de código de barras físico (a arquitetura já contempla essa evolução — o leitor simula teclado + Enter, o que já é o comportamento esperado pelo campo de escaneamento)
