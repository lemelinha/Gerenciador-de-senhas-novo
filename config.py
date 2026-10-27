"""Configurações globais de aparência, dimensões e fontes da aplicação."""

APPEARANCE_MODE = "dark"
COLOR_THEME = "dark-blue"

MAIN_WINDOW_WIDTH = 720
MAIN_WINDOW_HEIGHT = 560
MAIN_WINDOW_TITLE = "Gerenciador de Senhas"

CORNER_RADIUS = 12

DEFAULT_PASSWORDS_FILE = "senhas.txt"
DEFAULT_PASSWORD_LENGTH = 16
CHARACTER_SET = r"abcdefghijklmnopqrstuvwxyzçABCDEFGHIJKLMNOPQRSTUVWXYZÇ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/"

# Fontes
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 24, "bold")
FONT_SECTION = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_BODY_BOLD = (FONT_FAMILY, 13, "bold")
FONT_SMALL = (FONT_FAMILY, 12)
FONT_MONO = ("Consolas", 15)

# Cores
COLOR_MUTED = ("gray45", "gray60")
COLOR_SUCCESS = "#2FA572"
COLOR_SUCCESS_HOVER = "#2A8C63"
COLOR_DANGER = "#D25C5C"
COLOR_DANGER_HOVER = "#B34A4A"
COLOR_GHOST_HOVER = ("gray85", "gray24")
COLOR_BORDER = ("gray70", "gray35")


def center_window(window, width, height):
    """Centraliza uma janela na tela."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
