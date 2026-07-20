import random
import datetime
import re

IP_LEGITIMO = "187.12.5.42"
IPS_ATAQUE = ["95.161.22.128", "45.250.247.54", "195.241.151.7"]
tempo_atual = datetime.datetime.now()

with open("dataset_auth.log", "r", encoding="utf-16", errors="ignore") as f:
    texto_bruto = f.read()

texto_limpo = texto_bruto.replace("\x00", "").replace("\n", " ")
padroes = r'(Failed password|Accepted password|Connection closed|Timeout before)'
fragmentos = re.split(padroes, texto_limpo)
log_final = []

for i in range(1, len(fragmentos), 2):
    tipo_log = fragmentos[i]         
    resto_log = fragmentos[i+1]      
    linha_completa = f"{tipo_log}{resto_log}".strip()
    linha_completa = re.sub(r'\s+', ' ', linha_completa) 
    
    comando_injetado = ""

    # Mascaramento de IPs e Injeção de Comandos (O que o Kayo pediu!)
    if "admin_tcc" in linha_completa:
        linha_mascarada = linha_completa.replace("172.17.0.1", IP_LEGITIMO)
        # Se for um login com sucesso do admin, 90% das vezes é normal, 10% é o Scan de Portas (Anomalia)
        if "Accepted password" in linha_completa:
            if random.random() > 0.10:
                comando_injetado = " COMMAND=/bin/bash" # Trabalho normal
            else:
                comando_injetado = " COMMAND=nmap -sS -p 22,80,443 192.168.1.0/24" # O SCAN DE PORTAS
                
    elif "root" in linha_completa:
        linha_mascarada = linha_completa.replace("172.17.0.1", random.choice(IPS_ATAQUE))
        # Se o bruteforce acertar a senha, ele tenta roubar as senhas do servidor
        if "Accepted password" in linha_completa:
            comando_injetado = " COMMAND=/usr/bin/cat /etc/shadow" # O COMANDO SHADOW
            
    else:
        linha_mascarada = linha_completa.replace("172.17.0.1", "10.0.0.5")

    tempo_atual += datetime.timedelta(seconds=random.randint(1, 3))
    timestamp = tempo_atual.strftime("%b %d %H:%M:%S")

    # Adiciona o log e o comando injetado no final
    log_final.append(f"{timestamp} honeypot-server sshd[1024]: {linha_mascarada}{comando_injetado}")

with open("linux_auth_logs_labeled.txt", "w", encoding="utf-8") as f:
    for log in log_final:
        f.write(log + "\n")

print("[+] Dataset Evoluído! Logs com Comandos Injetados (Shadow e Port Scan) gerados.")