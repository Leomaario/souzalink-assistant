import os
import customtkinter as ctk
from PIL import Image # Importa a biblioteca de imagens

# --- CLASSE DE ESTILO (PAINEL DE CONTROLE VISUAL) ---
class Theme:
    """
    Centraliza todas as configurações de aparência do aplicativo.
    Mude os valores aqui para alterar o visual do chatbot inteiro.
    """
    # GERAL
    WINDOW_SIZE = "550x650"  # Tamanho da janela
    APPEARANCE_MODE = "light"  # "light", "dark" ou "system"
    COLOR_THEME = "green"  # Tema de cor padrão do CustomTkinter

    # CORES (Formato: (modo claro, modo escuro))
    MAIN_BG_COLOR = ("#F2F2F2", "#1C1C1C") # Cor de fundo da janela e do chat
    BOT_BUBBLE_COLOR = ("#E8F5E9", "#2E4B33") # Balão de mensagem do Bot (Verde claro)
    USER_BUBBLE_COLOR = ("#FFFFFF", "#3C3C3C") # Balão de mensagem do Usuário (Branco/Cinza)
    TEXT_INPUT_BG_COLOR = ("#FFFFFF", "#2B2B2B") # Fundo da caixa de texto
    BUTTON_COLOR = "#2E7D32"  # Cor principal do botão Enviar

    # FONTES
    MAIN_FONT = ("Segoe UI", 14) # Fonte principal para os balões
    INPUT_FONT = ("Segoe UI", 12) # Fonte da caixa de texto

    # IMAGENS (Certifique-se que esses arquivos existem na pasta do projeto)
    BOT_AVATAR_PATH = "bot_avatar.png"
    USER_AVATAR_PATH = "user_avatar.png"
    AVATAR_SIZE = (40, 40) # Tamanho dos avatares em pixels

# --- CLASSE DE LÓGICA DO CHATBOT (O "CÉREBRO" - AGORA BASEADO EM MENU) ---
class ChatbotLogic:
    def __init__(self):
        """Inicializa o cérebro do chatbot."""
        self.menu_options = {
            '1': "Para listar um ramal, por favor, me informe o nome do setor ou da pessoa.",
            '2': "Ok, abrindo um chamado para a equipe de TI. Por favor, descreva seu problema em uma única mensagem.",
            '3': "Entendido, chamado para a Manutenção. Qual o local e o problema a ser reportado?",
            '4': "Para notificar no LD Sistemas, preciso do número da nota e do motivo. Por favor, informe.",
            '5': "Para resetar sua senha, por favor, acesse o portal de autoatendimento da TI ou procure um analista. 🔑"
        }
        self.initial_message = """Olá, Sou SouzaLink, seu assistente desenvolvido por Leomario! 🤖
Em que posso te ajudar hoje?

1 - Listar Ramal
2 - Abrir chamado para TI
3 - Abrir chamado para Manutenção
4 - Notificar no LD Sistemas
5 - Esqueci minha Senha"""

    def get_response(self, user_input):
        """Processa a entrada do usuário e retorna a resposta com base no menu."""
        text = user_input.strip()

        # Se o usuário digitou um número válido do menu
        if text in self.menu_options:
            return self.menu_options[text]
        
        # Se for a primeira mensagem
        if text.lower() == "olá":
             return self.initial_message

        # Resposta padrão se a opção não for válida
        return f"Opção '{text}' não reconhecida. Por favor, escolha um número de 1 a 5."


# --- CLASSE DA APLICAÇÃO (A "INTERFACE GRÁFICA") ---
class ChatApplication(ctk.CTk):
    def __init__(self, logic_handler):
        super().__init__()
        
        self.logic_handler = logic_handler

        # --- ESTILIZAÇÃO DA JANELA USANDO A CLASSE THEME ---
        self.title("SouzaLink - Assistente de TI")
        self.geometry(Theme.WINDOW_SIZE)
        self.resizable(False, False) # Impede de redimensionar a janela
        
        ctk.set_appearance_mode(Theme.APPEARANCE_MODE)
        ctk.set_default_color_theme(Theme.COLOR_THEME)

        # Carregar imagens dos avatares uma vez
        try:
            bot_image = Image.open(Theme.BOT_AVATAR_PATH)
            self.bot_avatar = ctk.CTkImage(bot_image, size=Theme.AVATAR_SIZE)
            
            user_image = Image.open(Theme.USER_AVATAR_PATH)
            self.user_avatar = ctk.CTkImage(user_image, size=Theme.AVATAR_SIZE)
        except FileNotFoundError as e:
            print(f"Erro: Imagem de avatar não encontrada! Verifique o caminho em Theme: {e}")
            self.bot_avatar = None
            self.user_avatar = None

        # --- LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.messages_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.MAIN_BG_COLOR)
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.messages_frame.columnconfigure(0, weight=1)

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

        # Exibe a mensagem inicial com o menu
        self.after(500, lambda: self.create_message_bubble(self.logic_handler.initial_message, "bot"))

    def send_message(self, event=None):
        user_text = self.user_entry.get().strip()
        if not user_text:
            return
        
        self.create_message_bubble(user_text, "user")
        
        bot_response = self.logic_handler.get_response(user_text)
        self.after(300, lambda: self.create_message_bubble(bot_response, "bot"))
        
        self.user_entry.delete(0, "end")

    def create_message_bubble(self, text, sender):
        """Cria e posiciona um balão de mensagem com um avatar."""
        # Frame para a linha inteira (avatar + balão)
        line_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        
        if sender == "user":
            # Alinha a linha à direita
            line_frame.pack(fill="x", padx=(60, 5), pady=5)
            line_frame.grid_columnconfigure(0, weight=1) # Coluna vazia para empurrar
            
            # Coloca o balão na coluna 1
            bubble = ctk.CTkLabel(line_frame, text=text, wraplength=350, justify="left",
                                  fg_color=Theme.USER_BUBBLE_COLOR, corner_radius=15,
                                  font=Theme.MAIN_FONT, padx=12, pady=8)
            bubble.grid(row=0, column=1, sticky="e")
            
            # Coloca o avatar na coluna 2
            if self.user_avatar:
                avatar = ctk.CTkLabel(line_frame, image=self.user_avatar, text="")
                avatar.grid(row=0, column=2, padx=(5,0), sticky="s")

        else: # sender == "bot"
            # Alinha a linha à esquerda
            line_frame.pack(fill="x", padx=(5, 60), pady=5)
            
            # Coloca o avatar na coluna 0
            if self.bot_avatar:
                avatar = ctk.CTkLabel(line_frame, image=self.bot_avatar, text="")
                avatar.grid(row=0, column=0, padx=(0,5), sticky="s")

            # Coloca o balão na coluna 1
            bubble = ctk.CTkLabel(line_frame, text=text, wraplength=350, justify="left",
                                  fg_color=Theme.BOT_BUBBLE_COLOR, corner_radius=15,
                                  font=Theme.MAIN_FONT, padx=12, pady=8)
            bubble.grid(row=0, column=1, sticky="w")

        self.messages_frame._parent_canvas.yview_moveto(1.0)

# --- PONTO DE ENTRADA DA APLICAÇÃO ---
if __name__ == "__main__":
    try:
        chatbot_brain = ChatbotLogic()
        app = ChatApplication(logic_handler=chatbot_brain)
        app.mainloop()
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao iniciar o chatbot:\n\n{e}")