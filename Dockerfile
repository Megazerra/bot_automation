FROM python:3.9-slim

# --- Configuración básica ---
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/app
ENV DISPLAY=99

RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    echo "America/New_York" > /etc/timezone

# Se asume que el WORKDIR original es /app
WORKDIR /app

#RUN apt update && apt install software-properties-common -y && \
 #   apt install python3.9 -y

# Instalar dependencias del sistema: wget, gnupg, curl, unzip, Python y pip
RUN apt-get update && \
    apt-get install -y wget gnupg curl unzip python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && apt install systemctl -y && \
    apt install ssh -y && \
    apt-get install -y net-tools

# Añadir la llave pública de Google y el repositorio para Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Instalar Google Chrome Stable
RUN apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Descarga e instala ChromeDriver (Chrome for Testing) compatible con la versión 133 de Chrome
RUN wget -O /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.126/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip
    #mv /usr/local/bin/chrome-linux64/chromedriver /usr/local/bin/chromedriver && \
    #chmod +x /usr/local/bin/chromedriver && \
    #rm -rf /usr/local/bin/chrome-linux64

# --- Incorporar tu proyecto Python ---
COPY requirements.txt /app/requirements.txt
COPY presets /app/presets
COPY common /app/common
COPY actions /app/actions
COPY capcha_evasion /app/capcha_evasion

# Instalar Requirements
RUN pip install -r requirements.txt

