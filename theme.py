
class Theme:
    """
    Centraliza todas as configurações de aparência do aplicativo.
    Mude os valores aqui para alterar o visual do chatbot inteiro.
    """
    # GERAL
    WINDOW_SIZE = "550x650"
    APPEARANCE_MODE = "light"
    COLOR_THEME = "green"

    # CORES (Formato: (modo claro, modo escuro))
    MAIN_BG_COLOR = ("#F2F2F2", "#1C1C1C")
    BOT_BUBBLE_COLOR = ("#E8F5E9", "#2E4B33")
    USER_BUBBLE_COLOR = ("#FFFFFF", "#3C3C3C")
    TEXT_INPUT_BG_COLOR = ("#FFFFFF", "#2B2B2B")
    BUTTON_COLOR = "#2E7D32"

    # FONTES
    MAIN_FONT = ("Arial", 16)
    INPUT_FONT = ("Arial", 18)
    TIMESTAMP_FONT = ("Segoe UI", 10)


    # IMAGENS (Certifique-se que esses arquivos existem na pasta do projeto)
    BOT_AVATAR_PATH = "avatar_souzalink.png"
    USER_AVATAR_PATH = "avatar_user.png"
    CHAT_BG_PATH = "chat_background.png"
    AVATAR_SIZE = (40, 40)