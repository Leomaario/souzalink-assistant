# main.py

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import webbrowser
import re
from datetime import datetime

from theme import Theme
from logic import ChatbotLogic

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
            self.iconbitmap("souzalink_.ico")
        except Exception as e:
            print(f"AVISO: Ícone 'souzalink_.ico' não encontrado. {e}")

        try:
            bot_image = Image.open(Theme.BOT_AVATAR_PATH)
            self.bot_avatar = ctk.CTkImage(bot_image, size=Theme.AVATAR_SIZE)
            user_image = Image.open(Theme.USER_AVATAR_PATH)
            self.user_avatar = ctk.CTkImage(user_image, size=Theme.AVATAR_SIZE)
        except FileNotFoundError:
            self.bot_avatar = None
            self.user_avatar = None
            messagebox.showwarning("Aviso de Avatares", "Não foi possível encontrar uma ou mais imagens de avatares.")

        ctk.set_appearance_mode(Theme.APPEARANCE_MODE)
        ctk.set_default_color_theme(Theme.COLOR_THEME)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.messages_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.MAIN_BG_COLOR)
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        entry_frame.columnconfigure(0, weight=1)

        self.user_entry = ctk.CTkEntry(entry_frame, placeholder_text="Digite uma opção...", 
                                       font=Theme.INPUT_FONT, height=40, corner_radius=15, 
                                       fg_color=Theme.TEXT_INPUT_BG_COLOR)
        self.user_entry.grid(row=0, column=0, sticky="ew")
        self.user_entry.bind("<Return>", self.send_message)

        send_button = ctk.CTkButton(entry_frame, text="➤", width=40, height=40, corner_radius=15,
                                    font=(Theme.INPUT_FONT[0], 18, "bold"), command=self.send_message,
                                    fg_color=Theme.BUTTON_COLOR)
        send_button.grid(row=0, column=1, padx=(10, 0))

        self.after(500, lambda: self.create_message_bubble(self.logic_handler.initial_message, "bot"))

    def on_closing(self):
        if messagebox.askyesno("Sair", "Você tem certeza que quer fechar o assistente?"):
            self.destroy()

    def send_message(self, event=None):
        user_text = self.user_entry.get().strip()
        if not user_text: return
        
        self.create_message_bubble(user_text, "user")
        self.user_entry.delete(0, "end")
        
        typing_bubble = self.create_message_bubble("SouzaLink está digitando...", "bot", is_typing=True)
        
        def get_and_replace():
            bot_responses = self.logic_handler.get_response(user_text)
            if not isinstance(bot_responses, list):
                bot_responses = [bot_responses]
            typing_bubble.destroy()
            for i, response in enumerate(bot_responses):
                self.after(i * 300, lambda r=response: self.create_message_bubble(r, "bot"))
        self.after(500, get_and_replace)

    def create_message_bubble(self, text, sender, is_typing=False):
        timestamp = datetime.now().strftime("%H:%M")
        
        line_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        line_frame.pack(fill="x", padx=5, pady=(5, 0), anchor="e" if sender == "user" else "w")
        
        is_link = re.fullmatch(r'https?://[^\s]+', text.strip())
        
        bubble_and_ts_frame = ctk.CTkFrame(line_frame, fg_color="transparent")

        if sender == "user":
            if self.user_avatar:
                avatar = ctk.CTkLabel(line_frame, image=self.user_avatar, text="")
                avatar.pack(side="right", padx=(5, 0), anchor="s")
            bubble_and_ts_frame.pack(side="right")
        else: # sender == "bot"
            if self.bot_avatar:
                avatar = ctk.CTkLabel(line_frame, image=self.bot_avatar, text="")
                avatar.pack(side="left", padx=(0, 5), anchor="s")
            bubble_and_ts_frame.pack(side="left")

        if is_typing:
            bubble = ctk.CTkLabel(bubble_and_ts_frame, text=text, font=(Theme.MAIN_FONT[0], Theme.MAIN_FONT[1] - 1, "italic"),
                                 fg_color=Theme.BOT_BUBBLE_COLOR, corner_radius=15, padx=12, pady=8)
            bubble.pack()
        elif is_link:
            link_font = ctk.CTkFont(family=Theme.MAIN_FONT[0], size=Theme.MAIN_FONT[1], underline=True)
            bubble = ctk.CTkLabel(bubble_and_ts_frame, text=text, font=link_font, text_color="#1E88E5",
                                      cursor="hand2", fg_color=Theme.BOT_BUBBLE_COLOR, corner_radius=15, padx=12, pady=8)
            bubble.pack()
            bubble.bind("<Button-1>", lambda e, link=text: self.open_link(link))
        else:
            self._create_formatted_text_bubble(bubble_and_ts_frame, text, sender)
        
        if not is_typing:
            ts_anchor = "e" if sender == "user" else "w"
            timestamp_label = ctk.CTkLabel(bubble_and_ts_frame, text=timestamp,
                                           font=Theme.TIMESTAMP_FONT, text_color="gray50")
            timestamp_label.pack(anchor=ts_anchor, padx=5, pady=(0, 2))
        
        self.messages_frame._parent_canvas.yview_moveto(1.0)
        return line_frame
    
    # --- CORREÇÃO APLICADA AQUI ---
    # A função agora aceita o argumento 'sender'
    def _create_formatted_text_bubble(self, container, text, sender):
        # E usa o 'sender' para definir a cor, em vez de adivinhar
        bubble_color = Theme.USER_BUBBLE_COLOR if sender == "user" else Theme.BOT_BUBBLE_COLOR
        
        bubble_frame = ctk.CTkFrame(container, fg_color=bubble_color, corner_radius=15)
        bubble_frame.pack()
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            pady = (8, 2) if i == 0 and len(lines) > 1 else (0, 2)
            if i == len(lines) - 1: pady = (pady[0], 8)
            if len(lines) == 1: pady = 8
            if "[NEGRITO]" in line:
                line_subframe = ctk.CTkFrame(bubble_frame, fg_color="transparent")
                line_subframe.pack(fill="x", padx=12, pady=pady, anchor="w")
                parts = line.split("[NEGRITO]")
                texto_normal, resto = parts[0], parts[1]
                partes_negrito = resto.split("[/NEGRITO]")
                texto_negrito, texto_resto = partes_negrito[0], partes_negrito[1]
                ctk.CTkLabel(line_subframe, text=texto_normal, font=Theme.MAIN_FONT).pack(side="left")
                fonte_negrito = (Theme.MAIN_FONT[0], Theme.MAIN_FONT[1], "bold")
                ctk.CTkLabel(line_subframe, text=texto_negrito, font=fonte_negrito).pack(side="left")
                if texto_resto: ctk.CTkLabel(line_subframe, text=texto_resto, font=Theme.MAIN_FONT).pack(side="left")
            else:
                ctk.CTkLabel(bubble_frame, text=line, wraplength=350, justify="left",
                             font=Theme.MAIN_FONT, padx=12).pack(anchor="w", pady=pady)
        return bubble_frame

    def open_link(self, url):
        webbrowser.open_new_tab(url)

if __name__ == "__main__":
    try:
        chatbot_brain = ChatbotLogic()
        app = ChatApplication(logic_handler=chatbot_brain)
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao iniciar o chatbot:\n\n{e}")