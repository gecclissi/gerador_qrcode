#!/usr/bin/env python3
"""
Gerador Completo de QR Codes — versão ajustada sem campo conteúdo no modo Wi-Fi
e sem o botão toggle fullscreen.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageColor, ImageOps
import qrcode
import io
import os
from reportlab.pdfgen import canvas as pdf_canvas

# ---------------- CONFIG ----------------
PREVIEW_DISPLAY_SIZE = 260
MIN_RES = 200
PRESET_OPTIONS = [200, 600, 1200, 2000, 4000]
CHECKER_SQUARE = 20
CHECKER_COLOR_A = (242, 242, 242, 255)
CHECKER_COLOR_B = (224, 224, 224, 255)

# ---------------- Helpers ----------------
def parse_color(col):
    if not col:
        return (255,255,255,255)
    if isinstance(col, tuple):
        return (col[0], col[1], col[2], 255)
    if isinstance(col, str) and col.lower() == "transparent":
        return None
    try:
        rgb = ImageColor.getrgb(col)
        return (rgb[0], rgb[1], rgb[2], 255)
    except Exception:
        return (255,255,255,255)

def build_qr_mask(dados, tamanho):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(dados)
    qr.make(fit=True)
    mask = qr.make_image(fill_color="black", back_color="white").convert("L")
    module_mask = mask.point(lambda p: 255 if p < 128 else 0)
    module_mask = module_mask.resize((tamanho, tamanho), Image.NEAREST)
    return module_mask

def gera_qr_image(dados: str, fg: str, bg: str, tamanho: int, logo_path=None):
    if tamanho <= 0:
        tamanho = MIN_RES
    module_mask = build_qr_mask(dados, tamanho)
    fg_rgba = parse_color(fg) or (0,0,0,255)

    base = Image.new("RGBA", (tamanho, tamanho), (0,0,0,0))
    fg_layer = Image.new("RGBA", (tamanho, tamanho), fg_rgba)
    base.paste(fg_layer, (0,0), module_mask)

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_size = max(40, tamanho // 6)
            logo = ImageOps.contain(logo, (logo_size, logo_size), Image.LANCZOS)
            lx, ly = logo.size
            base.paste(logo, ((tamanho - lx)//2, (tamanho - ly)//2), logo)
        except Exception:
            pass

    bg_rgba = parse_color(bg)
    if bg_rgba is None:
        final = base
    else:
        bg_img = Image.new("RGBA", (tamanho, tamanho), bg_rgba)
        final = Image.alpha_composite(bg_img, base)

    return final

def gera_checkerboard(size, square=CHECKER_SQUARE, colorA=CHECKER_COLOR_A, colorB=CHECKER_COLOR_B):
    cb = Image.new("RGBA", (size, size), (0,0,0,0))
    for y in range(0, size, square):
        for x in range(0, size, square):
            cor = colorA if ((x//square + y//square) % 2 == 0) else colorB
            for yy in range(y, min(y+square, size)):
                for xx in range(x, min(x+square, size)):
                    cb.putpixel((xx, yy), cor)
    return cb

# ---------------- UI ----------------
def iniciar_interface():
    root = tk.Tk()
    root.title("Gerador Completo de QR Codes")
    root.geometry("1000x720")
    root.minsize(900,600)

    state = {"dark": False, "logo_path": None}

    # Vars
    tipo_var = tk.StringVar(value="texto")
    conteudo_var = tk.StringVar()
    fg_var = tk.StringVar(value="#000000")
    bg_var = tk.StringVar(value="#ffffff")
    tamanho_var = tk.StringVar(value=str(PRESET_OPTIONS[0]))

    # Layout
    left = ttk.Frame(root)
    left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    right = ttk.Frame(root, width=340)
    right.pack(side="right", fill="y", padx=10, pady=10)

    # Tipo
    ttk.Label(left, text="Tipo de QR:").pack(anchor="w")
    tipos = ["texto","url","email","whatsapp","wifi","telefone"]
    tipo_menu = ttk.Combobox(left, values=tipos, textvariable=tipo_var, state="readonly")
    tipo_menu.pack(fill="x", pady=6)

    # Campo Conteúdo (deve SUMIR no modo Wi-Fi)
    conteudo_label = ttk.Label(left, text="Conteúdo:")
    conteudo_label.pack(anchor="w")
    conteudo_entry = ttk.Entry(left, textvariable=conteudo_var)
    conteudo_entry.pack(fill="x", pady=6)

    # Campos Wi-Fi
    wifi_frame = ttk.Frame(left)
    ssid_var = tk.StringVar()
    senha_var = tk.StringVar()
    seg_var = tk.StringVar(value="WPA2")

    ttk.Label(wifi_frame, text="SSID:").pack(anchor="w")
    ttk.Entry(wifi_frame, textvariable=ssid_var).pack(fill="x", pady=2)
    ttk.Label(wifi_frame, text="Senha:").pack(anchor="w")
    ttk.Entry(wifi_frame, textvariable=senha_var).pack(fill="x", pady=2)
    ttk.Label(wifi_frame, text="Segurança:").pack(anchor="w")
    ttk.Combobox(wifi_frame, values=["WPA","WPA2","WPA3","WEP","nopass"], textvariable=seg_var, state="readonly").pack(fill="x", pady=2)

    # Ocultar campo conteúdo no modo Wi-Fi
    def on_tipo_change(*_):
        if tipo_var.get() == "wifi":
            conteudo_label.pack_forget()
            conteudo_entry.pack_forget()
            wifi_frame.pack(fill="x", pady=6)
        else:
            conteudo_label.pack(anchor="w")
            conteudo_entry.pack(fill="x", pady=6)
            wifi_frame.pack_forget()
        atualizar_preview()

    tipo_var.trace_add("write", lambda *a: on_tipo_change())

    # Cores
    colors_frame = ttk.Frame(left)
    colors_frame.pack(fill="x", pady=6)

    ttk.Label(colors_frame, text="Cor QR (FG):").grid(row=0, column=0, sticky="w")
    fg_entry = ttk.Entry(colors_frame, textvariable=fg_var, width=12)
    fg_entry.grid(row=0, column=1, padx=4)

    def pick_fg():
        c = colorchooser.askcolor(title="Escolher cor do QR", color=fg_var.get())
        if c and c[1]:
            fg_var.set(c[1]); atualizar_preview()
    ttk.Button(colors_frame, text="Selecionar", command=pick_fg).grid(row=0, column=2, padx=6)

    ttk.Label(colors_frame, text="Fundo (BG):").grid(row=1, column=0, sticky="w")
    bg_entry = ttk.Entry(colors_frame, textvariable=bg_var, width=12)
    bg_entry.grid(row=1, column=1, padx=4)

    def pick_bg():
        c = colorchooser.askcolor(title="Escolher cor do fundo", color=bg_var.get())
        if c and c[1]:
            bg_var.set(c[1]); atualizar_preview()
    ttk.Button(colors_frame, text="Selecionar", command=pick_bg).grid(row=1, column=2, padx=6)

    ttk.Button(colors_frame, text="Fundo Transparente", command=lambda: (bg_var.set("transparent"), atualizar_preview())).grid(row=2, column=0, columnspan=3, sticky="we", pady=6)

    # Logo
    def escolher_logo():
        path = filedialog.askopenfilename(filetypes=[("Imagens","*.png;*.jpg;*.jpeg;*.svg")])
        if path:
            state["logo_path"] = path
            messagebox.showinfo("Logo", "Logo selecionado!")
            atualizar_preview()
    ttk.Button(left, text="Selecionar Logo", command=escolher_logo).pack(fill="x", pady=6)

    # Resolução
    ttk.Label(left, text="Resolução para export / preview quality (px):").pack(anchor="w", pady=(8,0))
    res_frame = ttk.Frame(left)
    res_frame.pack(fill="x", pady=4)
    tamanho_entry = ttk.Entry(res_frame, textvariable=tamanho_var, width=14)
    tamanho_entry.grid(row=0, column=0, padx=4)

    def aplicar_preset(v):
        tamanho_var.set(str(v)); atualizar_preview()

    col = 1
    for p in PRESET_OPTIONS:
        ttk.Button(res_frame, text=str(p), command=lambda v=p: aplicar_preset(v)).grid(row=0, column=col, padx=3)
        col += 1

    ttk.Label(left, text=f"(mínimo {MIN_RES}px)").pack(anchor="w", pady=(2,6))

    # Dark mode
    def aplicar_tema():
        style = ttk.Style()
        if state["dark"]:
            root.configure(bg="#222222")
            style.theme_use('default')
            style.configure('.', background='#222222', foreground='#FFFFFF')
            style.configure('TEntry', fieldbackground='#333333', foreground='#FFFFFF')
            style.configure('TLabel', background='#222222', foreground='#FFFFFF')
            style.configure('TButton', background='#333333', foreground='#FFFFFF')
        else:
            root.configure(bg="#FFFFFF")
            style.theme_use('default')
            style.configure('.', background='#FFFFFF', foreground='#000000')
            style.configure('TEntry', fieldbackground='#FFFFFF', foreground='#000000')
            style.configure('TLabel', background='#FFFFFF', foreground='#000000')
            style.configure('TButton', background='#FFFFFF', foreground='#000000')

    def toggle_dark():
        state["dark"] = not state["dark"]
        aplicar_tema()
        atualizar_preview()

    ttk.Button(left, text="Alternar Dark/Light", command=toggle_dark).pack(fill="x", pady=6)

    # ---------- Right (Preview e Salvar) ----------
    ttk.Label(right, text=f"Preview (fixo {PREVIEW_DISPLAY_SIZE}px):").pack()
    preview_frame = ttk.Frame(right, width=PREVIEW_DISPLAY_SIZE, height=PREVIEW_DISPLAY_SIZE)
    preview_frame.pack(pady=8)
    preview_frame.pack_propagate(False)
    preview_label = tk.Label(preview_frame, bd=1, relief="solid")
    preview_label.pack(expand=True, fill="both")

    def salvar_saida():
        if tipo_var.get() == "wifi":
            if seg_var.get() == "nopass":
                dados = f"WIFI:T:nopass;S:{ssid_var.get()};;"
            else:
                dados = f"WIFI:T:{seg_var.get()};S:{ssid_var.get()};P:{senha_var.get()};;"
        else:
            dados = conteudo_var.get()

        if not dados:
            messagebox.showerror("Erro", "Nenhum conteúdo definido.")
            return

        try:
            tamanho_final = int(float(tamanho_var.get()))
        except Exception:
            messagebox.showerror("Erro", "Digite uma resolução válida (número).")
            return
        if tamanho_final < MIN_RES:
            messagebox.showwarning("Aviso", f"A resolução mínima é {MIN_RES}px. Ajustando.")
            tamanho_final = MIN_RES
            tamanho_var.set(str(MIN_RES))

        img_final = gera_qr_image(dados, fg_var.get(), bg_var.get(), tamanho_final, state.get("logo_path"))

        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("JPEG","*.jpg;*.jpeg"),("PDF","*.pdf")])
        if not caminho:
            return
        ext = os.path.splitext(caminho)[1].lower()

        try:
            if ext == ".png":
                img_final.save(caminho)
                messagebox.showinfo("Sucesso", "PNG salvo!")
            elif ext in (".jpg", ".jpeg"):
                if img_final.mode == "RGBA":
                    bg_img = Image.new("RGB", img_final.size, (255,255,255))
                    bg_img.paste(img_final, mask=img_final.split()[3])
                    bg_img.save(caminho, quality=95)
                else:
                    img_final.convert("RGB").save(caminho, quality=95)
                messagebox.showinfo("Sucesso", "JPEG salvo!")
            elif ext == ".pdf":
                img_bytes = io.BytesIO()
                img_final.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                c = pdf_canvas(caminho, pagesize=(tamanho_final + 100, tamanho_final + 100))
                c.drawInlineImage(img_bytes, 50, 50, width=tamanho_final, height=tamanho_final)
                c.save()
                messagebox.showinfo("Sucesso", "PDF salvo!")
            else:
                messagebox.showerror("Erro", "Formato não suportado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    ttk.Button(right, text="Salvar (PNG/JPEG/PDF)", command=salvar_saida).pack(pady=6)

    # Preview
    checker_cache = {}
    def get_checker(size):
        if size in checker_cache:
            return checker_cache[size]
        cb = gera_checkerboard(size)
        checker_cache[size] = cb
        return cb

    def atualizar_preview(*_):
        if tipo_var.get() == "wifi":
            if seg_var.get() == "nopass":
                dados = f"WIFI:T:nopass;S:{ssid_var.get()};;"
            else:
                dados = f"WIFI:T:{seg_var.get()};S:{ssid_var.get()};P:{senha_var.get()};;"
        else:
            dados = conteudo_var.get()

        if not dados:
            preview_label.config(image="", text="(sem conteúdo)")
            preview_label.image = None
            return

        try:
            tamanho_gerado = int(float(tamanho_var.get()))
        except Exception:
            tamanho_gerado = PRESET_OPTIONS[0]
            tamanho_var.set(str(tamanho_gerado))

        if tamanho_gerado < MIN_RES:
            tamanho_gerado = MIN_RES
            tamanho_var.set(str(MIN_RES))

        try:
            high_img = gera_qr_image(dados, fg_var.get(), bg_var.get(), tamanho_gerado, state.get("logo_path"))
        except Exception:
            preview_label.config(text="Erro ao gerar preview")
            preview_label.image = None
            return

        if isinstance(bg_var.get(), str) and bg_var.get().lower() == "transparent":
            checker = get_checker(tamanho_gerado)
            display_high = Image.alpha_composite(checker, high_img)
        else:
            display_high = high_img

        display_preview = display_high.resize((PREVIEW_DISPLAY_SIZE, PREVIEW_DISPLAY_SIZE), Image.LANCZOS)
        tkimg = ImageTk.PhotoImage(display_preview)
        preview_label.config(image=tkimg, text="")
        preview_label.image = tkimg

    conteudo_var.trace_add("write", lambda *a: atualizar_preview())
    fg_var.trace_add("write", lambda *a: atualizar_preview())
    bg_var.trace_add("write", lambda *a: atualizar_preview())
    tamanho_var.trace_add("write", lambda *a: atualizar_preview())
    tipo_var.trace_add("write", lambda *a: atualizar_preview())
    ssid_var.trace_add("write", lambda *a: atualizar_preview())
    senha_var.trace_add("write", lambda *a: atualizar_preview())
    seg_var.trace_add("write", lambda *a: atualizar_preview())

    aplicar_tema()
    on_tipo_change()
    atualizar_preview()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
