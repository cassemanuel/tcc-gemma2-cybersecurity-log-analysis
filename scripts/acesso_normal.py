import paramiko
import time

def acesso_legitimo():
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Usa as credenciais corretas definidas no Dockerfile
        cliente.connect('127.0.0.1', port=2222, username='admin_tcc', password='senha_segura')
        print("[+] Acesso legítimo realizado com sucesso.")
        
        # Simula uma ação normal de administrador
        stdin, stdout, stderr = cliente.exec_command('ls -la /var/log')
        time.sleep(2)
        
    except Exception as e:
        print(f"[-] Erro na conexão: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    for i in range(50):
        acesso_legitimo()
        time.sleep(3)