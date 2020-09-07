from tkinter import *
from design import DesignPrograma

class ContatoFrame(Frame):
    def __init__(self, master=None, info=None, parent=None):
        super().__init__(master)
        self.design = DesignPrograma()
        self.imagem_alterar = PhotoImage(master=self, file="icones/icons8-informações-40.png")
        self.imagem_deletar = PhotoImage(master=self, file="icones/icons8-delete-40.png")
        self.info = info
        self.parent = parent
        self.componentes()

    def componentes(self):
        self["bg"] = "#87CEFA"
        self["borderwidth"] = 3
        self["relief"] = "ridge"

        self.label_nome = Label(self,
                                text=self.info["nome"],
                                width=30,
                                borderwidth=self.design.tamanho_borda_label,
                                relief=self.design.estilo_borda_label,
                                bg=self.design.cor_fundo_label)

        self.label_nome.config(font=(10))
        self.label_nome.grid(row=0, column=0)

        self.btn_alterar = Button(self, text="Alterar",
                                  command=self.alterar,
                                  bg=self.design.cor_fundo_botao,
                                  borderwidth=self.design.tamanho_borda_botao)

        self.btn_alterar.config(image=self.imagem_alterar)
        self.btn_alterar.grid(row=0, column=1)

        self.btn_deletar = Button(self,
                                  text="X",
                                  command=self.deletar,
                                  bg=self.design.cor_fundo_botao,
                                  borderwidth=self.design.tamanho_borda_botao)

        self.btn_deletar.config(image=self.imagem_deletar)
        self.btn_deletar.grid(row=0, column=2)

    def deletar(self):
        self.parent.deletar_contato(self.info["id"])

    def alterar(self):
        self.parent.alterar_contato(self.info["id"])


