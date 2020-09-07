# !/usr/bin/env python
# -*- coding: utf-8 -*-
#Existe algo chamado protocolo que decide o que acontecerá quando o programa será fechado, é possível manipular esse protoco com
#o método self.protocol. É também a interação entre o aplicativo e o gerenciador de tarefas, manipulador de protocolo.

from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from leitura_escrita import EscritaJson
from leitura_escrita import LeituraJson
from leitura_escrita import CriarDiretorio
from componentes_internos import ContatoFrame
from design import DesignPrograma

design = DesignPrograma()

class TelaBase(Tk):
    def __init__(self):
        super().__init__()
        self.menu_bar()
        self["bg"] = design.cor_fundo_main
        self["relief"] = design.estilo_borda_main
        self["borderwidth"] = design.tamanho_borda_main

    def menu_bar(self):
        self.menu_bar = Menu(self)    #primeiro é necessário criar  uma iinstância de Menu
        self.sub_menu_arquivo = Menu(self.menu_bar, tearoff=0)  #tear off desabilita a criação do menu flutuante ao clicar no pontilhado
        self.sub_menu_arquivo.add_command(label='Novo', command=lambda: self.new_file())
        self.sub_menu_arquivo.add_command(label='Abrir', command=lambda: self.open_file())
        self.sub_menu_arquivo.add_command(label='Sair', command=lambda: self.msg_box())
        self.sub_menu_info = Menu(self.menu_bar, tearoff=0)
        self.sub_menu_info.add_command(label='Info', command=self.janela_info)
        self.menu_bar.add_cascade(label='Arquivo', menu=self.sub_menu_arquivo)
        self.menu_bar.add_cascade(label="Ajuda", menu=self.sub_menu_info)
        self.config(menu=self.menu_bar)
        self.protocol("WM_DELETE_WINDOW", self.msg_box)

    def msg_box(self):
        msg_box_sair = messagebox.askquestion("Sair", "Você deseja mesmo sair?", parent=self, icon="question")
        if msg_box_sair == 'yes':
            self.destroy()

    def janela_info(self):
        janela = JanelaVersao()

    def open_file(self):
        arquivo = filedialog.askopenfile(title="Abrir Lista de Contatos",
                                         filetypes=[("JSON", ".json")],
                                         parent=self)

        if arquivo is not None:
            self.destroy()
            self.abrir_tela_agenda(arquivo.name)

    def new_file(self):
        arquivo = filedialog.asksaveasfile(title="Salvar Lista de Contatos",
                                           filetypes=[("JSON", ".json")],
                                           parent=self)

        if arquivo is not None:
            self.salvar_nova_lista_telefonica(arquivo.name)

    def abrir_tela_agenda(self, dir):
        self.tela_agenda = TelaAgenda(dir)

    def salvar_nova_lista_telefonica(self, dir):
        escrita = EscritaJson(dir)
        escrita.alterar_nova_lista()


class TelaInicial(TelaBase):
    def __init__(self):
        super().__init__()
        self.imagem_novo = PhotoImage(master=self, file="icones/icons8-document-120.png")
        self.imagem_abrir = PhotoImage(master=self, file="icones/icons8-opened-folder-120.png")

        self.title("Agenda Eletrônica")
        self.resizable(width=0, height=0)
        self.carregar_widgets()
        self.geometry("500x500")
        self.parent_window = self
        self.criar_diretorio()
        self.mainloop()

    def carregar_widgets(self):
        self.frame_superior = Frame(self, pady=30, bg=design.cor_fundo)
        self.frame_inferior = Frame(self, pady=80, padx=80, bg=design.cor_fundo)

        self.frame_superior.pack()
        self.frame_inferior.pack(fill=X)

        self.font_cabecalho = font.Font(size=design.tamanho_titulo, family=design.font_titulo)
        self.lbl_cabecalho = Label(self.frame_superior,
                                   text="Agenda Telefônica 0.1",
                                   borderwidth=design.tamanho_borda_label,
                                   relief=design.estilo_borda_label,
                                   bg=design.cor_fundo_label)

        self.lbl_cabecalho.configure(font=self.font_cabecalho)
        self.lbl_cabecalho.pack()

        self.btn_adicionar = Button(self.frame_inferior,
                                    image=self.imagem_novo,
                                    bg=design.cor_fundo_botao,
                                    borderwidth=design.tamanho_borda_botao,
                                    command=lambda: self.new_file())

        self.btn_adicionar.bind("<Leave>", self.gritar)
        self.btn_adicionar.bind("<Enter>", self.gritar)

        self.btn_agenda = Button(self.frame_inferior,
                                 image=self.imagem_abrir,
                                 bg=design.cor_fundo_botao,
                                 borderwidth=design.tamanho_borda_botao,
                                 command=lambda: self.open_file())

        self.btn_adicionar.pack(side="left")
        self.btn_agenda.pack(side="right")

    def gritar(self, event):
        print("AAAAH!")

    def limpar_input(self):
        self.input_nome.delete(0, END)
        self.input_endereco.delete(0, END)
        self.input_telefone.delete(0, END)
        self.input_email.delete(0, END)

    def criar_diretorio(self):
        new_dir = CriarDiretorio("Contatos")
        if new_dir.criar_diretorio():
            messagebox.showinfo("Configuração", "Criado novo diretório de contatos!")




