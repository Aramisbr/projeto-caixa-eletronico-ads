import socket

HOST = '127.0.0.1'
PORTA = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORTA))
    
    print(f"Conectado ao servidor em {HOST}:{PORTA}")

    # AUTENTICAÇÃO
    while True:
        login = input("Login (matrícula): ")
        senha = input("Senha: ")
        
        # Envia o login para o servidor
        s.sendall(login.encode())
        
        # Envia a senha para o servidor
        s.sendall(senha.encode())
        
        # Resposta do servidor.
        resposta = s.recv(1024).decode()
        
        if resposta == 'sucesso':
            print("\nLogin realizado com sucesso!")
            while True:
                print("Digite a opção que deseja realizar:")
                print("1 - Depositar")
                print("2 - Sacar") 
                print("3 - Visualizar Saldo") 
                print("4 - Sair") 
                
                opcao = input("> ")
                
                # Envia a opção escolhida para o servidor
                s.sendall(opcao.encode())
                
                # DEPOSITAR
                if opcao == '1':
                    valor_str = input("Quanto deseja depositar: ")
                    s.sendall(valor_str.encode()) 
                    resposta_servidor = s.recv(1024).decode()
                    print(resposta_servidor, "\n")
                    
                # SACAR
                elif opcao == '2':
                    valor_str = input("Quanto deseja sacar: ")
                    s.sendall(valor_str.encode()) 
                    resposta_servidor = s.recv(1024).decode() 
                    print(resposta_servidor, "\n")
                
                # SALDO
                elif opcao == '3':
                    resposta_servidor = s.recv(1024).decode() 
                    print(resposta_servidor, "\n")
                
                # SAIR
                elif opcao == '4':
                    print("Até mais!")
                    break 
                
                # OPÇÃO INVÁLIDA
                else:
                    print("Opção inválida, por favor tente novamente.\n")
                    
            break
        else:
            print("\nLogin ou senha incorreta. Tente novamente.")

print("Conexão encerrada.")