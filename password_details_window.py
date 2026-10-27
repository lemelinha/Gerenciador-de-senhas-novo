import tkinter as tk

import customtkinter as ctk

import config as cfg


class PasswordDetailsWindow(ctk.CTkToplevel):
    """Janela para editar e copiar uma senha.

    Instância única: chamar `PasswordDetailsWindow(self.app)` novamente
    apenas traz a janela já aberta para frente, em vez de criar outra.
    As ações estão vazias para implementação.
    """

    WIDTH = 420
    HEIGHT = 380

    _instance = None

    def __new__(cls, master, commands, nome, senha):
        instance = cls._instance

        if instance is not None:
            try:
                still_open = bool(instance.winfo_exists())
            except tk.TclError:
                still_open = False

            if still_open:
                instance.deiconify()
                instance.lift()
                instance.focus_force()
                return instance

        return super().__new__(cls)

    def __init__(self, master, commands, nome, senha):
        # __new__ devolveu a janela que já estava aberta: apenas foca.
        if self is type(self)._instance:
            self.deiconify()
            self.lift()
            self.focus_force()
            return

        super().__init__(master)

        self.title("Editar senha")
        cfg.center_window(self, self.WIDTH, self.HEIGHT)
        self.resizable(False, False)

        self.name_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._build_ui()

        type(self)._instance = self
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Destroy>", self._on_destroy, add="+")

        self.lift()
        self.focus_force()
        self.after(50, self.focus_force)

        self.commands = commands
        self.nome_antigo = nome
        self.name_entry.set(nome)
        self.password_entry.set(senha)

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            container,
            text="Editar senha",
            font=cfg.FONT_SECTION,
        ).pack(anchor="w")

        ctk.CTkLabel(
            container,
            text="Nome",
            font=cfg.FONT_BODY,
        ).pack(anchor="w", pady=(16, 4))

        self.name_entry = ctk.CTkEntry(
            container,
            height=38,
            textvariable=self.name_var,
            placeholder_text="Nome da senha",
        )
        self.name_entry.pack(fill="x")

        ctk.CTkLabel(
            container,
            text="Senha",
            font=cfg.FONT_BODY,
        ).pack(anchor="w", pady=(14, 4))

        self.password_entry = ctk.CTkEntry(
            container,
            height=38,
            textvariable=self.password_var,
            placeholder_text="Senha",
        )
        self.password_entry.pack(fill="x")

        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(fill="x", pady=(20, 0))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            actions,
            text="Copiar",
            height=38,
            command=lambda: self.commands.copiar_senha(self.password_entry.get()),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="Salvar alterações",
            height=38,
            fg_color=cfg.COLOR_SUCCESS,
            hover_color=cfg.COLOR_SUCCESS_HOVER,
            command=self.salvar_nova_senha,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ctk.CTkButton(
            container,
            text="Fechar",
            height=38,
            fg_color="transparent",
            border_width=1,
            border_color=cfg.COLOR_BORDER,
            hover_color=cfg.COLOR_GHOST_HOVER,
            command=self.destroy,
        ).pack(fill="x", pady=(10, 0))

    def _on_destroy(self, event):
        if event.widget is self:
            type(self)._instance = None

    def salvar_nova_senha(self):
        if self.commands.editar_senha(self.nome_antigo, self.name_entry.get(), self.password_entry.get()) == 0:
            self.nome_antigo = self.name_entry.get()
