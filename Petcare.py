import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datatime import date

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

# ==================== FUNÇÕES DE PETS ====================
def cadastrar_pet():
  nome = entry_nome.get()
  dono = entry_dono.get()
  idade = entry_idade.get()
  especie = entry_especie.get()

  if nome and dono:
    c.execute("INSERT INTO pets (nome, dono, idade, especie) VALUES (?, ?, ?, ?)", (nome, dono, idade, especie))
    conn.commit()
    messagebox.showinfo("Sucesso", "Pet cadastrado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_dono.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_especie.delete(0, tk.END)
    atualizar_lista_pets()
    atualizar_tabela_pets()
    atualizar_tabela_atendimentos()
  else:
    messagebox.showwarning("Atenção", "Nome e dono são obrigatórios.")

def editar_pet():
  selecionado = tabela_pets.selection()
  if not selecionado:
    messagebox.showwarning("Atenção", "Selecione um pet para editar.")
    return

  item = tabela_pets.item(selecionado)
  pet_id, nome, dono, idade, especie = item['values']

  janela_edit_pet = tk.Toplevel()
  janela_edit_pet.title("Editar Pet")

  tk.Label(janela_edit_pet, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
  tk.Label(janela_edit_pet, text="Dono:").grid(row=1, column=0, padx=5, pady=5)
  tk.Label(janela_edit_pet, text="Idade:").grid(row=2, column=0, padx=5, pady=5)
  tk.Label(janela_edit_pet, text="Espécie:").grid(row=3, column=0, padx=5, pady=5)]

  entry_nome_edit = tk.Entry(janela_edit_pet)
  entry_nome_edit.grid(row=0, column=1, padx=5, pady=5)
  entry_nome_edit.insert(0, nome)

  entry_dono_edit = tk.Entry(janela_edit_pet)
  entry_dono_edit.grid(row=1, column=1, padx=5, pady=5)
  entry_dono_edit.insert(0, nome)

  entry_idade_edit = tk.Entry(janela_edit_pet)
  entry_idade_edit.grid(row=2, column=1, padx=5, pady=5)
  entry_idade_edit.insert(0, nome)

  entry_especie_edit = tk.Entry(janela_edit_pet)
  entry_especie_edit.grid(row=3, column=1, padx=5, pady=5)
  entry_especie_edit.insert(0, nome)]

  def salvar_pet():
    novo_nome = entry_nome_edit.get()
    novo_dono = entry_dono_edit.get()
    nova_idade = entry_idade_edit.get()
    nova_especie = entry_especie_edit.get()

    if novo_nome and novo_dono:
      c.execute("UPDATE pets SET nome=?, dono=?, idade=?, especie=? WHERE id=?", (novo_nome, novo_dono, nova_idade, nova_especie, pet_id))
      conn.commit()
      atualizar_lista_pets()
      atualizar_tabela_pets()
      messagebox.showinfo("Sucesso", "Pet atualizado com seucesso!")
      janela_edit_pet.destroy()
    else:
      messagebox.showwarning("Atenção", "Nome e dono são obrigatórios.")

  btn_salvar = ttk.Button(janela_edit_pet, text="Salvar Alterações", command=salvar_pet)
  btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

def excluir_pet():
  selecionado = tabela_pets.selection()
  if not selecionado:
    messagebox.showwarning("Atenção", "Selecione um pet para excluir.")
    return
  item = tabela_pets.item(selecionado)
  pet_id = item['values'] [0]

  confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir esse pet? Todos os atendimentos vinculados também serão excluídos.")
  if confirmar:
    c.execute("DELETE FROM atendimentos WHERE pet_id=?", (pet_id))
    c.execute("DELETE FROM pets WHERE id=?", (pet_id))
    conn.commit()
    atualizar_lista_pets()
    atualizar_tabela_pets()
    atualizar_tabela_atendimentos()
    messagebox.showinfo("Sucesso", "Pet e atendimentos excluídos com sucesso.")

