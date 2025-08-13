# logic.py

from actions import *
from keywords import KeywordResponder

class ChatbotLogic:
    def __init__(self):
        self.keyword_handler = KeywordResponder()
        self.menu_options = {
            '1': ListarRamalAction(), '2': AbrirChamadoTIAction(),
            '3': AbrirChamadoManutencaoAction(), '4': NotificarLDSistemasAction(),
            '5': EsqueciSenhaAction(), '6': AcessarEmailAction(), '7': FalarWhatsAppAction()
        }
        # --- MENU ATUALIZADO COM TEXTO GENÉRICO ---
        self.initial_message = """Olá, Sou SouzaLink, seu assistente virtual! 🤖
Em que posso te ajudar hoje?

1 - Listar Ramal
2 - Abrir chamado para TI
3 - Abrir chamado para Manutenção
4 - Acessar Sistema Interno
5 - Esqueci minha Senha
6 - Acessar E-mail
7 - Falar com Suporte pelo WhatsApp"""
        self.conversation_state = None
        self.current_action_object = None

    # O resto do arquivo logic.py continua exatamente o mesmo...
    def get_response(self, user_input):
        text = user_input.strip()
        if text.lower() in ["menu", "cancelar", "voltar", "oi", "olá"]:
            self.conversation_state = None
            self.current_action_object = None
            return [self.initial_message]
        if self.conversation_state is not None:
            if self.conversation_state == 'aguardando_setor_ramal':
                responses, should_end = self.current_action_object.processar_resposta(text)
                if should_end:
                    self.conversation_state = None
                    self.current_action_object = None
                return responses
        keyword_response = self.keyword_handler.get_response(text)
        if keyword_response:
            return [keyword_response]
        if text in self.menu_options:
            action_object = self.menu_options[text]
            if isinstance(action_object, ListarRamalAction):
                self.conversation_state = 'aguardando_setor_ramal'
                self.current_action_object = action_object
            return action_object.execute()
        return [f"Desculpe, não entendi '{text}'. Por favor, escolha um número de 1 a 7, ou digite 'menu' para voltar ao início."]