class TelaAgenda(TelaBase):
    def __init__(self, dir):
        super().__init__()
        self.imagem_adicionar = PhotoImage(master=self, file="icones/icons8-plus-40.png")
        self.imagem_buscar = PhotoImage(master=self, file="icones/icons8-search-40.png")
        self.imagem_salvar = PhotoImage(master=self, file="icones/icons8-briefcase-40.png")


        self.title("Agenda Aberta")
        self.resizable(width=0, height=0)
        self.dir = dir
        self.leitura_agenda = LeituraJson(dir)
        self.carregar_widgets()
        self.geometry("500x500")

    def carregar_widgets(self):
        self.superior = Frame(self, bg=design.cor_fundo)
        self.central = Frame(self, pady=30, bg=design.cor_fundo)
        self.inferior = Frame(self, pady=30, bg=design.cor_fundo)

        self.superior.pack()
        self.central.pack()
        self.inferior.pack()

        self.lbl_cabecalho = Label(self.superior,
                                   text="Agenda Aberta",
                                   borderwidth=design.tamanho_borda_label,
                                   relief=design.estilo_borda_label,
                                   bg="#00BFFF")

        self.lbl_cabecalho.config(font=(design.estilo_borda_label, design.tamanho_titulo))
        self.lbl_cabecalho.pack()

        self.main_frame = Frame(self.central)
        self.canvas_contato = Canvas(self.main_frame, borderwidth = 5, bg="#ffffff")
        self.frame_contato = Frame(self.canvas_contato, bg="#ffffff")

        #self.scroll_bar_horizontal = Scrollbar(self.main_frame, orient="horizontal")
        #self.scroll_bar_horizontal.pack(side=BOTTOM, fill=X)

        self.scroll_bar_vertical = Scrollbar(self.main_frame,
                                             orient="vertical",
                                             command=self.canvas_contato.yview,
                                             width=20)

        self.canvas_contato.configure(yscrollcommand=self.scroll_bar_vertical.set)
        self.scroll_bar_vertical.pack(side=RIGHT, fill=Y)
        self.canvas_contato.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_contato.create_window((4,4), window=self.frame_contato, anchor="nw", tags="self.frame_contato")

        self.frame_contato.bind("<Configure>",
                                self.blabla)
        self.main_frame.pack()

        self.btn_buscar = Button(self.inferior,
                                 text="Buscar",
                                 image=self.imagem_buscar,
                                 bg=design.cor_fundo_botao,
                                 borderwidth=design.tamanho_borda_botao)

        self.btn_buscar.config(state="disabled")
        self.btn_buscar.pack(side=RIGHT)

        self.btn_adicionar = Button(self.inferior,
                                    image=self.imagem_adicionar,
                                    bg=design.cor_fundo_botao,
                                    borderwidth=design.tamanho_borda_botao,
                                    command=self.adicionar_contato)

        self.btn_adicionar.pack(side=RIGHT)

        self.btn_salvar = Button(self.inferior,
                                 image=self.imagem_salvar,
                                 bg=design.cor_fundo_botao,
                                 borderwidth=design.tamanho_borda_botao,
                                 command=self.salvar_modificacao)

        self.btn_salvar.pack(side=RIGHT)

        self.leitura_agenda.ler_json()
        self.atualizar_lista_contatos()

    def blabla(self, event):
        self.canvas_contato.configure(scrollregion=self.canvas_contato.bbox("all"))

    def atualizar_lista_contatos(self):
        self.clear_frame_contato()
        for row in range(len(self.leitura_agenda.arquivo_lido)):
            dados = self.leitura_agenda.arquivo_lido[row]
            ContatoFrame(self.frame_contato,
                         info=dados,
                         parent=self,
                         ).grid(row=row, column=0)

    def clear_frame_contato(self):
            frame_contato = self.frame_contato.grid_slaves()
            for widget in frame_contato:
                widget.destroy()

    def localizar_id_lista(self, id):
        for index, contato in enumerate(self.leitura_agenda.arquivo_lido):
            if contato["id"] == id:
                return index

    def salvar_modificacao(self):
        arquivo = EscritaJson(self.dir)
        arquivo.arquivo_escrito = self.leitura_agenda.arquivo_lido
        arquivo.atualizar()
        messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso", parent=self)

    def deletar_contato(self, id):
        index = self.localizar_id_lista(id)
        del self.leitura_agenda.arquivo_lido[index]
        self.atualizar_lista_contatos()

    def inserir_contato(self, contato):
        self.leitura_agenda.arquivo_lido.append(contato)
        self.atualizar_lista_contatos()

    def adicionar_contato(self):
        janela = JanelaContato(parent=self)
        janela.mainloop()

    def alterar_contato(self, id):
        for index, contato in enumerate(self.leitura_agenda.arquivo_lido):
            if contato["id"] == id:
                janela = JanelaContatoAlterar(self, contato)
                janela.mainloop()

    def atualizar_contato(self, contato):
        id = contato["id"]
        nome = contato["nome"]
        endereco = contato["endereco"]
        telefone = contato["telefone"]
        email = contato["email"]

        index = self.localizar_id_lista(id)
        self.leitura_agenda.arquivo_lido[index]["nome"] = nome
        self.leitura_agenda.arquivo_lido[index]["endereco"] = endereco
        self.leitura_agenda.arquivo_lido[index]["telefone"] = telefone
        self.leitura_agenda.arquivo_lido[index]["email"] = email
        self.atualizar_lista_contatos()