# ==================== FUNÇÕES DE ATENDIMENTO ====================
def cadastrar_atendimento():
  pet_selecionado = combo_pet.get()
  data = entry_data.get()
  motivo = entry_motivo.get()
  tratamento = entry_tratamento.get()

  if not data:
    messagebox.showwarning("Atenção", "A data é obrigatória.")
    return

  if not pet_selecionado:
    messagebox.showwarning("Atenção", "Selecione o pet.")
    return
  pet_id = pet_ids[pet_selecionado]
  c.execute ("INSERT INTO atendimentos (pet_id, data, motivo, tratamento) VALUES (?, ?, ?, ?)", (pet_id, data, motivo, tratamento))
  conn.commit()
  messagebox.showinfo("Sucesso", "Atendimento cadastrado com seucesso!")

  entry_data.delete(0, tk.END)
  entry_motivo.delete(0, tk.END)
  entry_tratamento.delete(0, tk.END)  
  atualizar_tabela_atendimento()

def editar_atendimento():
  global atendimento_em_edicao
  selecionado = tabela_atendimentos.selection()
  if not selecionado:
    messagebox.showwarning("Atenção", "Selecione um atendimento para editar.")
    return

  item = tabela_atendimentos.item(selecionado)
  atendimento_id, _, data, motivo, tratamento = item['values']
  atendimento_em_edicao = atendimento_id

  janela_edicao = tk.TopLevel()
  janela_edicao.title("Editar Atendimento")

  tk.Label(janela_edicao, text="Data:").grid(row=0, column=0, padx=5, pady=5)
  tk.Label(janela_edicao, text="Motivo:").grid(row=1, column=0, padx=5, pady=5)
  tk.Label(janela_edicao, text="Tratamento:").grid(row=2, column=0, padx=5, pady=5)

  entry_data_edit = tk.Entry(janela_edicao)
  entry_data_edit.grid(row=0, column=1, padx=5, pady=5)
  entry_data_edit.insert(0, data)

  entry_motivo_edit = tk.Entry(janela_edicao)
  entry_motivo_edit.grid(row=1, column=1, padx=5, pady=5)
  entry_motivo_edit.insert(0, motivo)

  entry_tratamento_edit = tk.Entry(janela_edicao)
  entry_tratamento_edit.grid(row=2, column=1, padx=5, pady=5)
  entry_tratamento_edit.insert(0, tratamento)

  btn_salvar = ttk.Button(janela_edicao, text="Salvar Alterações", command=lambda: salvar_edicao(entry_data_edit, entry_motivo_edit, entry_tratamento_edit, janela_edicao))
  btn_salvar.grid(row=3, column=0, columnspan=2, pady=10)

def salvar_edicao(data, motivo, tratamento, janela):
  global atendimento_em_edicao
  c.execute("UPDATE atendimentos SET data=?, motivo=?, tratamento=? WHERE id=?", (data.get(), motivo.get(), tratamento.get(), atendimento_em_edicao))
  conn.commit()
  atendimento_em_edicao = None
  messagebox.showinfo("Sucesso", "Atendimento atualizado com sucesso!")
  atualizar_tabela_atendimentos()
  janela.destroy()

def excluir_atendimento():
  selecionado = tabela_atendimentos.selection()
  if not seleconado:
    messagebox.showwarning("Atenção", "Selecione um atendimento para excluir.")
    return
    
  item = tabela_atendimentos.item(selecionado)
  atendimento_id = item['values'][0]

confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este atendimento?")
if confirmar:
  c.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
  conn.commit()
  messagebox.showinfo("Sucesso", "Atendimento excluído")
  atualizar_tabela_atendimentos()

# ==================== FUNÇÕES DE ATUALIZAÇÃO ====================
def atualizar_lista_pets():
  global pet_ids
  combo_pet['values'] = []
  pet_ids = {}
  c.execute("SELECT id, nome FROM pets")
  for pid, nome in c.fetchall():
    label = f"{nome} (ID {pid})"
    pet_ids[label] = pid
  combo_pet['values'] = list(pet_ids.keys())

def atualizar_tabela_pets():
  for item in tabela_pets.get_children():
    tabela_pets.delete(item)

  c.execute("SELECT id, nome, dono, idade, especie FROM pets ORDER BY nome")
  for pet in c.fetchall():
    tabela_pets.insert('', 'end', values=pet)

