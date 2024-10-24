import os
from dotenv import load_dotenv
from historico import exibir_historico, historico_txt, historico_csv, historico_pdf

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import YoutubeLoader

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")

chat = ChatGroq(model='llama3-70b-8192', temperature=0.5)

def resposta_bot(mensagens, documento):
  msg_system = '''
  Você é um assistente simpático e seu nome é Osvaldinho. De preferência responda com respostas curtas e objetivas.
  Você utiliza as seguintes informações para formular suas respostas: {informacoes}
  '''
  mensagem_modelo = [('system', msg_system)]
  mensagem_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagem_modelo)
  chain = template | chat
  return chain.invoke({'informacoes': documento}).content

def carrega_site():
  # https://colegioprovecto.com.br
  url_site = input('Digite a URL do site: ')
  loader = WebBaseLoader(url_site)
  dados = loader.load()
  documento = ''
  for doc in dados:
    documento += doc.page_content
  return documento

def carrega_pdf():
  caminho = '/content/drive/MyDrive/Colab Notebooks/Provecto - Sobre.pdf'
  loader = PyPDFLoader(caminho)
  dados_pdf = loader.load()
  documento = ''
  for doc in dados_pdf:
    documento += doc.page_content
  return documento

def carrega_youtube():
  # https://www.youtube.com/watch?v=ro2ttE2kqmU
  url_youtube = input('Digite a URL do vídeo: ')
  loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
  dados_youtube = loader.load()
  documento = ''
  for doc in dados_youtube:
    documento += doc.page_content
  return documento

def mostrar_menu_salvamento(mensagens):
    while True:
        print("\nVocê deseja salvar o histórico de conversa?")
        print("1 - Salvar como TXT")
        print("2 - Salvar como CSV")
        print("3 - Salvar como PDF")
        print("x - Não salvar e sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            historico_txt(mensagens)
            break
        elif opcao == '2':
            historico_csv(mensagens)
            break
        elif opcao == '3':
            historico_pdf(mensagens)
            break
        elif opcao.lower() == 'x':
            print("Saindo sem salvar o histórico.")
            break
        else:
            print("Opção inválida. Tente novamente.")

print('Bem-vindo ao Osvaldinho!\n Escolha uma das opções abaixo para começar a conversar:')

txt_selecao = '''
Digite 1 - Conversar com Site
Digite 2 - Conversar com Vídeo do Youtube
Digite 3 - Conversar com PDF
\n
Digite x - Sair
'''
while True:
    selecao = input(txt_selecao)
    if selecao == '1':
        documento = carrega_site()
        break
    elif selecao == '2':
        documento = carrega_youtube()
        break
    elif selecao == '3':
        documento = carrega_pdf()
        break
    elif selecao.lower() == 'x':
        print("Saindo...")
        exit()  # Encerra o programa
    else:
        print('Opção inválida. Tente novamente.')

mensagens = []  # Lista de mensagens
while True:
    pergunta = input('Usuário: ')
    if pergunta.lower() == 'x':
        exibir_historico(mensagens)  # Exibe o histórico antes de perguntar sobre salvar
        mostrar_menu_salvamento(mensagens)  # Chama o menu de salvamento
        break  # Sai do loop após salvar ou optar por não salvar

    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta))
    print('Osvaldinho: ', resposta)

print('Bot: Até a próxima!')