class JanelaVersao(Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.title("Informação")
        self.resizable(width=0, height=0)
        self.carregar_widgets()
        self.geometry("400x300")
        self.mainloop()

    def carregar_widgets(self):
        self["bg"] = "#87CEFA"
        self["borderwidth"] = 8
        self["relief"] = "ridge"

        text = "Agenda telefônica criada para \nfins didáticos\nVersão 0.1\nCriada por Felipe Matheus"
        self.superior = Frame(self, pady=20, relief=design.estilo_borda, bg=design.cor_fundo)
        self.central = Frame(self, pady=20, relief=design.estilo_borda, bg=design.cor_fundo)
        self.inferior = Frame(self, pady=30, relief=design.estilo_borda, bg=design.cor_fundo)

        self.superior.pack()
        self.central.pack()
        self.inferior.pack()

        self.label_info = Label(self.superior,
                                text="Informações",
                                borderwidth=design.tamanho_borda_label,
                                relief=design.estilo_borda_label,
                                bg=design.cor_fundo_label)

        self.label_info.config(font=(design.font_titulo, design.tamanho_titulo))
        self.label_info.pack()

        self.label_info = Label(self.central,
                                text=text,
                                borderwidth=design.tamanho_borda_label,
                                relief=design.estilo_borda_label,
                                bg=design.cor_fundo_label)

        self.label_info.config(font=design.tamanho_txt)
        self.label_info.pack()

        self.btn_ok = Button(self.inferior,
                             text="Okay",
                             bg=design.cor_fundo_botao,
                             borderwidth=design.tamanho_borda_botao,
                             command=self.destroy)

        self.btn_ok.config(font=design.tamanho_txt)
        self.btn_ok.pack()

class JanelaContato(Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.imagem_ok = PhotoImage(master=self, file="icones/ok.gif")
        self.imagem_fechar = PhotoImage(master=self, file="icones/icons8-unavailable-40.png")
        self.parent = parent
        self.title("Contato")
        self.resizable(width=0, height=0)
        self.carregar_widgets()
        self.geometry("400x400")
        self.grab_set()

    def carregar_widgets(self):
        self["bg"] = design.cor_fundo_main
        self["relief"] = design.estilo_borda_main
        self["borderwidth"] = design.tamanho_borda_main

        self.superior = Frame(self, pady=20, bg=design.cor_fundo)
        self.nome = Frame(self, pady=10, padx=80, bg=design.cor_fundo)
        self.endereco = Frame(self, pady=10, padx=80, bg=design.cor_fundo)
        self.telefone = Frame(self, pady=10, padx=80, bg=design.cor_fundo)
        self.email = Frame(self, pady=10, padx=80, bg=design.cor_fundo)
        self.botoes = Frame(self, pady=30, bg=design.cor_fundo)

        self.label_contato = Label(self.superior,
                                   text="Novo Contato",
                                   borderwidth=design.tamanho_borda_label,
                                   relief=design.estilo_borda_label,
                                   bg=design.cor_fundo_label)

        self.label_contato.config(font=(design.font_titulo, design.tamanho_titulo))
        self.label_contato.pack()

        self.superior.pack()
        self.nome.pack(fill=BOTH)
        self.endereco.pack(fill=BOTH)
        self.telefone.pack(fill=BOTH)
        self.email.pack(fill=BOTH)
        self.botoes.pack()

        self.label_nome = Label(self.nome,
                                text="Nome:",
                                borderwidth=design.tamanho_borda_label,
                                relief=design.estilo_borda_label,
                                bg=design.cor_fundo_label,
                                font=design.tamanho_txt)

        self.label_endereco = Label(self.endereco,
                                    text="Endereço:",
                                    borderwidth=design.tamanho_borda_label,
                                    relief=design.estilo_borda_label,
                                    bg=design.cor_fundo_label,
                                    font=design.tamanho_txt)

        self.label_telefone = Label(self.telefone,
                                    text="Telefone",
                                    borderwidth=design.tamanho_borda_label,
                                    relief=design.estilo_borda_label,
                                    bg=design.cor_fundo_label,
                                    font=design.tamanho_txt)

        self.label_email = Label(self.email,
                                 text="E-mail",
                                 borderwidth=design.tamanho_borda_label,
                                 relief=design.estilo_borda_label,
                                 bg=design.cor_fundo_label,
                                 font=design.tamanho_txt)

        self.label_nome.pack(side=LEFT)
        self.label_endereco.pack(side=LEFT)
        self.label_telefone .pack(side=LEFT)
        self.label_email .pack(side=LEFT)

        self.input_nome = Entry(self.nome)
        self.input_endereco = Entry(self.endereco)
        self.input_telefone = Entry(self.telefone)
        self.input_email = Entry(self.email)

        self.input_nome.pack(side=RIGHT)
        self.input_endereco.pack(side=RIGHT)
        self.input_telefone.pack(side=RIGHT)
        self.input_email.pack(side=RIGHT)

        self.btn_ok = Button(self.botoes,
                             bg=design.cor_fundo_botao,
                             borderwidth=design.tamanho_borda_botao,
                             command=self.salvar_contato)

        self.btn_ok.config(image=self.imagem_ok)

        self.btn_fechar = Button(self.botoes,
                                 bg=design.cor_fundo_botao,
                                 borderwidth=design.tamanho_borda_botao,
                                 command=self.destroy)

        self.btn_fechar.config(image=self.imagem_fechar)

        self.btn_ok.pack(side=LEFT)
        self.btn_fechar.pack(side=LEFT)

    def salvar_contato(self):
        nome = self.input_nome.get()
        endereco = self.input_endereco.get()
        telefone = self.input_telefone.get()
        email = self.input_email.get()
        id = self.gerar_id()

        contato = {"id":id,
                   "nome":nome,
                   "endereco":endereco,
                   "telefone":telefone,
                   "email":email
                   }

        self.parent.inserir_contato(contato)
        messagebox.showinfo("Salvo com sucesso", "O contato {} foi salvo com sucesso".format(nome), parent=self)
        self.destroy()

    def gerar_id(self):
        if len(self.parent.leitura_agenda.arquivo_lido) > 0:
            id = self.parent.leitura_agenda.arquivo_lido[-1]["id"] + 1
            return id
        return 1

class JanelaContatoAlterar(JanelaContato):
    def __init__(self, parent, info):
        super().__init__(parent)
        self.info = info
        self.info_contato()

    def salvar_contato(self):
        nome = self.input_nome.get()
        endereco = self.input_endereco.get()
        telefone = self.input_telefone.get()
        email = self.input_email.get()
        id = self.info["id"]

        contato = {"id":id,
                   "nome":nome,
                   "endereco":endereco,
                   "telefone":telefone,
                   "email":email
                   }

        self.parent.atualizar_contato(contato)
        messagebox.showinfo("Alterado com sucesso", "O contato {} foi alterado com sucesso".format(nome), parent=self)
        self.destroy()

    def info_contato(self):
        id = self.info["id"]
        nome = self.info["nome"]
        endereco = self.info["endereco"]
        telefone = self.info["telefone"]
        email = self.info["email"]

        self.input_nome.insert(0, nome)
        self.input_endereco.insert(0, endereco)
        self.input_telefone.insert(0, telefone)
        self.input_email.insert(0, email)