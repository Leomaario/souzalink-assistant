# keywords.py

class KeywordResponder:
    def __init__(self):
        """
        Esta classe armazena um dicionário de palavras-chave e suas respostas diretas.
        É o nosso "banco de dados" de perguntas e respostas rápidas (FAQ).
        """
        self.keyword_map = {
            # --- Small Talk (o que tínhamos antes) ---
            "tudo bem?": "Como um modelo de linguagem, estou sempre funcionando perfeitamente! E você, como está? 😊",
            "tudo bem": "Tudo ótimo! Pronto para ajudar. 👍",
            "quem é você?": "Sou o SouzaLink: Assistente desenvolvido por Leomario, estou sempre pronto para ajudar! 🤖",
            "obrigado": "De nada! Se precisar de mais alguma coisa, é só chamar. 😉",
            "tchau": "Até mais! Tenha um ótimo dia. 👋",

            # --- Respostas Rápidas de TI (Novos Exemplos) ---
            "glpi": "O GLPI é nosso sistema de chamados. Você pode acessá-lo pelo menu principal na opção 2.",
            "ramal": "Você pode listar os ramais disponíveis digitando '1' no menu principal.",
            "ti": "A equipe de TI está aqui para ajudar com problemas técnicos. Você pode abrir um chamado na opção 2 do menu.",
            "manutenção": "Para abrir um chamado de manutenção, use a opção 3 do menu principal.",
            "ld sistemas": "Para notificar no LD Sistemas, use a opção 4 do menu principal.",
            "senha": "Para resetar sua senha, use a opção 5 do menu principal.",
            "wifi": "A rede Wi-Fi para colaboradores é a 'WIFI-FREE', e não tem senha.",
            "email": "Você pode acessar seus e-mails pelo portal: https://outlook.office.com/mail/",
            "tudo bem?": "Como um assistente virtual, estou sempre pronto para ajudar! E você, como está? 😊",
            "como você está?": "Estou sempre pronto para ajudar! E você, como está? 😊",
            "bem": "Fico feliz em saber que você está bem! como posso ajudar?😊",
            "mal": "Sinto muito em saber que você não está bem. Como posso ajudar a melhorar seu dia? 😊",
            "problema": "Se você está enfrentando um problema, por favor, descreva-o para que eu possa ajudar. Você pode abrir um chamado na opção 2 do menu.",
            "erro": "Se você encontrou um erro, por favor, descreva-o para que eu possa ajudar. Você pode abrir um chamado na opção 2 do menu.",
            "ajuda": "Claro! Estou aqui para ajudar. Por favor, descreva seu problema ou dúvida.",
            "suporte": "Você pode obter suporte técnico abrindo um chamado na opção 2 do menu principal.",
            "contato ti": "Para entrar em contato com a equipe de TI, você pode abrir um chamado na opção 2 do menu principal.",
            "contato manutenção": "Para entrar em contato com a equipe de Manutenção, você pode abrir um chamado na opção 3 do menu principal.",
            "contato ld sistemas": "Para entrar em contato com o LD Sistemas, você pode abrir um chamado na opção 4 do menu principal.",
            "leomario" : "Leomario é o desenvolvedor deste assistente. Ele está sempre trabalhando para melhorar a experiência do usuário.",
        }

    def get_response(self, user_input):
        """
        Verifica se a entrada do usuário corresponde a uma palavra-chave.
        Retorna a resposta se encontrar, ou None se não encontrar.
        """
        # Converte para minúsculas para a busca ser case-insensitive
        text = user_input.lower().strip()
        
        # Retorna a resposta se a chave exata for encontrada
        return self.keyword_map.get(text)