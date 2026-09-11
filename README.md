# ComunaStore

Sistema desktop de controle de estoque e fechamento de vendas, feito em Python. O caixa escaneia (ou digita) o código de um produto, o sistema calcula o total da compra e atualiza o estoque automaticamente, salvando tudo numa planilha Excel.

Projeto criado com fins de aprendizado — praticando Programação Orientada a Objetos em Python (incluindo herança e tratamento de exceções), organização em camadas, e desenvolvimento de interface gráfica com CustomTkinter.

## Funcionalidades (v1)

- Consultar/acessar o estoque
- Consultar o preço de um produto sem iniciar venda
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

### Gestão de estoque
- Cadastro de novo produto pela interface
- Edição de produto existente (preço, nome, etc.)
- Alerta visual de estoque baixo (produtos abaixo de um limite mínimo)
- Remover produto do catálogo

### Vendas
- Cálculo de descontos
- Remover um item já escaneado, antes de finalizar a venda
- Múltiplas formas de pagamento
- Cancelar a venda inteira em andamento (sem salvar nada)

### Relatórios / Análise
- Exportação de relatório de vendas
- Produto mais vendido / ranking de vendas
- Total vendido no dia/período

> **Dependência importante:** hoje, uma vez que a venda é finalizada, os dados dela em si se perdem — só o reflexo no estoque fica salvo. Praticamente todo o bloco de Relatórios depende de um histórico de vendas persistido, que ainda não existe. Provavelmente é o primeiro passo de infraestrutura necessário antes de atacar essa área.

### Outros
- Login de usuário / permissões por funcionário
- Trocar a planilha Excel por um banco de dados
- Testes automatizados
- Integração com leitor de código de barras físico (a arquitetura já contempla essa evolução — o leitor simula teclado + Enter, o que já é o comportamento esperado pelo campo de escaneamento)