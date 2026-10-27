import customtkinter as ctk

import config as cfg


class NotificationPopup(ctk.CTkToplevel):
    """Pop-up (toast) não bloqueante, exibido no canto da janela principal.

    Fecha sozinho após alguns segundos ou ao ser clicado.
    """

    WIDTH = 290
    HEIGHT = 62
    MARGIN = 24
    DURATION_MS = 2200

    def __init__(self, master, message, success=True, duration=DURATION_MS):
        super().__init__(master)

        self.withdraw()  # evita aparecer no centro antes de posicionar
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(False, False)

        color = cfg.COLOR_SUCCESS if success else cfg.COLOR_DANGER
        icon = "✓" if success else "!"

        self.configure(fg_color=color)

        label = ctk.CTkLabel(
            self,
            text=f"{icon}  {message}",
            font=cfg.FONT_BODY_BOLD,
            text_color="#FFFFFF",
            wraplength=self.WIDTH - 32,
            justify="left",
        )
        label.pack(fill="both", expand=True, padx=16, pady=12)

        label.bind("<Button-1>", lambda _event: self.destroy())
        self.bind("<Button-1>", lambda _event: self.destroy())

        self._position_over_master(master)
        self.deiconify()
        self.lift()

        self.after(duration, self._safe_destroy)

    def _position_over_master(self, master):
        """Posiciona o toast no canto inferior direito da janela principal."""
        master.update_idletasks()
        x = master.winfo_rootx() + master.winfo_width() - self.WIDTH - self.MARGIN
        y = master.winfo_rooty() + master.winfo_height() - self.HEIGHT - self.MARGIN
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def _safe_destroy(self):
        if self.winfo_exists():
            self.destroy()
