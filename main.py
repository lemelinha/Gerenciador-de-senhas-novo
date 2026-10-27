import customtkinter as ctk

from config import *
from commands import PasswordManagerCommands
from notification import NotificationPopup
import os

class App(ctk.CTk):
    """Janela principal do gerenciador de senhas.

    Toda a parte visual está construída. As ações dos botões chamam os
    métodos de `PasswordManagerCommands`, que estão vazios para implementação.
    """

    def __init__(self):
        super().__init__()

        self.title(MAIN_WINDOW_TITLE)
        center_window(self, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.resizable(False, False)

        # Variáveis e widgets que a lógica vai utilizar
        self.length_var = ctk.IntVar(value=DEFAULT_PASSWORD_LENGTH)
        self.generated_password_var = ctk.StringVar()
        self.password_name_var = ctk.StringVar()
        self.selected_password_var = ctk.StringVar(value="Selecione uma senha")
        self.password_entry = None
        self.name_entry = None
        self.saved_combo = None
        self.saved_password_box = None

        # Referência ao pop-up de notificação atual
        # (precisa existir antes de qualquer notificação)
        self._notification = None

        # Camada de lógica (métodos vazios, prontos para implementação)
        self.commands = PasswordManagerCommands(self)

        self._build_ui()

        # Carrega as senhas depois que a interface já foi criada
        self.commands.carregar_senhas_salvas()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 4))

        ctk.CTkLabel(
            header,
            text=MAIN_WINDOW_TITLE,
            font=FONT_TITLE,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Gere, salve e organize suas senhas com segurança.",
            font=FONT_SMALL,
            text_color=COLOR_MUTED,
        ).pack(anchor="w", pady=(2, 0))

    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=(8, 24))

        body.grid_columnconfigure(0, weight=3, uniform="cards")
        body.grid_columnconfigure(1, weight=2, uniform="cards")
        body.grid_rowconfigure(0, weight=1)

        self._build_generator_card(body)
        self._build_saved_card(body)

    def _build_generator_card(self, parent):
        card = ctk.CTkFrame(parent, corner_radius=CORNER_RADIUS)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(
            card,
            text="Gerar senha",
            font=FONT_SECTION,
        ).pack(anchor="w", padx=20, pady=(18, 14))

        # Tamanho da senha
        ctk.CTkLabel(
            card,
            text="Tamanho da senha",
            font=FONT_BODY,
        ).pack(anchor="w", padx=20)

        size_row = ctk.CTkFrame(card, fg_color="transparent")
        size_row.pack(fill="x", padx=20, pady=(6, 16))

        self.length_slider = ctk.CTkSlider(
            size_row,
            from_=12,
            to=30,
            number_of_steps=18,
            variable=self.length_var,
            command=self._on_length_change,
        )
        self.length_slider.pack(side="left", fill="x", expand=True)

        self.length_label = ctk.CTkLabel(
            size_row,
            text="16",
            width=32,
            font=FONT_BODY_BOLD,
        )
        self.length_label.pack(side="left", padx=(10, 0))

        # Senha gerada
        ctk.CTkLabel(
            card,
            text="Senha gerada",
            font=FONT_BODY,
        ).pack(anchor="w", padx=20)

        self.password_entry = ctk.CTkEntry(
            card,
            height=40,
            font=FONT_MONO,
            textvariable=self.generated_password_var,
            state="normal",
        )
        self.password_entry.pack(fill="x", padx=20, pady=(6, 16))

        # Nome da senha
        ctk.CTkLabel(
            card,
            text="Nome da senha",
            font=FONT_BODY,
        ).pack(anchor="w", padx=20)

        self.name_entry = ctk.CTkEntry(
            card,
            height=40,
            textvariable=self.password_name_var,
            placeholder_text="Ex.: Gmail, GitHub, Banco...",
        )
        self.name_entry.pack(fill="x", padx=20, pady=(6, 20))

        # Botões
        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            buttons,
            text="Gerar senha",
            height=40,
            command=self.commands.gerar_senha,
        ).pack(fill="x", pady=(0, 10))

        actions = ctk.CTkFrame(buttons, fg_color="transparent")
        actions.pack(fill="x")
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
            text="Salvar",
            height=38,
            fg_color=COLOR_SUCCESS,
            hover_color=COLOR_SUCCESS_HOVER,
            command=self.commands.salvar_senha,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _build_saved_card(self, parent):
        card = ctk.CTkFrame(parent, corner_radius=CORNER_RADIUS)
        card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(
            card,
            text="Minhas senhas",
            font=FONT_SECTION,
        ).pack(anchor="w", padx=20, pady=(18, 14))

        ctk.CTkLabel(
            card,
            text="Selecione uma senha salva",
            font=FONT_BODY,
        ).pack(anchor="w", padx=20)

        self.saved_combo = ctk.CTkComboBox(
            card,
            values=["Selecione uma senha"],
            variable=self.selected_password_var,
            state="readonly",
            height=40,
            command=self.set_saved_password,
        )
        self.saved_combo.pack(fill="x", padx=20, pady=(6, 20))

        # Caixa de texto com a senha da opção selecionada
        password_panel = ctk.CTkFrame(card, fg_color=("gray90", "gray17"), corner_radius=10)
        password_panel.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(
            password_panel,
            text="Senha",
            font=FONT_BODY_BOLD,
        ).pack(anchor="w", padx=14, pady=(12, 6))

        self.saved_password_box = ctk.CTkTextbox(
            password_panel,
            font=FONT_MONO,
            wrap="char",
            height=64,
        )
        self.saved_password_box.pack(fill="x", padx=14, pady=(0, 14))
        self.saved_password_box.configure(state="disabled")

        # Espaçador para manter os botões no rodapé do card
        ctk.CTkFrame(card, fg_color="transparent", height=1).pack(fill="both", expand=True)

        ctk.CTkButton(
            card,
            text="Ver detalhes",
            height=38,
            command=self.commands.ver_senha,
        ).pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkButton(
            card,
            text="Excluir",
            height=38,
            fg_color="transparent",
            border_width=1,
            border_color=COLOR_DANGER,
            text_color=COLOR_DANGER,
            hover_color=COLOR_GHOST_HOVER,
            command=self.commands.excluir_senha,
        ).pack(fill="x", padx=20, pady=(0, 20))

    # ------------------------------------------------------------------
    # Callback visual do slider
    # ------------------------------------------------------------------
    def _on_length_change(self, value):
        self.length_label.configure(text=str(int(float(value))))

    # ------------------------------------------------------------------
    # Exibição da senha salva
    # ------------------------------------------------------------------
    def set_saved_password(self, nome=None):
        nome = self.selected_password_var.get()

        senha = self.commands.senhas_salvas.get(nome, "")

        self.saved_password_box.configure(state="normal")
        self.saved_password_box.delete("1.0", "end")

        self.saved_password_box.insert("1.0", senha)

        self.saved_password_box.configure(state="disabled")

    # ------------------------------------------------------------------
    # Notificações
    # ------------------------------------------------------------------
    def show_notification(self, message, success=True):
        """Exibe um pop-up de aviso no canto da janela.

        Use `success=False` para uma notificação de erro (vermelha).
        """
        if self._notification is not None and self._notification.winfo_exists():
            self._notification.destroy()

        self._notification = NotificationPopup(self, message, success=success)


if __name__ == "__main__":
    if not os.path.exists(DEFAULT_PASSWORDS_FILE):
        with open(DEFAULT_PASSWORDS_FILE, "w") as f:
            f.write("")

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = App()
    app.mainloop()
