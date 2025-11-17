import qrcode
import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
from reportlab.platypus import SimpleDocTemplate, Image as PDFImage
from reportlab.lib.pagesizes import letter

# ---------------------- Função para gerar QR ----------------------
def gerar_qrcode(dados, cor_fg, cor_bg, logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(dados)
    qr.make(fit=True)

    img = qr.make_image(fill_color=cor_fg, back_color=cor_bg).convert("RGB")

    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((80, 80))
            img_w, img_h = img.size
            img.paste(logo, ((img_w - 80) // 2, (img_h - 80) // 2), logo)
        except:
            pass

    return img

# ---------------------- Salvar em PDF ----------------------
def salvar_pdf(img, caminho):
    pdf = SimpleDocTemplate(caminho, pagesize=letter)
    temp_path = "temp_qr.png"
    img.save(temp_path)
    pdf_img = PDFImage(temp_path, width=300, height=300)
    pdf.build([pdf_img])
    os.remove(temp_path)

# ---------------------- Função principal GUI ----------------------
def iniciar_interface():
    root = tk.Tk()
    root.title("Gerador Completo de QR Codes")
    root.geometry("620x700")
    root.configure(bg="#e6e6e6")

    dados_var = tk.StringVar()
    cor_fg = "black"
    cor_bg = "white"
    logo_path = None

    # ---------------- SCROLL AREA ----------------
    main_canvas = tk.Canvas(root, bg="#e6e6e6", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    scroll_frame = tk.Frame(main_canvas, bg="#ffffff")

    scroll_frame.bind(
        "<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )

    main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    main_canvas.configure(yscrollcommand=scrollbar.set)

    main_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------------- CONTAINER INTERNO ----------------
    container = tk.Frame(scroll_frame, bg="#ffffff", bd=2, relief="groove")
    container.pack(padx=20, pady=20, fill="both", expand=True)

    titulo = tk.Label(container, text="Gerador Completo de QR Codes", font=("Arial", 16, "bold"), bg="#ffffff")
    titulo.pack(pady=10)

    # -------- Seleção do tipo de QR --------
    tk.Label(container, text="Tipo de QR Code:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", padx=15, pady=5)
    tipo_var = tk.StringVar(value="texto")

    tipos = ["texto", "url", "email", "whatsapp", "wifi", "telefone"]
    radio_frame = tk.Frame(container, bg="#ffffff")
    radio_frame.pack(anchor="w", padx=20)

    # Colocar os radio buttons em linha
    col = 0
    for t in tipos:
        tk.Radiobutton(
            radio_frame,
            text=t.capitalize(),
            value=t,
            variable=tipo_var,
            bg="#ffffff"
        ).grid(row=0, column=col, padx=8)
        col += 1

    # -------- Entrada de dados --------
    tk.Label(container, text="Conteúdo: ", bg="#ffffff", font=("Arial", 12)).pack(anchor="w", padx=15, pady=5)
    entrada = tk.Entry(container, textvariable=dados_var, width=45, font=("Arial", 11), bd=2, relief="groove")
    entrada.pack(pady=5)

    # -------- Funções auxiliares --------
    def selecionar_logo():
        nonlocal logo_path
        logo_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg")])
        if logo_path:
            messagebox.showinfo("Logo", "Logo selecionado!")

    def escolher_cor_fg():
        nonlocal cor_fg
        cor_fg = colorchooser.askcolor()[1]

    def escolher_cor_bg():
        nonlocal cor_bg
        cor_bg = colorchooser.askcolor()[1]

    # -------- Botões em linha --------
    linha_btns = tk.Frame(container, bg="#ffffff")
    linha_btns.pack(pady=10)

    tk.Button(linha_btns, text="Selecionar Logo", command=selecionar_logo, bg="#1e90ff", fg="white", pady=5, padx=10).grid(row=0, column=0, padx=5)
    tk.Button(linha_btns, text="Cor QR", command=escolher_cor_fg, bg="#32cd32", fg="white", pady=5, padx=10).grid(row=0, column=1, padx=5)
    tk.Button(linha_btns, text="Cor Fundo", command=escolher_cor_bg, bg="#ff8c00", fg="white", pady=5, padx=10).grid(row=0, column=2, padx=5)

    preview_label = tk.Label(container, bg="#ffffff")
    preview_label.pack(pady=10)

    # -------- Preview --------
    def gerar_preview():
        tipo = tipo_var.get()
        conteudo = dados_var.get()

        match tipo:
            case "texto": dados = conteudo
            case "url": dados = conteudo
            case "email": dados = f"mailto:{conteudo}"
            case "whatsapp": dados = f"https://wa.me/{conteudo}"
            case "wifi": 
                ssid, senha = conteudo.split(",")
                dados = f"WIFI:T:WPA;S:{ssid};P:{senha};;"
            case "telefone": dados = f"tel:{conteudo}"

        img = gerar_qrcode(dados, cor_fg, cor_bg, logo_path)
        img_preview = img.resize((220, 220))
        img_tk = ImageTk.PhotoImage(img_preview)

        preview_label.config(image=img_tk)
        preview_label.image = img_tk

        return img, dados

    tk.Button(container, text="Gerar Preview", command=gerar_preview, bg="#5555ff", fg="white", pady=7, width=20).pack(pady=10)

    # -------- Salvar PNG --------
    def salvar_png():
        img, _ = gerar_preview()
        caminho = filedialog.asksaveasfilename(defaultextension=".png")
        if caminho:
            img.save(caminho)
            messagebox.showinfo("Sucesso", "QR Code salvo como PNG!")

    # -------- Salvar PDF --------
    def salvar_como_pdf():
        img, _ = gerar_preview()
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf")
        if caminho:
            salvar_pdf(img, caminho)
            messagebox.showinfo("Sucesso", "QR Code salvo em PDF!")

    tk.Button(container, text="Salvar como PNG", command=salvar_png, bg="#008000", fg="white", pady=7, width=20).pack(pady=5)
    tk.Button(container, text="Salvar como PDF", command=salvar_como_pdf, bg="#b22222", fg="white", pady=7, width=20).pack(pady=5)

    root.mainloop()

# ---------------------- Executar ----------------------
if __name__ == "__main__":
    iniciar_interface()
