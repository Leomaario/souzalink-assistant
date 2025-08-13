# actions.py
import pandas as pd
from thefuzz import process
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MenuAction:
    def execute(self):
        raise NotImplementedError("Cada ação precisa implementar o método execute()!")

class ListarRamalAction(MenuAction):
    def __init__(self):
        self.ramais_db = {}
        try:
            caminho_planilha = resource_path("RAMAL.xlsx")
            df = pd.read_excel(caminho_planilha)
            print("Planilha de ramais carregada com sucesso!")
            for _, row in df.iterrows():
                setor_limpo = str(row['SETOR']).lower().strip()
                self.ramais_db[setor_limpo] = {"setor": str(row['SETOR']).strip(), "ramal": str(row['RAMAL'])}
        except Exception as e:
            print(f"AVISO: Erro ao ler 'RAMAL.xlsx': {e}. Usando dados de exemplo.")
            self.ramais_db = {"ti": {"setor": "TI", "ramal": "1234"}}

    def execute(self):
        return ["Você quer listar todos os ramais ou de um setor específico? Digite 'todos' ou o nome do setor."]

    def processar_resposta(self, user_input):
        busca = user_input.lower().strip()
        follow_up = "\n\nQual outro setor deseja pesquisar? (Digite 'menu' para voltar)"
        if not self.ramais_db: return ["Desculpe, não consegui carregar os dados dos ramais."], True
        if busca == 'todos':
            response = "Aqui está a lista de todos os ramais: 📝\n\n"
            for info in self.ramais_db.values():
                response += f"- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]\n"
            return [response + follow_up], False
        if busca in self.ramais_db:
            info = self.ramais_db[busca]
            response = f"Aqui está o ramal de '{info['setor']}':\n- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]"
            return [response + follow_up], False
        matches = [info for setor, info in self.ramais_db.items() if busca in setor]
        if matches:
            response = f"Encontrei estes setores com '{user_input}':\n\n"
            for info in matches:
                response += f"- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]\n"
            return [response + follow_up], False
        best_match, score = process.extractOne(busca, self.ramais_db.keys())
        if score >= 80:
            info = self.ramais_db[best_match]
            response = f"Você quis dizer '{info['setor']}'?\n- {info['setor']}: [NEGRITO]{info['ramal']}[/NEGRITO]"
            return [response + follow_up], False
        return [f"Desculpe, não encontrei o setor '{user_input}'. Tente novamente."], False

class AbrirChamadoTIAction(MenuAction):
    def execute(self):
        # Exemplo genérico de link para sistema de chamados
        return ["Ok, para abrir um chamado para a TI, acesse o seguinte link:", "http://seu-servidor.com/glpi/chamados"]

class AbrirChamadoManutencaoAction(MenuAction):
    def execute(self):
        # Exemplo genérico
        return ["Para abrir um chamado para a manutenção, acesse o link:", "http://seu-servidor.com/manutencao/chamados"]

class NotificarLDSistemasAction(MenuAction):
    def execute(self):
        # Exemplo genérico
        return ["Para acessar o Sistema Interno, use o link:", "https://seu-sistema-interno.com/login"]

class EsqueciSenhaAction(MenuAction):
    def execute(self):
        return ["Para resetar sua senha, por favor, use o portal de autoatendimento:", "http://seu-servidor.com/glpi/reset-senha", "Se o problema persistir, contate o Ramal [NEGRITO]1234[/NEGRITO]."]
    
class AcessarEmailAction(MenuAction):
    def execute(self):
        return ["Para acessar seu e-mail, por favor, clique no seguinte link:", "https://outlook.office.com/mail/"]

class FalarWhatsAppAction(MenuAction):
    def execute(self):
        # Placeholder para o número de WhatsApp
        return ["Para falar com o suporte via WhatsApp, clique no link:", "https://wa.me/5511999999999?text=Olá,%20preciso%20de%20suporte!"]