import tkinter as tk
import re
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# ========== CONEXÃO COM O BANCO DE DADOS ==========
conn = sqlite3.connect('petcare.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dono TEXT NOT NULL,
                idade INTEGER,
                especie TEXT,
                raca TEXT,
                numero_dono TEXT,
                cpf_dono TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER,
                data TEXT,
                motivo TEXT,
                tratamento TEXT,
                veterinario TEXT,
                carteirinha_vet TEXT,
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
    raca = entry_raca.get()
    numero_dono = entry_numero_dono.get()
    cpf_dono = entry_cpf_dono.get()
    
    if nome and dono:
        c.execute("INSERT INTO pets (nome, dono, idade, especie, raca, numero_dono, cpf_dono ) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (nome, dono, idade, especie, raca, numero_dono, cpf_dono))
        conn.commit()
        messagebox.showinfo("Sucesso", "Pet cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_dono.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_especie.delete(0, tk.END)
        entry_raca.delete(0, tk.END)
        entry_numero_dono.delete(0, tk.END)
        entry_cpf_dono.delete(0, tk.END)
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
    pet_id, nome, dono, idade, especie, raca, numero_dono, cpf_dono = item['values']

    janela_edit_pet = tk.Toplevel()
    janela_edit_pet.title("Editar Pet")

    tk.Label(janela_edit_pet, text="Nome do pet:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="Idade:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="Espécie:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="Raça:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="Nome do Dono:").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="Número do Dono:").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(janela_edit_pet, text="CPF do Dono:").grid(row=6, column=0, padx=5, pady=5)


    entry_nome_edit = tk.Entry(janela_edit_pet)
    entry_nome_edit.grid(row=0, column=1, padx=5, pady=5)
    entry_nome_edit.insert(0, nome)

    entry_idade_edit = tk.Entry(janela_edit_pet)
    entry_idade_edit.grid(row=1, column=1, padx=5, pady=5)
    entry_idade_edit.insert(0, idade)

    entry_especie_edit = tk.Entry(janela_edit_pet)
    entry_especie_edit.grid(row=2, column=1, padx=5, pady=5)
    entry_especie_edit.insert(0, especie)

    entry_raca_edit = tk.Entry(janela_edit_pet)
    entry_raca_edit.grid(row=3, column=1, padx=5, pady=5)
    entry_raca_edit.insert(0, raca)

    entry_dono_edit = tk.Entry(janela_edit_pet)
    entry_dono_edit.grid(row=4, column=1, padx=5, pady=5)
    entry_dono_edit.insert(0, dono)

    entry_numero_dono_edit = tk.Entry(janela_edit_pet)
    entry_numero_dono_edit.grid(row=5, column=1, padx=5, pady=5)
    entry_numero_dono_edit.insert(0, numero_dono)

    entry_cpf_dono_edit = tk.Entry(janela_edit_pet)
    entry_cpf_dono_edit.grid(row=6, column=1, padx=5, pady=5)
    entry_cpf_dono_edit.insert(0, cpf_dono)

    def salvar_pet():
        novo_nome = entry_nome_edit.get()
        novo_dono = entry_dono_edit.get()
        nova_idade = entry_idade_edit.get()
        nova_especie = entry_especie_edit.get()
        nova_raca = entry_raca_edit.get()
        novo_numero_dono = entry_numero_dono_edit.get()
        novo_cpf_dono = entry_cpf_dono_edit.get()

        if novo_nome and novo_dono:
            c.execute("UPDATE pets SET nome=?, dono=?, idade=?, especie=?, raca=?, numero_dono=?, cpf_dono=? WHERE id=?",
                      (novo_nome, novo_dono, nova_idade, nova_especie, nova_raca, novo_numero_dono, novo_cpf_dono, pet_id))
            conn.commit()
            atualizar_lista_pets()
            atualizar_tabela_pets()
            atualizar_tabela_atendimentos()
            messagebox.showinfo("Sucesso", "Pet atualizado com sucesso!")
            janela_edit_pet.destroy()
        else:
            messagebox.showwarning("Atenção", "Nome e dono são obrigatórios.")

    btn_salvar = ttk.Button(janela_edit_pet, text="Salvar Alterações", command=salvar_pet)
    btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)

def excluir_pet():
    selecionado = tabela_pets.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pet para excluir.")
        return

    item = tabela_pets.item(selecionado)
    pet_id = item['values'][0]

    confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este pet? Todos os atendimentos vinculados também serão excluídos.")
    if confirmar:
        c.execute("DELETE FROM atendimentos WHERE pet_id=?", (pet_id,))
        c.execute("DELETE FROM pets WHERE id=?", (pet_id,))
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
    veterinario = entry_veterinario.get()
    carteirinha_vet = entry_carteirinha_vet.get()

    if not data:
        messagebox.showwarning("Atenção", "A data é obrigatória.")
        return

    if not pet_selecionado:
        messagebox.showwarning("Atenção", "Selecione o pet.")
        return
    pet_id = pet_ids[pet_selecionado]
    c.execute("INSERT INTO atendimentos (pet_id, data, motivo, tratamento, veterinario, carteirinha_vet) VALUES (?, ?, ?, ?, ?, ?)",
              (pet_id, data, motivo, tratamento, veterinario, carteirinha_vet))
    conn.commit()
    messagebox.showinfo("Sucesso", "Atendimento cadastrado com sucesso!")

    entry_motivo.delete(0, tk.END)
    entry_tratamento.delete(0, tk.END)
    entry_veterinario.delete(0, tk.END)
    entry_carteirinha_vet.delete(0, tk.END)
    atualizar_tabela_atendimentos()

def editar_atendimento():
    global atendimento_em_edicao
    selecionado = tabela_atendimentos.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um atendimento para editar.")
        return

    item = tabela_atendimentos.item(selecionado)
    atendimento_id, _, data, motivo, tratamento, veterinario, carteirinha_vet = item['values']
    atendimento_em_edicao = atendimento_id

    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Atendimento")

    tk.Label(janela_edicao, text="Data:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(janela_edicao, text="Motivo:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(janela_edicao, text="Tratamento:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(janela_edicao, text="Veterinário Responsável:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(janela_edicao, text="Número da Carteirinha do Responsável:").grid(row=4, column=0, padx=5, pady=5)

    entry_data_edit = tk.Entry(janela_edicao)
    entry_data_edit.grid(row=0, column=1, padx=5, pady=5)
    entry_data_edit.insert(0, data)

    entry_motivo_edit = tk.Entry(janela_edicao)
    entry_motivo_edit.grid(row=1, column=1, padx=5, pady=5)
    entry_motivo_edit.insert(0, motivo)

    entry_tratamento_edit = tk.Entry(janela_edicao)
    entry_tratamento_edit.grid(row=2, column=1, padx=5, pady=5)
    entry_tratamento_edit.insert(0, tratamento)

    entry_veterinario_edit = tk.Entry(janela_edicao)
    entry_veterinario_edit.grid(row=3, column=1, padx=5, pady=5)
    entry_veterinario_edit.insert(0, veterinario)

    entry_carteirinha_vet_edit = tk.Entry(janela_edicao)
    entry_carteirinha_vet_edit.grid(row=4, column=1, padx=5, pady=5)
    entry_carteirinha_vet_edit.insert(0, carteirinha_vet)

    btn_salvar = ttk.Button(
    janela_edicao,
    text="Salvar Alterações",
    command=lambda: salvar_edicao(
        entry_data_edit,
        entry_motivo_edit,
        entry_tratamento_edit,
        entry_veterinario_edit,
        entry_carteirinha_vet_edit,
        janela_edicao
        )
    )
    btn_salvar.grid(row=5, column=0, columnspan=2, pady=10)

def salvar_edicao(data, motivo, tratamento, veterinario, carteirinha_vet, janela):
    global atendimento_em_edicao
    if atendimento_em_edicao:
        c.execute(
            "UPDATE atendimentos SET data=?, motivo=?, tratamento=?, veterinario=?, carteirinha_vet=? WHERE id=?",
            (
                data.get(),
                motivo.get(),
                tratamento.get(),
                veterinario.get(),
                carteirinha_vet.get(),
                atendimento_em_edicao
            )
        )
        conn.commit()
        atendimento_em_edicao = None
        messagebox.showinfo("Sucesso", "Atendimento atualizado com sucesso!")
        atualizar_tabela_atendimentos()
        atualizar_tabela_pets()
        janela.destroy()

def excluir_atendimento():
    selecionado = tabela_atendimentos.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um atendimento para excluir.")
        return

    item = tabela_atendimentos.item(selecionado)
    atendimento_id = item['values'][0]

    confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este atendimento?")
    if confirmar:
        c.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Atendimento excluído.")
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

    c.execute("SELECT id, nome, dono, idade, raca, especie, numero_dono, cpf_dono FROM pets ORDER BY nome")
    for pet in c.fetchall():
        tabela_pets.insert('', 'end', values=pet)

def atualizar_tabela_atendimentos():
    for item in tabela_atendimentos.get_children():
        tabela_atendimentos.delete(item)

    c.execute("""
        SELECT a.id, p.nome, a.data, a.motivo, a.tratamento, a.veterinario, a.carteirinha_vet 
        FROM atendimentos a
        JOIN pets p ON a.pet_id = p.id
        ORDER BY a.data DESC
    """)

    for atendimento in c.fetchall():
        tabela_atendimentos.insert('', 'end', values=atendimento)

def maiuscula(event, entry):
    texto = entry.get()
    if texto:
        entry.delete(0, tk.END)
        entry.insert(0, texto[0].upper() + texto[1:])

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
entry_nome.bind("<KeyRelease>", lambda event: maiuscula(event, entry_nome))

ttk.Label(frame_cadastro, text="Nome do Dono:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_dono = ttk.Entry(frame_cadastro)
entry_dono.grid(row=1, column=1, padx=5, pady=5)
entry_dono.bind("<KeyRelease>", lambda event: maiuscula(event, entry_dono))

def adicionar_ano(entry):
    texto = entry.get()
    if texto.isdigit():  
        entry.delete(0, tk.END)  
        entry.insert(0, texto + " anos")  
    return

ttk.Label(frame_cadastro, text="Idade:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_idade = ttk.Entry(frame_cadastro)
entry_idade.grid(row=2, column=1, padx=5, pady=5)
entry_idade.bind("<KeyRelease>", lambda event: adicionar_ano(entry_idade))

ttk.Label(frame_cadastro, text="Espécie:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_especie = ttk.Entry(frame_cadastro)
entry_especie.grid(row=3, column=1, padx=5, pady=5)
entry_especie.bind("<KeyRelease>", lambda event: maiuscula(event, entry_especie))

ttk.Label(frame_cadastro, text="Raça:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
entry_raca = ttk.Entry(frame_cadastro)
entry_raca.grid(row=4, column=1, padx=5, pady=5)
entry_raca.bind("<KeyRelease>", lambda event: maiuscula(event, entry_raca))

def formatar_numero_dono(event=None):
    numero_dono = numero_dono_var.get()
    numeros = re.sub(r'\D', '', numero_dono)  
    numeros = numeros[:11]  

    formatado = ''
    if len(numeros) >= 1:
        formatado += '(' + numeros[:2]  
    if len(numeros) >= 3:
        formatado += ') ' + numeros[2:7]  
    if len(numeros) >= 8:
        formatado += '-' + numeros[7:11]  

    entry_numero_dono.delete(0, tk.END)  
    entry_numero_dono.insert(0, formatado)  
    entry_numero_dono.icursor(tk.END) 

numero_dono_var = tk.StringVar()
ttk.Label(frame_cadastro, text="Telefone do Dono:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
entry_numero_dono = ttk.Entry(frame_cadastro, textvariable=numero_dono_var)
entry_numero_dono.grid(row=5, column=1, padx=5, pady=5)
entry_numero_dono.bind('<KeyRelease>', formatar_numero_dono)

def formatar_cpf(event=None):
    pos = entry_cpf_dono.index(tk.INSERT)
    cpf = re.sub(r'\D', '', cpf_var.get())

    cpf_formatado = ''
    if len(cpf) > 0:
        cpf_formatado += cpf[:3]
    if len(cpf) >= 4:
        cpf_formatado += '.' + cpf[3:6]
    if len(cpf) >= 7:
        cpf_formatado += '.' + cpf[6:9]
    if len(cpf) >= 10:
        cpf_formatado += '-' + cpf[9:11]

    entry_cpf_dono.delete(0, tk.END)
    entry_cpf_dono.insert(0, cpf_formatado)
    entry_cpf_dono.icursor(tk.END)

cpf_var = tk.StringVar()

ttk.Label(frame_cadastro, text="CPF do Dono:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
entry_cpf_dono = ttk.Entry(frame_cadastro, textvariable=cpf_var)
entry_cpf_dono.grid(row=6, column=1, padx=5, pady=5)
entry_cpf_dono.bind('<KeyRelease>', formatar_cpf)

btn_cadastrar = ttk.Button(frame_cadastro, text="Cadastrar Pet", command=cadastrar_pet)
btn_cadastrar.grid(row=7, column=0, columnspan=2, pady=10)

entry_nome.delete(0, tk.END)
entry_dono.delete(0, tk.END)
entry_idade.delete(0, tk.END)
entry_especie.delete(0, tk.END)
entry_raca.delete(0, tk.END)
entry_numero_dono.delete(0, tk.END)
entry_cpf_dono.delete(0, tk.END)

# Campo de busca
frame_busca = ttk.LabelFrame(aba_pets, text="Buscar Pet", padding=10)
frame_busca.pack(fill='x', padx=10, pady=5)

entry_busca = ttk.Entry(frame_busca)
entry_busca.pack(side='left', fill='x', expand=True, padx=5)

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
btn_limpar.pack(side='left', padx=5)


# Lista de pets cadastrados
frame_tabela_pets = ttk.LabelFrame(aba_pets, text="Pets Cadastrados", padding=10)
frame_tabela_pets.pack(fill='both', expand=True, padx=10, pady=5)

colunas_pets = ('ID', 'Nome', 'Dono', 'Idade', 'Espécie', 'Raça', 'Número do Dono', 'CPF do Dono')
tabela_pets = ttk.Treeview(frame_tabela_pets, columns=colunas_pets, show='headings')
for col in colunas_pets:
    tabela_pets.heading(col, text=col)
    tabela_pets.column(col, minwidth=0, width=100)

tabela_pets.pack(fill='both', expand=True)

frame_botoes_pets = ttk.Frame(aba_pets)
frame_botoes_pets.pack(pady=10)

btn_editar_pet = ttk.Button(frame_botoes_pets, text="Editar Pet Selecionado", command=lambda: editar_pet())
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
entry_data.grid(row=1, column=1, padx=5, pady=5)
entry_data.insert(0, date.today().strftime("%d/%m/%Y"))

ttk.Label(frame_atendimento, text="Motivo:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_motivo = ttk.Entry(frame_atendimento)
entry_motivo.grid(row=2, column=1, padx=5, pady=5)
entry_motivo.bind("<KeyRelease>", lambda event: maiuscula(event, entry_motivo))

ttk.Label(frame_atendimento, text="Tratamento:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_tratamento = ttk.Entry(frame_atendimento)
entry_tratamento.grid(row=3, column=1, padx=5, pady=5)
entry_tratamento.bind("<KeyRelease>", lambda event: maiuscula(event, entry_tratamento))

ttk.Label(frame_atendimento, text="Veterinário Responsável:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
entry_veterinario = ttk.Entry(frame_atendimento)
entry_veterinario.grid(row=4, column=1, padx=5, pady=5)
entry_veterinario.bind("<KeyRelease>", lambda event: maiuscula(event, entry_veterinario))

def formatar_carteirinha(event=None):
    carteirinha = carteirinha_var.get()
    numeros = re.sub(r'\D', '', carteirinha)
    numeros = numeros[:11]

    formatado = ''
    if len(numeros) > 0:
        formatado += numeros[:6]
    if len(numeros) >= 7:
        formatado += '.' + numeros[6:9]
    if len(numeros) >= 10:
        formatado += '-' + numeros[9:11]

    pos = entry_carteirinha_vet.index(tk.INSERT)
    entry_carteirinha_vet.delete(0, tk.END)
    entry_carteirinha_vet.insert(0, formatado)
    entry_carteirinha_vet.icursor(tk.END)

carteirinha_var = tk.StringVar()

ttk.Label(frame_atendimento, text="Carteirinha do Responsável:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
entry_carteirinha_vet = ttk.Entry(frame_atendimento, textvariable=carteirinha_var)
entry_carteirinha_vet.grid(row=5, column=1, padx=5, pady=5)
entry_carteirinha_vet.bind('<KeyRelease>', formatar_carteirinha)

btn_atendimento = ttk.Button(frame_atendimento, text="Cadastrar Atendimento", command=cadastrar_atendimento)
btn_atendimento.grid(row=6, column=0, columnspan=2, pady=10)

# ========== ABA DE VISUALIZAÇÃO ==========
aba_visualizar = ttk.Frame(aba_control)
aba_control.add(aba_visualizar, text='Visualizar Atendimentos')

frame_tabela_atend = ttk.LabelFrame(aba_visualizar, text="Histórico de Atendimentos", padding=10)
frame_tabela_atend.pack(fill='both', expand=True, padx=10, pady=10)

colunas = ('ID', 'Pet', 'Data', 'Motivo', 'Tratamento', 'Veterinário', 'Carteirinha Vet')
tabela_atendimentos = ttk.Treeview(frame_tabela_atend, columns=colunas, show='headings')
for col in colunas:
    tabela_atendimentos.heading(col, text=col)
    tabela_atendimentos.column(col, minwidth=0, width=100)

tabela_atendimentos.pack(expand=True, fill='both')

frame_botoes_atend = ttk.Frame(aba_visualizar)
frame_botoes_atend.pack(pady=10)

btn_editar = ttk.Button(frame_botoes_atend, text="Editar Atendimento Selecionado", command=editar_atendimento)
btn_editar.pack(side='left', padx=5)

btn_excluir = ttk.Button(frame_botoes_atend, text="Excluir Atendimento Selecionado", command=excluir_atendimento)
btn_excluir.pack(side='left', padx=5)

# ========== PARTE FINAL DO PROJETO ==========
atualizar_lista_pets()
atualizar_tabela_pets()
atualizar_tabela_atendimentos()
root.mainloop()
conn.close()
