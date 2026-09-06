import os
import time
import urllib.parse
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_disparos():
    caminho_csv = 'leads_tratados.csv'
    
    if not os.path.exists(caminho_csv):
        print(f"Erro: Arquivo '{caminho_csv}' não encontrado!")
        return

    df = pd.read_csv(caminho_csv)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")

    print("\n--------------------------------------------------")
    print("Aguardando carregamento do WhatsApp Web...")
    print("--------------------------------------------------\n")
    
    time.sleep(10)
    
    # Salva print da tela do QR Code
    driver.save_screenshot("qrcode.png")
    print("Captura do QR Code salva em 'qrcode.png'.")

    # Aguarda autenticação via QR Code (até 3 minutos)
    try:
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="side"] | //div[@data-tab="3"]'))
        )
        print("WhatsApp Web autenticado com sucesso! Iniciando disparos em segundo plano...\n")
    except Exception:
        print("Tempo esgotado para leitura do QR Code ou erro na autenticação.")
        driver.quit()
        return

    tot_sucesso = 0
    tot_falha = 0
    tempo_espera_segundos = 180  # 3 minutos exatos por mensagem

    for index, linha in df.iterrows():
        nome = str(linha.get('Nome_Tratado', 'Cliente'))
        if nome.lower() == 'nan' or not nome:
            nome = 'Cliente'

        telefone = str(linha.get('Telefone_Limpo', linha.get('WhatsApp_Formatado', '')))
        if '.' in telefone:
            telefone = telefone.split('.')[0]

        if not telefone or len(telefone) < 12:
            print(f"[{index + 1}/{len(df)}] Ignorado: Telefone inválido para {nome}.")
            tot_falha += 1
            continue

        mensagem = (
            f"Olá {nome}, tudo bem?\n\n"
            f"Conheça a *Mason Hub Academy*! Acesse nossa plataforma para obter a apostila e ver detalhes da formação:\n"
            f"https://masonhubacademy-byte.github.io/masonhubacademy/"
        )

        texto_encoded = urllib.parse.quote(mensagem)
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto_encoded}"

        driver.get(link)

        try:
            btn_enviar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"] | //button[@aria-label="Enviar"] | //button[contains(@class, "tvf2e")]'))
            )
            time.sleep(3)
            btn_enviar.click()
            tot_sucesso += 1
            
            hora_atual = datetime.now().strftime('%H:%M:%S')
            print(f"[{hora_atual}] [{index + 1}/{len(df)}] Sucesso: Mensagem enviada para {nome} ({telefone})")
            
            print("Aguardando 3 minutos para a próxima mensagem...")
            time.sleep(tempo_espera_segundos)

        except Exception:
            tot_falha += 1
            print(f"[{index + 1}/{len(df)}] Falha: Não foi possível enviar para {nome} ({telefone}).")
            time.sleep(5)

    print("\n--------------------------------------------------")
    print("Processo finalizado!")
    print(f"Enviados com sucesso: {tot_sucesso}")
    print(f"Falhas/Ignorados: {tot_falha}")
    print("--------------------------------------------------\n")
    
    driver.quit()

if __name__ == "__main__":
    iniciar_disparos()