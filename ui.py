import customtkinter as ctk
from service import VendaService
from exceptions import ProdutoNaoEncontradoException

class App:
    
    """
    Interface gráfica do ComunaStore (CustomTkinter).
    Responsabilidade única desta camada: mostrar dados e capturar eventos
    (cliques, Enter). Toda regra de negócio fica no VendaService — esta
    classe nunca calcula nada sozinha, só delega.
    """
    
    def __init__(self):
        
        # VendaService já carrega o estoque inteiro em memória na criação.
        # Isso evita reabrir a planilha a cada operação (só volta a tocar
        # no arquivo físico quando uma venda é finalizada).
        self.vs = VendaService()
        
        self.app = ctk.CTk()
        self.app.title("ComunaStore")
        self.app.geometry("800x500")
        self.app.iconbitmap("icone.ico")
        ctk.set_appearance_mode("light")
        
        # Fontes centralizadas aqui e reaproveitadas nos widgets — evita
        # recriar CTkFont repetidas vezes e facilita trocar o estilo geral
        # mudando em um lugar só.
        self.fonte_titulo = ctk.CTkFont(family='Arial', size=40, weight="bold")
        self.fonte_botao = ctk.CTkFont(family='Arial', size=20, weight="bold")
        self.fonte_campo = ctk.CTkFont(family='Arial', size=14, weight="normal", slant="italic")
        self.fonte_texto = ctk.CTkFont(family='Arial', size=12)
        self.fonte_tabela = ctk.CTkFont(family='Consolas', size=13)
        self.fonte_tabela_negrito = ctk.CTkFont(family='Consolas', size=13, weight="bold")
        self.fonte_total = ctk.CTkFont(family='Arial', size=28, weight="bold")
        self.fonte_status = ctk.CTkFont(family='Arial', size=14, weight="bold", slant="italic")
        
        # --- Tela Inicial ---
        # grid com linhas 0 e 3 "vazias" (weight=1) funcionando como molas
        # que empurram o conteúdo (linhas 1 e 2) para o centro da tela.
        self.tela_inicial = ctk.CTkFrame(self.app, fg_color="#F5F5F5")
        self.tela_inicial.grid_rowconfigure(0, weight=1)
        self.tela_inicial.grid_rowconfigure(1, weight=0)
        self.tela_inicial.grid_rowconfigure(2, weight=0)
        self.tela_inicial.grid_rowconfigure(3, weight=1)
        self.tela_inicial.grid_columnconfigure(0, weight=1)
        self.tela_inicial.pack(fill="both", expand=True)
        
        # --- Tela de Venda ---
        # Criada aqui mas só é "pacada" (exibida) em ao_clicar_iniciar —
        # as duas telas dividem a mesma janela e nunca ficam visíveis
        # ao mesmo tempo (uma é sempre escondida com pack_forget()).
        self.tela_venda = ctk.CTkFrame(self.app, fg_color="#F5F5F5")
        
        self.tela_consulta = ctk.CTkFrame(self.app, fg_color="#F5F5F5")
        
        # Cabeçalho da "tabela" de itens, calculado uma única vez (é sempre
        # o mesmo texto) e reinserido a cada redesenho da caixa_itens.
        self.cabecalho = f"{'Cód':<8}{'Descrição':<30}{'Qtd':>4}{'Vl.Unit':>10}{'Vl.Total':>10}\n"
        
        self.frame_botoes_inicial = ctk.CTkFrame(self.tela_inicial, fg_color="transparent")
        self.frame_botoes_inicial.grid(row=2, column=0)
        
        self.label_boas_vindas = ctk.CTkLabel(
            self.tela_inicial, 
            text="Bem-Vindo(a) à ComunaStore!", 
            font=self.fonte_titulo
        )
        self.label_boas_vindas.grid(row=1, column=0, pady=(0, 20))
        
        self.botao_iniciar_venda = ctk.CTkButton(
            self.frame_botoes_inicial, 
            text="Iniciar Venda", 
            command=self.ao_clicar_iniciar, 
            fg_color="#1E3A5F", 
            text_color="#FFFFFF", 
            hover_color="#2E5480", 
            corner_radius=12, 
            font=self.fonte_botao
        )
        self.botao_iniciar_venda.pack(side="left", padx=10)
        
        self.botao_consultar_preco = ctk.CTkButton(
            self.frame_botoes_inicial,
            text="Consultar Preço",
            command=self.ao_clicar_consulta,
            fg_color="#D9D9D9",
            text_color="#1A1A1A",
            hover_color="#C4C4C4",
            corner_radius=12,
            font=self.fonte_botao
        )
        self.botao_consultar_preco.pack(side="left", padx=10)
        
        self.caixa_itens = ctk.CTkTextbox(
            self.tela_venda, 
            width=480, 
            height=150,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            corner_radius=8,
            font=self.fonte_tabela
        )
        self.caixa_itens.pack(pady=10)
        self.caixa_itens._textbox.tag_config("negrito", font=self.fonte_tabela_negrito)
        
        self.label_status = ctk.CTkLabel(
            self.tela_venda, 
            text="",
            text_color="#FA2400",
            font=self.fonte_status
        )
        self.label_status.pack(pady=5)
        
        self.campo_codigo = ctk.CTkEntry(
            self.tela_venda, 
            placeholder_text="Escaneie o Código",
            fg_color="#FFFFFF",
            border_color="#1E3A5F",
            border_width=2,
            text_color="#1A1A1A",
            font=self.fonte_campo
        )
        self.campo_codigo.pack(pady=10)
        self.campo_codigo.bind("<Return>", self.ao_escanear)
        
        self.label_total = ctk.CTkLabel(
            self.tela_venda,
            text="",
            font=self.fonte_total,
            text_color="#1E3A5F"
        )
        
        self.botao_voltar_tela_inicial = ctk.CTkButton(
            self.tela_venda, 
            text="Voltar a Tela Inicial", 
            command=self.ao_voltar_tela_inicial,
            fg_color="#D9D9D9",
            text_color="#1A1A1A",
            hover_color="#C4C4C4"
        )
        
        self.botao_finalizar = ctk.CTkButton(
            self.tela_venda, 
            text="Finalizar Venda", 
            command=self.ao_finalizar,
            fg_color="#1E3A5F",
            hover_color="#2E5480",
            text_color="#FFFFFF",
            corner_radius=12,
            font=self.fonte_botao
        )
        self.botao_finalizar.pack(pady=10)
        
        self.campo_codigo_consulta = ctk.CTkEntry(
            self.tela_consulta,
            placeholder_text="Escaneie o Código",
            font=self.fonte_campo
        )
        self.campo_codigo_consulta.pack(pady=20)
        self.campo_codigo_consulta.bind("<Return>", self.ao_consultar)
        
        self.label_resultado_consulta = ctk.CTkLabel(
            self.tela_consulta, 
            text="", 
            font=self.fonte_total, 
            text_color="#1E3A5F"
        )
        self.label_resultado_consulta.pack(pady=20)

        self.botao_voltar_consulta = ctk.CTkButton(
            self.tela_consulta, 
            text="Voltar a Tela Inicial", 
            command=self.ao_voltar_consulta, 
            fg_color="#D9D9D9", 
            text_color="#1A1A1A"
        )
        self.botao_voltar_consulta.pack(pady=10)

    def formatar_linha_item(self, item):
        """Formata um ItemVenda como uma linha de "recibo" (colunas alinhadas).
        Fica na ui.py (não no __str__ do model) porque essa formatação é
        específica de exibição na tela — o __str__ do ItemVenda continua
        simples/neutro, útil em qualquer contexto (ex: terminal).
        """
        linha = f"{item.produto.codigo:<8}{item.produto.nome:<30}{item.quantidade:>4}{item.produto.preco:>10.2f}{item.calcula_subtotal():>10.2f}"
        return linha

    def ao_clicar_iniciar(self):
        # Inicia a venda "de verdade" na lógica (service) e só então troca
        # a tela — as duas ações sempre andam juntas nesse método.
        self.vs.iniciar_venda()
        self.tela_inicial.pack_forget()
        self.label_total.pack_forget() # garante que não sobrou visível de uma venda anterior
        self.tela_venda.pack(fill="both", expand=True)
        self.caixa_itens.delete("1.0", "end")
        self.label_status.configure(text="")
        self.label_status.pack(pady=5)
        
        self.caixa_itens.insert("end", self.cabecalho, "negrito")
        
    def ao_escanear(self, event):
        # event é obrigatório aqui porque esta função está conectada via
        # .bind() (diferente de command=, que não passa argumento nenhum).
        text = self.campo_codigo.get()

        try:
            self.vs.processar_codigo(text)

            self.label_status.configure(text="")
            # Redesenha a caixa inteira a partir dos dados reais, em vez de
            # só inserir a última linha — necessário porque escanear um
            # código repetido ATUALIZA um item existente, não cria um novo
            # (então "inserir só o último" mostraria o item errado).
            self.caixa_itens.delete("1.0", "end")
            self.caixa_itens.insert("end", self.cabecalho, "negrito")
            for item in self.vs.venda_atual.itens:
                self.caixa_itens.insert("end", self.formatar_linha_item(item) + "\n")

        except ProdutoNaoEncontradoException as e:
            # Erro tratado aqui, não deixado "vazar" — impede que a venda
            # inteira trave por causa de um código de leitura inválido.
            self.label_status.configure(text=str(e))

        self.campo_codigo.delete(0, "end")
    
    def ao_voltar_tela_inicial(self):
        self.tela_venda.pack_forget()
        self.label_total.pack_forget()
        self.tela_inicial.pack(fill="both", expand=True)
        # Reverte a troca de elementos feita em ao_finalizar, preparando
        # a tela de venda para a PRÓXIMA venda (senão campo/botão de
        # finalizar continuariam escondidos e o botão voltar continuaria
        # visível por engano).
        self.botao_voltar_tela_inicial.pack_forget()
        self.campo_codigo.pack(pady=20)
        self.botao_finalizar.pack(pady=10)
        
    def ao_finalizar(self):
        # finaliza_venda() já cuida de calcular o total, dar baixa no
        # estoque e salvar a planilha — aqui só usamos o retorno (total)
        # para atualizar a tela.
        total = self.vs.finaliza_venda()
        self.label_total.configure(text=f"Total: R${total:.2f}")
        self.label_total.pack()
        # Esconde o que só faz sentido DURANTE o escaneamento — evita que
        # o funcionário tente escanear mais itens numa venda já fechada.
        self.campo_codigo.pack_forget()
        self.botao_finalizar.pack_forget()
        self.label_status.pack_forget()
        self.botao_voltar_tela_inicial.pack(pady=10)

    def ao_clicar_consulta(self):
        self.tela_inicial.pack_forget()
        self.tela_consulta.pack(fill="both", expand=True)
    
    def ao_consultar(self, event):
        texto = self.campo_codigo_consulta.get()
        try:
            produto = self.vs.buscar_produto(texto)
            self.label_resultado_consulta.configure(text=f"{produto.nome} — R${produto.preco:.2f}")
        except ProdutoNaoEncontradoException as e:
            self.label_resultado_consulta.configure(text=str(e))
        
        self.campo_codigo_consulta.delete(0, "end")
            
    def ao_voltar_consulta(self):
        self.tela_consulta.pack_forget()
        self.tela_inicial.pack(fill="both", expand=True)
        self.label_resultado_consulta.configure(text="")
            

    def rodar(self):
        # mainloop() bloqueia aqui até a janela ser fechada — por isso é
        # sempre a última linha a rodar, depois de todos os widgets já
        # criados e posicionados.
        self.app.mainloop()

app = App()
app.rodar()