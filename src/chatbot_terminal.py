import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o cliente da API. 
# Importante: O código busca automaticamente a variável OPENAI_API_KEY
client = OpenAI()

def iniciar_chatbot():
    print("🤖 Olá, Sou o Alexandri.ia, seu tutor virtual de História e Geografia.")
    print("Digite 'sair' a qualquer momento para encerrar nossa conversa.\n")

    # Define a "personalidade" e o contexto do LLM (System Prompt)
    mensagens = [
        {"role": "system", "content": "Você é um professor de História e Geografia didático, paciente e focado. Suas respostas devem ser curtas, diretas e adequadas para estudantes."}
    ]

    # Loop principal de interação com o usuário
    while True:
        pergunta = input("Você: ")

        # Condição de parada solicitada na atividade
        if pergunta.strip().lower() == 'sair':
            print("EducaBot: Foi ótimo estudar com você! Até a próxima e bons estudos!")
            break

        # Adiciona a pergunta do usuário ao histórico da conversa
        mensagens.append({"role": "user", "content": pergunta})

        try:
            # Chamada à API para gerar a resposta
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo", # Modelo rápido e de baixo custo
                messages=mensagens,
                max_tokens=150, # Garante que as respostas sejam curtas
                temperature=0.7 # Equilibra coerência com um pouco de criatividade didática
            )

            conteudo_resposta = resposta.choices[0].message.content
            print(f"\nEducaBot: {conteudo_resposta}\n")

            # Adiciona a resposta do bot ao histórico para manter o contexto
            mensagens.append({"role": "assistant", "content": conteudo_resposta})

        except Exception as e:
            # Tratamento de erro básico (útil para garantir a qualidade/QA do software)
            print(f"\nErro ao se comunicar com a API: Verifique sua chave ou conexão. Detalhes: {e}\n")

if __name__ == "__main__":
    iniciar_chatbot()