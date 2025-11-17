# Gerador de QR Code -- README (Versão Atualizada)

## 📌 Sobre o Projeto

Este projeto é um **gerador avançado de QR Codes com interface
gráfica**, construído em Python usando Tkinter.\
Inclui diversos tipos de QR Code, preview ao vivo e exportação em
PNG/PDF.

### 🆕 **Principais Recursos**

-   **Preview automático** (atualiza sem clicar em botão)\
-   Suporte a **QR Code de Wi-Fi completo**, com:
    -   SSID\
    -   Senha\
    -   Seleção de segurança (WPA, WPA2, WPA3, WEP, nopass)
-   Suporte a:
    -   Texto\
    -   URL\
    -   E-mail\
    -   WhatsApp\
    -   Telefone\
-   **Fundo totalmente transparente (PNG)**\
-   Inserção de **logo com transparência**\
-   Exportação para **PNG** e **PDF**\
-   Janela com **scroll**\
-   Interface organizada e moderna

------------------------------------------------------------------------

## 📦 Requisitos

### ✔ Bibliotecas necessárias

Instale com:

``` bash
pip install qrcode[pil]
pip install pillow
pip install reportlab
```

Se estiver no Linux e faltar o Tkinter:

``` bash
sudo apt update
sudo apt install python3-tk -y
```

------------------------------------------------------------------------

## 🚀 Como Executar o Programa

1.  Salve o arquivo do script (ex.: `gerador_qr.py`)
2.  No terminal:

``` bash
python gerador_qr.py
```

A interface abrirá automaticamente.

------------------------------------------------------------------------

## 🧱 Estrutura do Programa

O programa conta com:

-   Interface gráfica completa (Tkinter)
-   Área dinâmica que muda dependendo do tipo de QR Code
-   Preview automático sempre que qualquer valor é alterado
-   Suporte a fundo transparente real (RGBA)
-   QR Code compatível com padrões internacionais

------------------------------------------------------------------------

## 📡 QR Code de Wi-Fi --- Como funciona

O QR Code segue o padrão internacional:

    WIFI:T:<segurança>;S:<SSID>;P:<senha>;;

✔ Permite conexão automática\
✔ Seguranças suportadas:

-   WPA\
-   WPA2\
-   WPA3\
-   WEP\
-   nopass (rede aberta)

------------------------------------------------------------------------

## 🛠 Como Compilar para EXE (Opcional)

### 1. Instale o PyInstaller

``` bash
pip install pyinstaller
```

### 2. Crie o executável

``` bash
pyinstaller --noconsole --onefile --windowed gerador_qr.py
```

### 3. Com ícone

``` bash
pyinstaller --noconsole --onefile --windowed --icon=icone.ico gerador_qr.py
```

------------------------------------------------------------------------

## 📄 Licença

Uso totalmente livre.

------------------------------------------------------------------------
