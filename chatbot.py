import os
from dotenv import load_dotenv

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
  else:
    print('Opção inválida. Tente novamente.')

mensagens = [] #Listas
while True:
  pergunta = input('Usuário: ')
  if pergunta.lower() == 'x':
    break

  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens, documento)
  mensagens.append(('assistant', resposta))
  print('Osvaldinho: ', resposta)

print('\nBot: Até a próxima!')
print('Abaixo está seu histórico')
print(mensagens)