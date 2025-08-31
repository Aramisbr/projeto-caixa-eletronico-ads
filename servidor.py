import socket

HOST = '127.0.0.1'
PORTA = 65432
LOGIN_VALIDO = '1152025100178'
SENHA_VALIDA = '123456'

# Cria um objeto socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORTA))
    
    # Aguarda conexão
    s.listen(1)
    
    print(f"Servidor escutando em {HOST}:{PORTA}")
    
    # Aceita uma nova conexão
    conn, addr = s.accept()
    
    # Garante que a conexão seja encerrada
    with conn:
        print(f"Conectado por {addr}")
        
        # AUTENTICAÇÃO
        while True:
            login = conn.recv(1024).decode()
            senha = conn.recv(1024).decode()
            
            print(f"Login recebido: {login}")
            print(f"Senha recebida: {senha}")
            
            # Verifica se o login e a senha estão corretos
            if login == LOGIN_VALIDO and senha == SENHA_VALIDA:
                conn.sendall(b'sucesso')
                print("Autenticação bem-sucedida. Encerrando o servidor para a primeira etapa.")
                
                saldo = 0.0
                
                # Loop para as operações
                while True:
                    # Recebe a opção escolhida
                    opcao = conn.recv(1024).decode()
                    
                    # DEPOSITAR
                    if opcao == '1':
                        print("Cliente escolheu a opção DEPOSITAR.")
                        valor_str = conn.recv(1024).decode()
                        valor = float(valor_str)
                        saldo += valor
                        resposta = f"Novo saldo: {saldo}"
                        conn.sendall(resposta.encode())
                        print(f"Depósito de R${valor} realizado. Saldo atual: R${saldo}")
                    
                    # SACAR
                    elif opcao == '2':
                        print("Cliente escolheu a opção SACAR.")
                        valor_str = conn.recv(1024).decode()
                        valor = float(valor_str)
                        # Verifica se há saldo suficiente
                        if valor > saldo:
                            conn.sendall(b'Saldo insuficiente')
                            print(f"Tentativa de saque de R${valor}. Saldo insuficiente.")
                        else:
                            saldo -= valor
                            resposta = f"Novo saldo: {saldo}"
                            conn.sendall(resposta.encode())
                            print(f"Saque de R${valor} realizado. Saldo atual: R${saldo}")
                            
                    # SALDO
                    elif opcao == '3':
                        print("Cliente escolheu a opção VISUALIZAR SALDO.")
                        resposta = f"Saldo: {saldo}"
                        conn.sendall(resposta.encode())
                        print(f"Saldo de R${saldo} enviado para o cliente.")
                        
                    # SAIR
                    elif opcao == '4':
                        print("Cliente escolheu a opção SAIR. Encerrando conexão com este cliente.")
                        break            
            else:
                conn.sendall(b'falha')
                print("Autenticação falhou. Aguardando nova tentativa do cliente.")
