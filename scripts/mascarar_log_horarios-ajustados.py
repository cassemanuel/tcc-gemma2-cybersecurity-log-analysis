import random
import datetime
import re

# Constantes de IP
IP_LEGITIMO = "187.12.5.42"
IPS_ATAQUE = ["95.161.22.128", "45.250.247.54", "195.241.151.7"]

# Define o tempo inicial para o início de um expediente realista
tempo_atual = datetime.datetime(2026, 8, 1, 8, 0, 0)

# Leitura do dataset bruto
with open("dataset_auth.log", "r", encoding="utf-16", errors="ignore") as f:
    texto_bruto = f.read()

texto_limpo = texto_bruto.replace("\x00", "").replace("\n", " ")
padroes = r'(Failed password|Accepted password|Connection closed|Timeout before)'
fragmentos = re.split(padroes, texto_limpo)
log_final = []

# Processamento e injeção de comportamento
for i in range(1, len(fragmentos), 2):
    tipo_log = fragmentos[i]         
    resto_log = fragmentos[i+1]      
    linha_completa = f"{tipo_log}{resto_log}".strip()
    linha_completa = re.sub(r'\s+', ' ', linha_completa) 
    
    comando_injetado = ""

    # LÓGICA UNIFICADA: Mascaramento, Injeção e Timestamps baseados em Horário
    if "admin_tcc" in linha_completa:
        linha_mascarada = linha_completa.replace("172.17.0.1", IP_LEGITIMO)
        
        if "Accepted password" in linha_completa:
            if random.random() > 0.10:
                comando_injetado = " COMMAND=/bin/bash"
            else:
                comando_injetado = " COMMAND=nmap -sS -p 22,80,443 192.168.1.0/24"
                
        # Validação do horário comercial (08:00 às 17:59)
        if 8 <= tempo_atual.hour < 18:
            # Horário de pico: ações espaçadas por minutos (ex: 2 a 15 minutos)
            delta_tempo = random.randint(120, 900) 
        else:
            # Madrugada/Noite: servidor ocioso, intervalos de horas (ex: 1 a 4 horas)
            delta_tempo = random.randint(3600, 14400) 

    elif "root" in linha_completa:
        linha_mascarada = linha_completa.replace("172.17.0.1", random.choice(IPS_ATAQUE))
        
        if "Accepted password" in linha_completa:
            comando_injetado = " COMMAND=/usr/bin/cat /etc/shadow"
            
        # Ataque de força bruta e scan: rajadas rápidas (1 a 3 segundos), independente da hora
        delta_tempo = random.randint(1, 3)

    else:
        # Eventos genéricos do sistema (fechamento de portas, timeouts)
        linha_mascarada = linha_completa.replace("172.17.0.1", "10.0.0.5")
        
        if 8 <= tempo_atual.hour < 18:
            delta_tempo = random.randint(60, 300)
        else:
            delta_tempo = random.randint(1800, 7200)

    # Aplica o avanço do tempo
    tempo_atual += datetime.timedelta(seconds=delta_tempo)
    timestamp = tempo_atual.strftime("%b %d %H:%M:%S")

    # Adiciona o log final formatado na lista
    log_final.append(f"{timestamp} honeypot-server sshd[1024]: {linha_mascarada}{comando_injetado}")

# Gravação do novo dataset evoluído
with open("linux_auth_logs_labeled.txt", "w", encoding="utf-8") as f:
    for log in log_final:
        f.write(log + "\n")

print("[+] Dataset Evoluído! Logs com ciclo dia/noite e Comandos Injetados gerados com sucesso.")
