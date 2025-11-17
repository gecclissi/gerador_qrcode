# Gerador de QR Code - README

## 📌 Sobre o Projeto
Este projeto é uma interface gráfica em Python para gerar QR Codes personalizados. Ele permite criar QR Codes de diferentes tipos (texto, e-mail, WhatsApp, URL etc.), visualizar o preview e fazer download da imagem.

A interface inclui:
- Layout estilizado
- Botões organizados lado a lado
- Área de preview rolável (scroll)
- Opções de exportação em PNG, JPEG e PDF
- Suporte a múltiplos tipos de QR Code por meio de switch-case (`match/case`)

---

## 📦 Requisitos
Para executar o programa, você precisa ter instalado:
- Python 3.10 ou superior

### ✔ Bibliotecas Python necessárias
Execute no terminal:
```bash
pip install qrcode
pip install pillow
pip install reportlab
```
Se estiver no Linux e faltar o Tkinter:
```bash
sudo apt update
sudo apt install python3-tk -y
```

---

## 🚀 Como Executar o Programa
1. Baixe o arquivo Python contendo a interface.
2. Abra o terminal ou CMD no diretório do arquivo.
3. Execute:
```bash
python nome_do_arquivo.py
```
A interface será aberta automaticamente.

---

## 🧱 Estrutura do Programa
O script possui:
- Uma janela principal com layout organizado
- Scroll para evitar que botões desapareçam quando o QR Code é visualizado
- Preview em tempo real
- Sistema "switch-case" para gerar diferentes tipos de QR Code
- Função de salvar em diferentes formatos
- Estilização básica (cores, espaçamentos e alinhamentos)

---

## 🛠 Como Compilar para EXE (Opcional)
Se quiser transformar o script em um executável para Windows:

### 1. Instale o PyInstaller
```bash
pip install pyinstaller
```

### 2. Gere o executável
```bash
pyinstaller --noconsole --onefile --windowed nome_do_arquivo.py
```

O executável ficará dentro da pasta:
```
dist/
```

### 3. (Opcional) Personalizar com ícone
```bash
pyinstaller --noconsole --onefile --windowed --icon=icone.ico nome_do_arquivo.py
```

---

## 📄 Licença
Este projeto é completamente livre para uso, modificação e distribuição.

---

## 💬 Suporte
Se quiser:
- Criar uma versão dark mode
- Transformar em aplicativo instalável
- Adicionar novos tipos de QR Code
- Gerar códigos em lote

É só pedir! 😊
