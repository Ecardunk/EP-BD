import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


conn = sqlite3.connect('consultas.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Medico (
    CRM TEXT PRIMARY KEY,
    NomeM TEXT,
    TelefoneM TEXT,
    Percentual REAL
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Consulta (
        idCon INTEGER PRIMARY KEY AUTOINCREMENT,
        CRM TEXT NOT NULL,
        IdEsp INTEGER NOT NULL,
        IdPac INTEGER NOT NULL,
        Data DATE NOT NULL,
        HoraInicCon TIME NOT NULL,
        HoraFimCon TIME NOT NULL,
        Pagou BOOLEAN,
        ValorPago REAL,
        FormaPagamento TEXT,
        FOREIGN KEY (CRM) REFERENCES Medico(CRM),
        UNIQUE (CRM, Data, HoraInicCon, HoraFimCon)
    )
''')

cursor.executescript("""
-- Populando com os Médicos
INSERT INTO Medico (CRM, NomeM, TelefoneM, Percentual) VALUES
('12345', 'Dr. House', '555-1234', 20.0),
('13123', 'Dr. Atende Tudo Da Silva', '24999-012', 5.0),
('13694', 'Dr. Dermatologista Pereira', '268-128416', 15.0),
('67890', 'Dr. Kildare', '555-5678', 15.0);
""")


# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()

def conectar():
    return sqlite3.connect('consultas.db')

def crm_existe(CRM):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM Medico WHERE CRM = ?', (CRM,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe


def adicionar_consulta(CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento):
    if not crm_existe(CRM):
        messagebox.showwarning("Erro", "CRM não encontrado na relação de médicos")
        return
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO Consulta (CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento))
        conn.commit()
        messagebox.showinfo("Sucesso", "Consulta adicionada com sucesso")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Erro", "Já existe uma consulta marcada com este médico no mesmo horário")
    finally:
        conn.close()

def listar_consultas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM consulta')
    consultas = cursor.fetchall()
    conn.close()
    return consultas

def atualizar_consulta(idCon, CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento):

    if not crm_existe(CRM):
        messagebox.showwarning("Erro", "CRM não encontrado na tabela de médicos")
        return

    conn = conectar()
    cursor = conn.cursor()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE consulta
    SET CRM = ?, IdEsp = ?, IdPac = ?, Data = ?, HoraInicCon = ?, HoraFimCon = ?, Pagou = ?, ValorPago = ?, FormaPagamento = ?
    WHERE idCon = ?
    ''', (CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento, idCon))
    conn.commit()
    conn.close()

def excluir_consulta(idCon):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Consulta WHERE idCon = ?', (idCon,))
    conn.commit()
    conn.close()

def pesquisar_consultas_por_medico(CRM):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Consulta WHERE CRM = ?', (CRM,))
    consultas = cursor.fetchall()
    conn.close()
    return consultas


# Funções da Interface Gráfica
def adicionar():
    CRM = CRM_entry.get()
    IdEsp = IdEsp_entry.get()
    IdPac = IdPac_entry.get()
    Data = Data_entry.get()
    HoraInicCon = HoraInicCon_entry.get()
    HoraFimCon = HoraFimCon_entry.get()
    Pagou = Pagou_entry.get()
    ValorPago =  ValorPago_entry.get()
    FormaPagamento = FormaPagamento_entry.get()
   

    if CRM and IdEsp and IdPac and Data and HoraInicCon and HoraFimCon and Pagou and ValorPago and FormaPagamento:
        adicionar_consulta(CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento)
        listar()
        #messagebox.showinfo("Sucesso", "Consulta adicionada com sucesso")
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos obrigatórios")

def listar():
    consultas = listar_consultas()
    lista_consultas.delete(0, tk.END)
    for consulta in consultas:
        lista_consultas.insert(tk.END, consulta)

