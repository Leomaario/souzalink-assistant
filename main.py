# main.py

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import webbrowser, re
from datetime import datetime
import sys, os # <-- Adicionado para a função "mágica"

from theme import Theme
from logic import ChatbotLogic

# --- FUNÇÃO MÁGICA PARA ENCONTRAR ARQUIVOS ---
def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ChatApplication(ctk.CTk):
    def __init__(self, logic_handler):
        super().__init__()
        
        self.logic_handler = logic_handler
        self.title("SouzaLink - Assistente de TI HRB")
        self.geometry(Theme.WINDOW_SIZE)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.attributes("-topmost", True)
        
        try:
            # --- MUDANÇA AQUI: Usa a função resource_path ---
            self.iconbitmap(resource_path("souzalink_.ico"))
        except Exception as e:
            print(f"AVISO: Ícone não encontrado. {e}")

        # --- MUDANÇA AQUI: Usa a função resource_path para os avatares ---
        self.bot_avatar = self.load_image(resource_path(Theme.BOT_AVATAR_PATH), Theme.AVATAR_SIZE)
        self.user_avatar = self.load_image(resource_path(Theme.USER_AVATAR_PATH), Theme.AVATAR_SIZE)

        if not self.bot_avatar or not self.user_avatar:
             messagebox.showwarning("Aviso", "Não foi possível encontrar uma ou mais imagens de avatares.")

        # ... o resto do seu código __init__ e da classe continua igual ...
        ctk.set_appearance_mode(Theme.APPEARANCE_MODE)
        ctk.set_default_color_theme(Theme.COLOR_THEME)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.messages_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.MAIN_BG_COLOR)
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        entry_frame.columnconfigure(0, weight=1)
        self.user_entry = ctk.CTkEntry(entry_frame, placeholder_text="Digite uma opção...", font=Theme.INPUT_FONT, height=40, corner_radius=15, fg_color=Theme.TEXT_INPUT_BG_COLOR)
        self.user_entry.grid(row=0, column=0, sticky="ew")
        self.user_entry.bind("<Return>", self.send_message)
        send_button = ctk.CTkButton(entry_frame, text="➤", width=40, height=40, corner_radius=15, font=(Theme.INPUT_FONT[0], 18, "bold"), command=self.send_message, fg_color=Theme.BUTTON_COLOR)
        send_button.grid(row=0, column=1, padx=(10, 0))
        self.after(500, lambda: self.create_message_bubble(self.logic_handler.initial_message, "bot"))
    def load_image(self, path, size=None):
        try:
            image = Image.open(path)
            return ctk.CTkImage(image, size=size) if size else ctk.CTkImage(image, size=(image.width, image.height))
        except Exception as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return None
    def on_closing(self):
        if messagebox.askyesno("Sair", "Você tem certeza que quer fechar o assistente?"): self.destroy()
    def send_message(self, event=None):
        user_text = self.user_entry.get().strip()
        if not user_text: return
        self.create_message_bubble(user_text, "user")
        self.user_entry.delete(0, "end")
        typing_bubble = self.create_message_bubble("SouzaLink está digitando...", "bot", is_typing=True)
        def get_and_display_response():
            bot_responses = self.logic_handler.get_response(user_text)
            typing_bubble.destroy()
            for i, response in enumerate(bot_responses):
                self.after(i * 300, lambda r=response: self.create_message_bubble(r, "bot"))
        self.after(700, get_and_display_response)
    def create_message_bubble(self, text, sender, is_typing=False):
        line_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        line_frame.pack(fill="x", padx=5, pady=(5, 0), anchor="e" if sender == "user" else "w")
        bubble_and_ts_frame = ctk.CTkFrame(line_frame, fg_color="transparent")
        if sender == "user":
            if self.user_avatar: ctk.CTkLabel(line_frame, image=self.user_avatar, text="").pack(side="right", padx=(5, 0), anchor="s")
            bubble_and_ts_frame.pack(side="right")
        else:
            if self.bot_avatar: ctk.CTkLabel(line_frame, image=self.bot_avatar, text="").pack(side="left", padx=(0, 5), anchor="s")
            bubble_and_ts_frame.pack(side="left")
        if is_typing:
            bubble = ctk.CTkLabel(bubble_and_ts_frame, text=text, font=(Theme.MAIN_FONT[0], Theme.MAIN_FONT[1], "italic"), fg_color=Theme.BOT_BUBBLE_COLOR, corner_radius=15, padx=12, pady=8)
            bubble.pack()
        else: self._create_formatted_text_bubble(bubble_and_ts_frame, text, sender)
        if not is_typing:
            timestamp = datetime.now().strftime("%H:%M")
            ts_label = ctk.CTkLabel(bubble_and_ts_frame, text=timestamp, font=Theme.TIMESTAMP_FONT, text_color="gray50")
            ts_label.pack(anchor="e" if sender == "user" else "w", padx=5, pady=(0, 2))
        self.messages_frame._parent_canvas.yview_moveto(1.0)
        return line_frame
    def _create_formatted_text_bubble(self, container, text, sender):
        bubble_color = Theme.USER_BUBBLE_COLOR if sender == "user" else Theme.BOT_BUBBLE_COLOR
        bubble_frame = ctk.CTkFrame(container, fg_color=bubble_color, corner_radius=15)
        bubble_frame.pack(anchor="w")
        is_link = re.fullmatch(r'https?://[^\s]+', text.strip())
        if is_link:
            link_font = ctk.CTkFont(family=Theme.MAIN_FONT[0], size=Theme.MAIN_FONT[1], underline=True)
            link_label = ctk.CTkLabel(bubble_frame, text=text, font=link_font, text_color="#1E88E5", cursor="hand2")
            link_label.pack(padx=12, pady=8)
            link_label.bind("<Button-1>", lambda e, link=text: self.open_link(link))
            return
        lines = text.split('\n')
        for i, line in enumerate(lines):
            pady = (8 if i == 0 else 0, 8 if i == len(lines) - 1 else 2)
            if "[NEGRITO]" in line:
                line_subframe = ctk.CTkFrame(bubble_frame, fg_color="transparent")
                line_subframe.pack(fill="x", padx=12, pady=pady, anchor="w")
                parts = line.split("[NEGRITO]")
                texto_normal, resto = parts[0], parts[1]
                partes_negrito = resto.split("[/NEGRITO]")
                texto_negrito, texto_resto = partes_negrito[0], partes_negrito[1]
                if texto_normal: ctk.CTkLabel(line_subframe, text=texto_normal, font=Theme.MAIN_FONT).pack(side="left")
                fonte_negrito = (Theme.MAIN_FONT[0], Theme.MAIN_FONT[1], "bold")
                ctk.CTkLabel(line_subframe, text=texto_negrito, font=fonte_negrito).pack(side="left")
                if texto_resto: ctk.CTkLabel(line_subframe, text=texto_resto, font=Theme.MAIN_FONT).pack(side="left")
            else: ctk.CTkLabel(bubble_frame, text=line, wraplength=350, justify="left", font=Theme.MAIN_FONT).pack(anchor="w", padx=12, pady=pady)
    def open_link(self, url): webbrowser.open_new_tab(url)

if __name__ == "__main__":
    try:
        chatbot_brain = ChatbotLogic()
        app = ChatApplication(logic_handler=chatbot_brain)
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao iniciar o chatbot:\n\n{e}")