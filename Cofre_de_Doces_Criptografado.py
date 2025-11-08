from pymongo import MongoClient
from cryptography.fernet import Fernet
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import random

# === CONFIGURAÇÕES ===

# 🔐 Carregar chave fixa (cria se não existir)
try:
    with open("fernet.key", "rb") as f:
        FERNET_KEY = f.read()
except FileNotFoundError:
    FERNET_KEY = Fernet.generate_key()
    with open("fernet.key", "wb") as f:
        f.write(FERNET_KEY)

fernet = Fernet(FERNET_KEY)

# 🔌 Conexão com MongoDB (substitua pelas suas credenciais se necessário)
client = MongoClient(
    "mongodb+srv://root:123@cluster0.gehegrd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.halloween
collection = db.candies


# === EFEITOS ESPECIAIS DE HALLOWEEN ===
def criar_fantasminhas(canvas):
    """Cria fantasminhas animados no fundo"""
    colors = ["#8B008B", "#4B0082", "#FF4500", "#32CD32"]
    for _ in range(8):
        x = random.randint(50, 550)
        y = random.randint(50, 450)
        size = random.randint(20, 40)
        color = random.choice(colors)

        # Corpo do fantasminha
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline="white", width=2)
        # Pontas embaixo
        for i in range(3):
            canvas.create_arc(x + (i * size / 3), y + size / 2,
                              x + ((i + 1) * size / 3), y + size,
                              start=0, extent=180, fill=color, outline="white", width=1)
        # Olhos
        eye_size = size // 8
        canvas.create_oval(x + size // 4 - eye_size, y + size // 3,
                           x + size // 4 + eye_size, y + size // 3 + eye_size * 2,
                           fill="white")
        canvas.create_oval(x + 3 * size // 4 - eye_size, y + size // 3,
                           x + 3 * size // 4 + eye_size, y + size // 3 + eye_size * 2,
                           fill="white")


def piscar_luzes():
    """Faz as cores piscarem suavemente"""
    colors = ["#FF6B00", "#FF4500", "#FF8C00", "#FFA500"]
    current_color = random.choice(colors)
    titulo.config(fg=current_color)
    root.after(1000, piscar_luzes)


# === FUNÇÕES ===

def adicionar_doce_gui():
    nome = entry_nome.get().strip()
    tipo = entry_tipo.get().strip()
    qtd_texto = entry_qtd.get().strip()

    if not nome or not tipo or not qtd_texto:
        messagebox.showwarning("⚠ Dados inválidos", "Preencha todos os campos corretamente.")
        return

    try:
        qtd = int(qtd_texto)
    except ValueError:
        messagebox.showwarning("⚠ Dados inválidos", "A quantidade deve ser um número inteiro.")
        return

    encrypted = fernet.encrypt(tipo.encode()).decode()
    doce = {
        "child": nome,
        "candy_type": encrypted,
        "qty": qtd,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    collection.insert_one(doce)
    messagebox.showinfo("✅ Sucesso", "Doce adicionado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)


def listar_doces_gui():
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "🎃📦 Doces armazenados (criptografados):\n\n", "titulo")
    for doc in collection.find():
        result_text.insert(tk.END, f"👻 {doc['child']} - 🍬 {doc['candy_type']} - Quantidade: {doc['qty']}\n", "dado")


def descriptografar_doces_gui():
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "🔓🍭 Doces descriptografados:\n\n", "titulo")
    for doc in collection.find():
        try:
            decrypted = fernet.decrypt(doc["candy_type"].encode()).decode()
            data = datetime.fromisoformat(doc["timestamp"].replace("Z", "")).strftime("%d/%m/%Y %H:%M:%S")
            result_text.insert(tk.END, f"🧙 {doc['child']} pegou {doc['qty']}x 🍬 {decrypted} em {data}\n", "dado")
        except Exception as e:
            result_text.insert(tk.END, f"💀 Erro ao descriptografar: {e}\n", "erro")


def fechar_app():
    client.close()
    root.destroy()


# === INTERFACE TKINTER COM TEMA HALLOWEEN ===

root = tk.Tk()
root.title("🧛‍♂️ Cofre Mágico de Doces - Halloween 🎃")
root.geometry("700x600")
root.configure(bg="#1a0f29")

# Canvas para efeitos de fundo
canvas = tk.Canvas(root, width=700, height=600, bg="#1a0f29", highlightthickness=0)
canvas.pack()

# Gradiente de fundo (simulado)
for i in range(600):
    r = int(26 + (i / 600) * 30)
    g = int(15 + (i / 600) * 10)
    b = int(41 + (i / 600) * 20)
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 700, i, fill=color)

