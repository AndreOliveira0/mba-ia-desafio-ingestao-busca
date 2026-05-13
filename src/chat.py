from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("-" * 60)
    print("Bem-vindo ao Desafio Ingestao de Busca!")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("-" * 60)
    
    while True:
        try:
            pergunta = input("\nPERGUNTA: ").strip()
            
            if pergunta.lower() == "sair":
                print("SISTEMA: Até logo!\n")
                break
            
            if not pergunta:
                print("SISTEMA: Por favor, digite uma pergunta válida.")
                continue

            resposta = chain.invoke({"question": pergunta})
            print(f"RESPOSTA: {resposta}")
        except KeyboardInterrupt:
            print("\nSISTEMA: Até logo!\n")
            break
        except Exception as e:
            print(f"\nSISTEMA: Erro ao processar a pergunta: {e}\n")
            break

if __name__ == "__main__":
    main()