def atualizar():
    try:
        idCon = int(simpledialog.askstring("Atualizar", "ID da consulta a ser atualizada:"))
        CRM = simpledialog.askstring("Atualizar", "CRM/Médico:")
        IdEsp = simpledialog.askstring("Atualizar", "Especialidade:")
        IdPac = simpledialog.askstring("Atualizar", "Paciente:")
        Data = simpledialog.askstring("Atualizar", "Data (AAAA-MM-DD):")
        HoraInicCon = simpledialog.askstring("Atualizar", "Início da consulta (HH:MM):")
        HoraFimCon = simpledialog.askstring("Atualizar", "Data da Consulta (AAAA-MM-DD):")
        Pagou = simpledialog.askstring("Atualizar", "Pagou? (Sim/Não)")
        ValorPago = simpledialog.askstring("Atualizar", "Valor pago:")
        FormaPagamento = simpledialog.askstring("Atualizar", "Forma de pagamento:")

        if idCon and CRM and IdEsp and IdPac and Data and HoraInicCon and HoraFimCon and Pagou and ValorPago and FormaPagamento:
            atualizar_consulta(idCon, CRM, IdEsp, IdPac, Data, HoraInicCon, HoraFimCon, Pagou, ValorPago, FormaPagamento)
            listar()
            messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso")
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos obrigatórios")
    except ValueError:
        messagebox.showwarning("Erro", "ID inválido")

def excluir():
    try:
        idCon = int(simpledialog.askstring("Excluir", "ID da consulta a ser excluída:"))
        excluir_consulta(idCon)
        listar()
        messagebox.showinfo("Sucesso", "Consulta excluída com sucesso")
    except ValueError:
        messagebox.showwarning("Erro", "ID inválido")

def pesquisar():
    CRM = simpledialog.askstring("Pesquisar", "CRM do médico:")
    if CRM:
        consultas = pesquisar_consultas_por_medico(CRM)
        lista_consultas.delete(0, tk.END)
        for consulta in consultas:
            lista_consultas.insert(tk.END, consulta)
    else:
        messagebox.showwarning("Erro", "Por favor, insira o CRM do médico")
# Interface Gráfica
root = tk.Tk()
root.title("Gerenciador de Consultas")

tk.Label(root, text="CRM/Médico:").grid(row=0, column=0)
CRM_entry = tk.Entry(root)
CRM_entry.grid(row=0, column=1)

tk.Label(root, text="Especialidade:").grid(row=1, column=0)
IdEsp_entry = tk.Entry(root)
IdEsp_entry.grid(row=1, column=1)

tk.Label(root, text="Paciente:").grid(row=2, column=0)
IdPac_entry = tk.Entry(root)
IdPac_entry.grid(row=2, column=1)

tk.Label(root, text="Data (AAAA-MM-DD):").grid(row=3, column=0)
Data_entry = tk.Entry(root)
Data_entry.grid(row=3, column=1)

tk.Label(root, text="Início da consulta (HH:MM):").grid(row=4, column=0)
HoraInicCon_entry = tk.Entry(root)
HoraInicCon_entry.grid(row=4, column=1)

tk.Label(root, text="Fim da consulta (HH:MM):").grid(row=5, column=0)
HoraFimCon_entry = tk.Entry(root)
HoraFimCon_entry.grid(row=5, column=1)

tk.Label(root, text="Pagou? (Sim/Não):").grid(row=6, column=0)
Pagou_entry = tk.Entry(root)
Pagou_entry.grid(row=6, column=1)

tk.Label(root, text="Valor pago:").grid(row=7, column=0)
ValorPago_entry = tk.Entry(root)
ValorPago_entry.grid(row=7, column=1)

tk.Label(root, text="Forma de pagamento:").grid(row=8, column=0)
FormaPagamento_entry = tk.Entry(root)
FormaPagamento_entry.grid(row=8, column=1)

tk.Button(root, text="Adicionar Consulta", command=adicionar).grid(row=9, column=0, columnspan=2)

lista_consultas = tk.Listbox(root, width=50)
lista_consultas.grid(row=10, column=0, columnspan=2)

tk.Button(root, text="Atualizar Consulta", command=atualizar).grid(row=11, column=0, columnspan=2)
tk.Button(root, text="Excluir Consulta", command=excluir).grid(row=12, column=0, columnspan=2)
tk.Button(root, text="Listar Consultas por Médico", command=pesquisar).grid(row=14, column=0, columnspan=2)
tk.Button(root, text="Listar Todas as Consultas", command=listar).grid(row=16, column=0, columnspan=2)
listar()

root.mainloop()
