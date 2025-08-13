# actions.py

import pandas as pd
from thefuzz import process

class MenuAction:
    """Classe base para todas as ações do menu."""
    def execute(self):
        raise NotImplementedError("Cada ação precisa implementar o método execute()!")

class ListarRamalAction(MenuAction):
    def __init__(self):
        self.ramais_db = {}
        try:
            df = pd.read_excel("RAMAL.xlsx")
            print("Planilha de ramais carregada com sucesso!")
            for index, row in df.iterrows():
                setor_limpo = str(row['SETOR']).lower().strip()
                self.ramais_db[setor_limpo] = { "setor": str(row['SETOR']).strip(), "ramal": str(row['RAMAL']) }
        except Exception as e:
            print(f"AVISO: Erro ao ler 'RAMAL.xlsx': {e}.")
            self.ramais_db = { "ti": {"setor": "TI", "ramal": "1234"}, "rh": {"setor": "RH", "ramal": "5678"} }

    def execute(self):
        return ["Você quer listar todos os ramais ou apenas de um setor específico? Por favor, digite 'todos' ou o nome do setor."]

    # --- MÉTODO ATUALIZADO PARA MANTER A CONVERSA ATIVA ---
    def processar_resposta(self, resposta_do_usuario):
        busca = resposta_do_usuario.lower().strip()
        
        # Frase para continuar a conversa após uma busca bem-sucedida
        follow_up_prompt = "\n\nQual outro setor deseja pesquisar? (Digite 'menu' para voltar)"

        if not self.ramais_db:
             return ["Desculpe, não consegui carregar os dados dos ramais."], True

        # --- LÓGICA DE BUSCA INTELIGENTE ATUALIZADA ---

        # 1. Busca Exata
        if busca == 'todos':
            todos_os_ramais = "Aqui está a lista de todos os ramais: 📝\n\n"
            for info in self.ramais_db.values():
                todos_os_ramais += f"- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]\n"
            # Adiciona a pergunta de continuação e mantém a conversa ativa (False)
            return [todos_os_ramais + follow_up_prompt], False
        
        elif busca in self.ramais_db:
            info = self.ramais_db[busca]
            response = f"Aqui está o ramal do setor '{busca.upper()}':\n- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]"
            # Adiciona a pergunta de continuação e mantém a conversa ativa (False)
            return [response + follow_up_prompt], False
        
        # 2. Busca Parcial
        matches_parciais = [info for setor_key, info in self.ramais_db.items() if busca in setor_key]
        
        if matches_parciais:
            response = ""
            if len(matches_parciais) == 1:
                info = matches_parciais[0]
                response = f"Encontrado: {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]"
            else:
                response = f"Encontrei múltiplos setores com '{resposta_do_usuario}':\n\n"
                for info in matches_parciais:
                    response += f"- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]\n"
            # Adiciona a pergunta de continuação e mantém a conversa ativa (False)
            return [response + follow_up_prompt], False

        # 3. Correção de Erros de Digitação
        melhor_match, score = process.extractOne(busca, self.ramais_db.keys())
        
        if score >= 80:
            info = self.ramais_db[melhor_match]
            response = f"Você quis dizer '{info['setor']}'?\n- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]"
            # Adiciona a pergunta de continuação e mantém a conversa ativa (False)
            return [response + follow_up_prompt], False

        # 4. Se nada der certo, permite que o usuário tente de novo.
        response = f"Desculpe, não encontrei o setor '{resposta_do_usuario}'. Tente novamente."
        return [response], False


# --- OUTRAS CLASSES (CONTINUAM IGUAIS) ---

class AbrirChamadoTIAction(MenuAction):
    def execute(self):
        return [ "Ok, para abrir um chamado para a TI, você precisa acessar o seguinte link:", "http://192.168.10.5/glpi/front/logout.php" ]

class AbrirChamadoManutencaoAction(MenuAction):
    def execute(self):
        return [ "Entendido, para abrir um chamado para a manutenção, acesse o link abaixo:", "https://scrb.neovero.com" ]

class NotificarLDSistemasAction(MenuAction):
    def execute(self):
        return [ "Para notificar no LD Sistemas, acesse o link:", "https://sistemas.ldsistemas.com/public/" ]

class EsqueciSenhaAction(MenuAction):
    def execute(self):
        return [ "Para alterar sua senha em qualquer sistema, você precisa abrir um chamado no GLPI:", "http://192.168.10.5/glpi/front/logout.php", "No formulário você terá as opções. Qualquer dúvida entre em contato com a TI no Ramal 225." ]