"""Camada de lógica do gerenciador de senhas.

A interface gráfica já está pronta e os botões chamam os métodos abaixo.
Implemente cada método substituindo o comentário "implementar aqui".

Variáveis e widgets disponíveis em `self.app` (App):

    Tamanho
        self.app.length_var             -> ctk.IntVar com o tamanho escolhido

    Senha gerada (campo somente leitura)
        self.app.generated_password_var -> ctk.StringVar da senha exibida
        self.app.password_entry         -> CTkEntry (não editável)
        Exemplo: self.app.generated_password_var.set("minhaSenha123")

    Nome da senha
        self.app.password_name_var      -> ctk.StringVar do nome digitado
        self.app.name_entry             -> CTkEntry do nome

    Senhas salvas
        self.app.selected_password_var  -> ctk.StringVar da opção selecionada
        self.app.saved_combo            -> CTkComboBox
        self.app.saved_password_box     -> CTkTextbox (somente leitura)
        Exemplo: self.app.saved_combo.configure(values=["Gmail", "GitHub"])
                 self.app.selected_password_var.set("Gmail")
                 self.app.set_saved_password("senhaDoGmail")

    Janela de detalhes
        from password_details_window import PasswordDetailsWindow
        PasswordDetailsWindow(self.app)  # abre a janela visual
"""
import os
from random import choice

from pyperclip import copy

from config import *

from password_details_window import *


class PasswordManagerCommands:
    """Concentra as ações do gerenciador de senhas."""

    def __init__(self, app):
        self.app = app
        self.senhas_salvas = {}

    def gerar_senha(self):
        senha=''
        for _ in range(self.app.length_var.get()):
            senha += choice(CHARACTER_SET)
        self.app.generated_password_var.set(senha)

    def copiar_senha(self, senha):
        senha = senha.strip()

        if not senha:
            self.app.show_notification("Nenhuma senha para copiar.", success=False)
            return

        try:
            copy(senha)
        except Exception:
            self.app.show_notification("Não foi possível copiar a senha.", success=False)
            return

        self.app.show_notification("Senha copiada!")

    def salvar_senha(self):
        nome = self.app.password_name_var.get().strip()
        senha = self.app.generated_password_var.get().strip()

        if not senha:
            self.app.show_notification('Nenhuma senha para salvar', success=False)
            return

        if not nome:
            self.app.show_notification('A senha deve possuir um nome', success=False)
            return

        if self.senha_existe(nome):
            self.app.show_notification('Já existe uma senha com esse nome', success=False)
            return

        try:
            with open(DEFAULT_PASSWORDS_FILE, 'a', encoding='utf-8') as arquivo:
                arquivo.write(nome)
                arquivo.write('\n')
                arquivo.write(senha)
                arquivo.write('\n')
        except Exception as e:
            self.app.show_notification('Não foi possível abrir o arquivo de senhas', success=False)
            print(e)
            return

        self.carregar_senhas_salvas()
        self.app.show_notification('Senha salva com successo!')

    def editar_senha(self, nome_antigo, nome, senha):
        nome = nome.strip()
        senha = senha.strip()
        if not senha:
            self.app.show_notification('Nenhuma senha para salvar', success=False)
            return -1

        if not nome:
            self.app.show_notification('A senha deve possuir um nome', success=False)
            return -1

        if  nome_antigo != nome and self.senha_existe(nome):
            self.app.show_notification('Já existe uma senha com esse nome', success=False)
            return -1

        self.senhas_salvas[nome] = self.senhas_salvas.pop(nome_antigo)
        self.senhas_salvas[nome] = senha
        content = ''
        for (nome, senha) in self.senhas_salvas.items():
            content += f'{nome}\n{senha}\n'
        try:
            with open(DEFAULT_PASSWORDS_FILE, 'w', encoding='utf-8') as arquivo:
                arquivo.write(content)
        except Exception:
            self.app.show_notification("Não foi alterar a senha!", success=False)
            return -1
        self.carregar_senhas_salvas()
        self.app.show_notification("Senha alterada com sucesso!")
        return 0


    def ver_senha(self):
        nome = self.app.selected_password_var.get()
        if not self.senha_existe(nome):
            return

        PasswordDetailsWindow(
            self.app, 
            self,
            nome,
            self.senhas_salvas[nome],
        )

    def excluir_senha(self):
        nome = self.app.selected_password_var.get()
        if not self.senha_existe(nome):
            return

        self.senhas_salvas.pop(nome)
        content = ''
        for (nome, senha) in self.senhas_salvas.items():
            content += f'{nome}\n{senha}\n'
        try:
            with open(DEFAULT_PASSWORDS_FILE, 'w', encoding='utf-8') as arquivo:
                arquivo.write(content)
        except Exception:
            self.app.show_notification("Não foi excluir a senha!", success=False)
            return
        self.app.show_notification("Senha excluída com sucesso!")

    def carregar_senhas_salvas(self):
        """Lê o arquivo .txt e preenche o dicionário e a combobox.

        Formato do arquivo: uma linha com o nome e a seguinte com a senha.
        """
        self.senhas_salvas = {}

        if not os.path.exists(DEFAULT_PASSWORDS_FILE):
            return

        try:
            with open(DEFAULT_PASSWORDS_FILE, "r", encoding="utf-8") as arquivo:
                linhas = [linha.strip() for linha in arquivo if linha.strip('\n')]
        except Exception:
            self.app.show_notification("Não foi possível carregar as senhas!", success=False)
            return

        for i in range(0, len(linhas), 2):
            self.senhas_salvas[linhas[i]] = linhas[i+1]

        senhas_lista = self.senhas_salvas.keys()
        self.app.saved_combo.configure(values=senhas_lista)

    def senha_existe(self, nome):
        if nome in self.senhas_salvas.keys():
            return True
        return False
