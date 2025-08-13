# logic.py

from actions import *
from keywords import KeywordResponder

class ChatbotLogic:
    def __init__(self):
        self.keyword_handler = KeywordResponder()
        self.menu_options = {
            '1': ListarRamalAction(),
            '2': AbrirChamadoTIAction(),
            '3': AbrirChamadoManutencaoAction(),
            '4': NotificarLDSistemasAction(),
            '5': EsqueciSenhaAction()
        }
        self.initial_message = """Olá, Sou SouzaLink, seu assistente desenvolvido por Leomario! 🤖
Em que posso te ajudar hoje?

1 - Listar Ramal
2 - Abrir chamado para TI
3 - Abrir chamado para Manutenção
4 - Notificar no LD Sistemas
5 - Esqueci minha Senha"""
        
        self.conversation_state = None
        self.current_action_object = None

    def get_response(self, user_input):
        text = user_input.strip()

        # 1. Checa se há uma resposta rápida para uma palavra-chave
        keyword_response = self.keyword_handler.get_response(text)
        if keyword_response and self.conversation_state is None:
            return [keyword_response]

        # --- CORREÇÃO APLICADA AQUI ---
        # Comandos de alta prioridade para resetar a conversa e voltar ao menu
        if text.lower() in ["olá", "ola", "oi", "menu", "cancelar", "voltar"]:
             self.conversation_state = None
             self.current_action_object = None # Garante limpeza total da memória
             print("Estado da conversa resetado pelo usuário.")
             return [self.initial_message]

        # 2. Checa se está no meio de uma conversa
        if self.conversation_state is not None:
            if self.conversation_state == 'aguardando_setor_ramal':
                responses, should_end = self.current_action_object.processar_resposta(text)
                if should_end:
                    self.conversation_state = None
                    self.current_action_object = None
                return responses

        # 3. Checa se é uma opção do menu principal
        if text in self.menu_options:
            action_object = self.menu_options[text]
            if isinstance(action_object, ListarRamalAction):
                self.conversation_state = 'aguardando_setor_ramal'
                self.current_action_object = action_object
            return action_object.execute()

        # 4. Se não for nada disso, retorna a mensagem padrão.
        return [f"Opção '{text}' não reconhecida. Por favor, escolha um número de 1 a 5, ou digite 'menu' para voltar ao início."]