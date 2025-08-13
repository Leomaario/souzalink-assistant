# SouzaLink - Assistente de TI Desktop 🤖

Um assistente virtual de desktop desenvolvido em Python para automatizar e centralizar as solicitações de suporte técnico mais comuns em um ambiente corporativo.

## 🎯 Finalidade

O objetivo principal deste projeto é criar um ponto central de atendimento que funciona 24/7, liberando a equipe de TI para focar em problemas mais complexos. O bot é capaz de:

-   Apresentar um menu de opções claro e direto.
-   Consultar uma base de dados externa (planilha Excel) para fornecer informações como ramais.
-   Oferecer links clicáveis para sistemas de abertura de chamados.
-   Conduzir conversas guiadas de múltiplos passos para diagnósticos simples.

## ✨ Features

-   **Interface Gráfica Moderna:** Construído com CustomTkinter para uma aparência limpa e amigável.
-   **Menu Interativo:** Navegação simples e direta baseada em opções numéricas.
-   **Integração com Excel:** Lê dados de uma planilha `.xlsx` em tempo real, facilitando a atualização de informações sem alterar o código.
-   **Busca Inteligente:** Utiliza `thefuzz` para encontrar resultados mesmo com erros de digitação ou buscas parciais.
-   **Avatares e Timestamps:** Interface de chat com avatares customizáveis e carimbo de data/hora para cada mensagem.
-   **Links Clicáveis:** As respostas podem conter links que abrem diretamente no navegador padrão.
-   **Empacotamento Profissional:** Scripts para gerar um executável (`.exe`) e um instalador completo.

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **CustomTkinter:** Para a Interface Gráfica (GUI).
-   **Pandas:** Para a leitura da planilha Excel.
-   **Pillow:** Para manipulação de imagens (avatares).
-   **TheFuzz:** Para a lógica de busca inteligente.
-   **PyInstaller:** Para gerar o executável `.exe`.
-   **Inno Setup:** Para criar o instalador final para Windows.

## 🚀 Como Começar

Siga os passos abaixo para rodar o projeto na sua máquina.

### Pré-requisitos

-   Python 3.8 ou superior.
-   Git (para clonar o repositório).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Leomaario/souzalink-assistant.git](https://github.com/Leomaario/souzalink-assistant.git)
    cd souzalink-assistant
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    # No Windows (CMD)
    .venv\Scripts\activate.bat
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuração

Para que o bot funcione na sua realidade, você **precisa** configurar os seguintes arquivos:

1.  **Planilha de Ramais (`RAMAL.xlsx`):**
    -   Este arquivo deve estar na pasta raiz do projeto.
    -   Ele **precisa** ter duas colunas com os cabeçalhos exatamente assim: `SETOR` e `RAMAL`.
    -   Preencha com os dados da sua empresa.

2.  **Imagens (`theme.py`):**
    -   Substitua os arquivos `bot_avatar.png` e `user_avatar.png` pelas suas imagens.
    -   Se os nomes dos seus arquivos forem diferentes, atualize os caminhos no arquivo `theme.py`.
    -   O mesmo vale para o ícone `souzalink_icon.ico`.

3.  **Opções do Menu (`actions.py`):**
    -   Abra o arquivo `actions.py`.
    -   Dentro de cada classe de ação (ex: `AbrirChamadoTIAction`), altere os textos de retorno e os links para que correspondam aos sistemas e procedimentos da sua empresa.

### Executando o Programa

Com o ambiente virtual ativo, rode o arquivo principal:
```bash
python main.py
```

## 🛣️ Roadmap Futuro

-   [ ] Evoluir o sistema de menu para uma IA conversacional que entende a intenção do usuário.
-   [ ] Integrar com APIs de sistemas de tickets (GLPI, Jira) para abrir e consultar chamados automaticamente.
-   [ ] Adicionar mais fluxos de diagnóstico guiado para outros problemas comuns.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
Feito com ❤️ por **Leomario** - [**Conecte-se comigo no LinkedIn!**](https://www.linkedin.com/in/leomaario/)