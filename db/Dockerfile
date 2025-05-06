# Dockerfile
FROM postgres:15

# Instala as locales pt_BR
RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# Configura o locale pt_BR.UTF-8
RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8