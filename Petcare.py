import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ========== CONEXÃO COM O BANCO DE DADOS ==========
conn = sqlite3.connect('petcare.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dono TEXT NOT NULL,
                idade INTEGER,
                especie TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER,
                data TEXT,
                motivo TEXT,
                tratamento TEXT,
                FOREIGN KEY (pet_id) REFERENCES pets(id)
            )''')
conn.commit()

# ========== VARIÁVEIS GLOBAIS ==========
atendimento_em_edicao = None

# ========== INICIALIZAÇÃO DO TKINTER ==========
root = tk.Tk()
root.title("PetCare - Sistema de Gerenciamento de Pets")

aba_control = ttk.Notebook(root)
aba_control.pack(expand=1, fill='both', padx=10, pady=10)

# ========== ABA DE PETS ==========
aba_pets = ttk.Frame(aba_control)
aba_control.add(aba_pets, text='Cadastro de Pets')

frame_cadastro = ttk.LabelFrame(aba_pets, text="Cadastro do Pet", padding=10)
frame_cadastro.pack(fill='x', padx=10, pady=10)

ttk.Label(frame_cadastro, text="Nome do Pet:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_nome = ttk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_cadastro, text="Nome do Dono:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_dono = ttk.Entry(frame_cadastro)
entry_dono.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_cadastro, text="Idade:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_idade = ttk.Entry(frame_cadastro)
entry_idade.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_cadastro, text="Espécie:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_especie = ttk.Entry(frame_cadastro)
entry_especie.grid(row=3, column=1, padx=5, pady=5)

btn_cadastrar = ttk.Button(frame_cadastro, text="Cadastrar Pet", command=cadastrar_pet)
btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10)
