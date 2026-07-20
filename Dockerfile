FROM ubuntu:latest

# Instalar o servidor SSH e o sudo
RUN apt-get update && apt-get install -y openssh-server sudo

# Criar o diretório de execução do SSH
RUN mkdir -p /var/run/sshd

# Criar um usuário legítimo para os testes de comportamento normal
RUN useradd -rm -d /home/admin_tcc -s /bin/bash -g root -G sudo -u 1001 admin_tcc
RUN echo 'admin_tcc:senha_segura' | chpasswd

# Configurar a senha do root para servir de alvo para o Brute Force
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# ---> DESATIVAR AS DEFESAS DO SSH PARA O EXPERIMENTO <---
RUN echo 'PerSourcePenalties no' >> /etc/ssh/sshd_config
RUN echo 'MaxStartups 100:30:200' >> /etc/ssh/sshd_config

# Expor a porta padrão do SSH
EXPOSE 22

# Iniciar o serviço em segundo plano (enviando logs para o console)
CMD ["/usr/sbin/sshd", "-D", "-e"]