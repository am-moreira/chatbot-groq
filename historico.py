import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Função para exibir o histórico no terminal
def exibir_historico(mensagens):
    print("\nHistórico de conversas:")
    for index, (quem, mensagem) in enumerate(mensagens):
        if quem == 'user':
            print(f"Usuário: {mensagem}")
        elif quem == 'assistant':
            print(f"Osvaldinho: {mensagem}")

# Função para salvar o histórico em arquivo TXT
def historico_txt(mensagens, nome_arquivo="historico_conversa.txt"):
    with open(nome_arquivo, "w", encoding="utf-8") as file:
        file.write("Histórico da Conversa:\n")
        for role, mensagem in mensagens:
            if role == 'user':
                file.write(f"Usuário: {mensagem}\n")
            elif role == 'assistant':
                file.write(f"Osvaldinho: {mensagem}\n")
    print(f"Histórico salvo em {nome_arquivo}")

# Função para salvar o histórico em arquivo CSV
def historico_csv(mensagens, nome_arquivo="historico_conversa.csv"):
    with open(nome_arquivo, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Papel", "Mensagem"])
        for role, mensagem in mensagens:
            writer.writerow([role, mensagem])
    print(f"Histórico salvo em {nome_arquivo}")

# Função para salvar o histórico em PDF
def historico_pdf(mensagens, nome_arquivo="historico_conversa.pdf"):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.setFont("Helvetica", 10)

    width, height = letter
    y = height - 40  # Posição inicial para o texto

    c.drawString(100, y, "Histórico da Conversa:")
    y -= 20

    for role, mensagem in mensagens:
        if role == 'user':
            c.drawString(100, y, f"Usuário: {mensagem}")
        elif role == 'assistant':
            c.drawString(100, y, f"Osvaldinho: {mensagem}")
        y -= 20
        if y < 40:  # Se a página estiver cheia, cria uma nova página
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40

    c.save()
    print(f"Histórico salvo em {nome_arquivo}")
