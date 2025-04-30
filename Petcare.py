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

# LISTA DE PETS CADASTRADOS 
frame_tabela_pets = ttk.LabelFrame(aba_pets, text="Pets Cadastrados", padding=10
frame_tabela_pets.pack(fill='both', expand=True, padx=10, pady=5)

colunas_pets = ('ID', 'Nome', 'Dono', 'Idade', 'Espécie')
tabela_pets = ttk.Treeview(frame_tabela_pets, columns=colunas_pets, show='headings')
for col in colunas_pets:
  tabela_pets.heading(col, text=col)
  tabela_pets.column(col, minwidth=0, width=100)

tabela_pets.pack(fill='both', expand=True)

frame_botoes_pets= ttk.Frame(aba_pets)
frame_botoes_pets.pack(pady=10)

btn_editar_pet= ttk.Button(frame_botoes_pets, text="Editar Pet Selecionado", command=lambda: editar_pet())
btn_editar_pet.pack(side='left', padx=5)

btn_excluir_pet = ttk.Button(frame_botoes_pets, text="Excluir Pet Selecionado", command=lambda: excluir_pet())
btn_excluir_pet.pack(side='left', padx=5)