def atualizar_tabela_atendimentos():
  for item in tabela_atendimentos.get_children():
    tabela_atendimentos.delete(item)
  c.execute("""SELECT a.id, p.nome, a.data, a.motivo, a.tratamento
  FROM atendimentos a 
  JOIN pets p ON a.pet_id = p.id
  ORDER BY a.data DESC 
  """)

  for atendimento in c.fetchall():
    tabela_atendimentos.insert('', 'end', values=atendimento)

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

# CAMPO DE BUSCA 
frame_busca = ttk.LabelFrame(aba_pets, text="Buscar Pet", padding=10)
frame_busca.pack(fill='x', padx=10, pady 5)

entry_busca = ttk.Entry(frame_busca)
entry_busca.pack(side='left', fill='x', expand= True, padx=5)

def buscar_pets():
  global c
  termo = entry_busca.get().strip()
  for item in tabela_pets.get_children():
    tabela_pets.delete(item)
  if termo:
    c.execute("SELECT * FROM pets WHERE nome LIKE ? OR dono LIKE ?", (f'%{termo}%', f'%{termo}%'))
  else:
    c.execute("SELECT * FROM pets")
  for row in c.fetchall():
    tabela_pets.insert('', 'end', values=row)

def limpar_busca():
  entry_busca.delete(0, tk.END)
  buscar_pets()

btn_buscar = ttk.Button(frame_busca, text="Buscar", command=buscar_pets)
btn_buscar.pack(side='left', padx=5)

btn_limpar = ttk.Button(frame_busca, text="Limpar Busca", command=limpar_busca)
btn_limapar.pack(side='left', padx=5)

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

# ========== ABA DE ATENDIMENTOS ==========
aba_atendimentos = ttk.Frame(aba_control)
aba_control.add(aba_atendimentos, text='Cadastro de Atendimentos')

frame_atendimento = ttk.LabelFrame(aba_atendimentos, text="Novo Atendimento", padding=10)
frame_atendimento.pack(fill='x', padx=10, pady=10)

ttk.Label(frame_atendimento, text="Pet:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
combo_pet = ttk.Combobox(frame_atendimento, state='readonly')
combo_pet.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_atendimento, text="Data:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_data = ttk.Entry(frame_atendimento)
entry_data.insert(0, date_today().strftime("%d/%m/%Y"))
entry_data.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_atendimento, text="Motivo:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_motivo = ttk.Entry(frame_atendimento)
entry_motivo.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_atendimento, text="Tratamento:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_tratamento = ttk.Entry(frame_atendimento)
entry_tratamento.grid(row=3, column=1, padx=5, pady=5)

btn_atendimento = ttk.Button(frame_atendimento, text="Cadastrar Atendimento", command=cadastrar_atendimento)
btn_atendimento.grid(row=4, column=0, columnspan=2, pady=10)

# ========== ABA DE VISUALIZAÇÃO ==========
aba_visualizar = ttk.Frame(aba_control)
aba_control.add(aba_visualizar, text='Visualizar Atendimentos')

frame_tabela_atend = ttk.LabelFrame (aba_visualizar, text="Histórico de Atendimentos", padding=10)
frame_tabela_atend.pack(fill='both', expand=True, padx=10, pady=10)

colunas = ('ID', 'Pet', 'Data', 'Motivo', 'Tratamento')
tabela_atendimentos = ttk.Treeview(frame_tabela_atend, columns=colunas, show='headings')
for col in colunas:
  tabela_atendimentos.heading(col, text=col)
  tabela_atendimentos.column(col,minwidth=0, width=100)

tabela_atendimentos.pack(expand=True, fill='both')

frame_botoes_atend = ttk.Frame(aba_visualizar)
frame_botoes_atend.pack(pady=10)

btn_editar = ttk.Button(frame_botoes_atend, text="Editar Atendimento Selecionado", command=editar_atendimento)
btn_editar.pack(side='left', padx=5)

btn_excluir = ttk.Button(frame_botoes_atend, text="Excluir Atendimento Selecionado", command=excluir_atendimento)
btn_excluir.pack(side='left', padx=5)