# Adicionar fantasminhas
criar_fantasminhas(canvas)

# Título principal com estilo assustador
titulo = tk.Label(root, text="🧛‍♂️ COFRE MÁGICO DE DOCES 🎃",
                  font=("Chiller", 24, "bold"),
                  bg="#1a0f29", fg="#FF6B00")
titulo.place(relx=0.5, rely=0.05, anchor="center")

# Subtítulo
subtitulo = tk.Label(root, text="Sistema Criptografado de Guloseimas",
                     font=("Chiller", 16),
                     bg="#1a0f29", fg="#9370DB")
subtitulo.place(relx=0.5, rely=0.1, anchor="center")

# Frame de Entrada com tema de castelo
frame_entrada = tk.Frame(root, bg="#2d1b3d", bd=3, relief="ridge",
                         highlightbackground="#FF4500", highlightthickness=2)
frame_entrada.place(relx=0.5, rely=0.25, anchor="center", width=500, height=120)

# Labels com tema Halloween
tk.Label(frame_entrada, text="👻 Nome da criança:",
         font=("Arial", 10, "bold"),
         bg="#2d1b3d", fg="#FFA500").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome = tk.Entry(frame_entrada, font=("Arial", 10),
                      bg="#4a2c5d", fg="white", insertbackground="white")
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="🍬 Tipo de doce:",
         font=("Arial", 10, "bold"),
         bg="#2d1b3d", fg="#FFA500").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_tipo = tk.Entry(frame_entrada, font=("Arial", 10),
                      bg="#4a2c5d", fg="white", insertbackground="white")
entry_tipo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="🔢 Quantidade:",
         font=("Arial", 10, "bold"),
         bg="#2d1b3d", fg="#FFA500").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_qtd = tk.Entry(frame_entrada, font=("Arial", 10),
                     bg="#4a2c5d", fg="white", insertbackground="white")
entry_qtd.grid(row=2, column=1, padx=5, pady=5)

# Frame dos Botões com tema de abóbora
frame_botoes = tk.Frame(root, bg="#1a0f29")
frame_botoes.place(relx=0.5, rely=0.4, anchor="center")

# Botões estilizados com cores de Halloween
btn_style = {"font": ("Arial", 10, "bold"), "width": 15, "height": 2, "bd": 3}

btn_add = tk.Button(frame_botoes, text="➕ ADICIONAR DOCE",
                    bg="#FF4500", fg="black", activebackground="#FF8C00",
                    command=adicionar_doce_gui, **btn_style)
btn_add.grid(row=0, column=0, padx=8, pady=5)

btn_listar = tk.Button(frame_botoes, text="📦 LISTAR DOCES",
                       bg="#8B008B", fg="white", activebackground="#9370DB",
                       command=listar_doces_gui, **btn_style)
btn_listar.grid(row=0, column=1, padx=8, pady=5)

btn_decrypt = tk.Button(frame_botoes, text="🔓 DESCRIPTOGRAFAR",
                        bg="#228B22", fg="white", activebackground="#32CD32",
                        command=descriptografar_doces_gui, **btn_style)
btn_decrypt.grid(row=0, column=2, padx=8, pady=5)

# Área de Resultado com tema de pergaminho antigo
frame_resultado = tk.Frame(root, bg="#1a0f29")
frame_resultado.place(relx=0.5, rely=0.75, anchor="center", width=650, height=250)

result_text = tk.Text(frame_resultado, height=12, width=78,
                      bg="#f5e6ca", fg="#2d1b3d",
                      font=("Courier", 9),
                      relief="sunken", bd=3,
                      wrap=tk.WORD)

# Configurar tags para formatação de texto
result_text.tag_configure("titulo", foreground="#8B0000", font=("Courier", 10, "bold"))
result_text.tag_configure("dado", foreground="#2d1b3d", font=("Courier", 9))
result_text.tag_configure("erro", foreground="#FF0000", font=("Courier", 9, "bold"))

scrollbar = tk.Scrollbar(frame_resultado, orient="vertical", command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)

result_text.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Rodapé temático
footer_text = "⚠️ Cuidado com os fantasmas... Eles adoram doces! 🍭👻"
footer = tk.Label(root, text=footer_text,
                  font=("Chiller", 12),
                  bg="#1a0f29", fg="#9370DB")
footer.place(relx=0.5, rely=0.95, anchor="center")

# Iniciar efeitos especiais
root.after(1000, piscar_luzes)

# Fechar corretamente
root.protocol("WM_DELETE_WINDOW", fechar_app)

# Iniciar interface
root.mainloop()