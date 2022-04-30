# Modulos necessários para calcular a idade, validar data, cpf, banco de dados e fazer o GUI.
import re
import datetime
import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import StringVar, messagebox

# Classe para conexão do banco de dados.
class ConectarDB:
    def __init__(self):
        self.con = sqlite3.connect('db.sqlite3')
        self.cur = self.con.cursor()
        self.criar_tabela()

    # Cria a tabela Candidato.
    def criar_tabela(self):
            self.cur.execute('''CREATE TABLE IF NOT EXISTS Candidato (
                nome TEXT,
                sobrenome TEXT,
                cpf TEXT,
                data_nasc TEXT,
                vaga TEXT)''') 

    # Alimentar a tabela.
    def inserir_registro(self, nome, sobrenome, cpf, data_nasc, vaga):
        try:
            self.cur.execute(
                '''INSERT INTO Candidato VALUES (?, ?, ?, ?, ?)''', (nome, sobrenome, cpf, data_nasc, vaga))
        except Exception:
            print(f'Registro não inserido, erro: {Exception}')
            self.con.rollback()
        else:
            self.con.commit()

    # Consulta no banco.
    def consultar_registros(self):
        return self.cur.execute('SELECT rowid, * FROM Candidato').fetchall()

    # Consulta o ultimo registro, usa o ROWID, padrão do SQLite.
    def consultar_ultimo_rowid(self):
        return self.cur.execute('SELECT MAX(rowid) FROM Candidato').fetchone()

    # Remove registro para o botão de excluir.
    def remover_registro(self, rowid):
        try:
            self.cur.execute("DELETE FROM Candidato WHERE rowid=?", (rowid,))
        except Exception:
            print(f'Registro não removido, erro: {Exception}')
            self.con.rollback()
        else:
            self.con.commit()

# Classe para a GUI.
class Janela(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Título da janela principal.
        master.title('SYS XPTO')

        # Tamanho da janela principal.
        master.geometry('770x384')

        # Instanciando a conexão com o banco.
        self.banco = ConectarDB()

        # Gerenciador de layout da janela principal.
        self.pack()

        # Criando os widgets da interface.
        self.criar_widgets()

    # Método para calcular a idade para ser apresentado na Treeview.
    def calcula_idade(self, data_nasc):
        idade_calculada = []
        idade = datetime.datetime.now().year - int(data_nasc[6:])
        idade_calculada.append(idade)
        if idade >= 18:
            maior_idade = 'Sim'
        else:
            maior_idade = 'Não'
        idade_calculada.append(maior_idade)
        return idade_calculada

    # Criar widgets da janela.
    def criar_widgets(self):
        # Frames.
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=5)

        # Labels.
        label_nome = tk.Label(frame1, text='Nome')
        label_nome.grid(row=0, column=0)

        label_sobrenome = tk.Label(frame1, text='Sobrenome')
        label_sobrenome.grid(row=0, column=1)

        label_cpf = tk.Label(frame1, text='CPF')
        label_cpf.grid(row=0, column=2)

        label_data_nasc = tk.Label(frame1, text='Data de Nascimento')
        label_data_nasc.grid(row=0, column=3)

        label_vagas = tk.Label(frame1, text='Vagas')
        label_vagas.grid(row=0, column=4)

        # Entrada de texto.
        self.entry_nome = tk.Entry(frame1)
        self.entry_nome.grid(row=1, column=0)

        self.entry_sobrenome = tk.Entry(frame1)
        self.entry_sobrenome.grid(row=1, column=1, padx=10)

        self.entry_cpf = StringVar()
        self.entry_cpf = tk.Entry(frame1)
        self.entry_cpf.grid(row=1, column=2)

        self.entry_data_nasc = tk.Entry(frame1)
        self.entry_data_nasc.grid(row=1, column=3, padx=10)

        # Combobox para associar o candidato as vagas disponíveis
        self.vagas_combobox = tkk.Combobox(frame1, width=22, values=[
                                            "Analista de dados",
                                            "DBA", 
                                            "Desenvolvedor(a) Full-Stack",
                                            "Estágio Desenvolvedor(a)", 
                                            "Tech Lead"])
        self.vagas_combobox.grid(row=1, column=4)
        self.vagas_combobox.set(value='Não selecionado')

        # Botão para adicionar um novo registro.
        button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_adicionar['command'] = self.adicionar_registro
        button_adicionar.grid(row=0, column=5, rowspan=2, sticky='s', padx=10)
        # Botão salvar para confirmar os dados na Treeview.
        button_salvar = tk.Button(frame3, text='Salvar', bg='blue', fg='white')
        button_salvar['command'] = self.salvar_registro
        button_salvar.pack(pady=10)

        # Treeview.
        self.treeview = tkk.Treeview(frame2, columns=('Nome', 'Sobrenome', 'CPF', 'Data de Nascimento', 'Idade', 'Maior de idade', 'Vaga'))
        self.treeview.column('#0', width=50, minwidth=50)
        self.treeview.column('#1', width=100, minwidth=100)
        self.treeview.column('#2', width=110, minwidth=110)
        self.treeview.column('#3', width=90, minwidth=90)
        self.treeview.column('#4', width=115, minwidth=115)
        self.treeview.column('#5', width=50, minwidth=50)
        self.treeview.column('#6', width=90, minwidth=90)
        self.treeview.heading('#0', text='ID')
        self.treeview.heading('#1', text='Nome')
        self.treeview.heading('#2', text='Sobrenome')
        self.treeview.heading('#3', text='CPF')
        self.treeview.heading('#4', text='Data de Nascimento')
        self.treeview.heading('#5', text='Idade')
        self.treeview.heading('#6', text='Maior de idade')
        self.treeview.heading('#7', text='Vaga')

        # Inserindo os dados do banco no treeview.
        for row in self.banco.consultar_registros():
            self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], self.calcula_idade(row[4])[0], self.calcula_idade(row[4])[1], row[5]))
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Botão para remover um item.
        button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_excluir['command'] = self.excluir_registro
        button_excluir.pack(pady=10)

    # Método para o botão salvar.
    def salvar_registro(self):
        messagebox.showinfo('Salvar', 'Candidatos cadastrados com sucesso')


    '''def pesquisa_cpf(self, cpf):
        for banco in self.banco.consultar_registros():
            for cpf in banco:
                if cpf == cpf:
                    return True
        return False'''

    # Método para o botão adicionar.
    def adicionar_registro(self):
        # Coletando os valores.
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        cpf = self.entry_cpf.get()
        data_nasc = self.entry_data_nasc.get()
        vaga = self.vagas_combobox.get()

        # Validação usando regex.
        validar_data = re.search(r'(..)/(..)/(....)', data_nasc)
        validar_cpf = re.search(r'(...).(...).(...)-(..)', cpf)
    
        
        '''if self.pesquisa_cpf(cpf):
            messagebox.showerror('Erro', 'Permitido apenas um cpf por cadastro')'''
        
        if validar_data and validar_cpf and nome != "" and sobrenome != "" and str(vaga) != "Não selecionado":
            self.banco.inserir_registro(nome=nome, sobrenome=sobrenome, cpf=cpf, data_nasc=data_nasc, vaga=vaga)

            # Coletando o ultimo registro que foi inserida no banco.
            rowid = self.banco.consultar_ultimo_rowid()[0]

            # Adicionando os novos dados no treeview.
            self.treeview.insert('', 'end', text=rowid, values=(nome, sobrenome, cpf, data_nasc, self.calcula_idade(data_nasc)[0], self.calcula_idade(data_nasc)[1], vaga))
        else:
            messagebox.showerror('Erro', 'Digite todos os dados, cpf: xxx.xxx.xxx-xx data: dd/mm/yyyy')
            
    # Método do botão excluir.
    def excluir_registro(self):
        # Verificando se algum item está selecionado.
        if not self.treeview.focus():
            messagebox.showerror('Erro', 'Nenhum item selecionado')
        else:
            # Coletando qual item está selecionado.
            item_selecionado = self.treeview.focus()

            # Coletando os dados do item selecionado (dicionário).
            rowid = self.treeview.item(item_selecionado)

            # Removendo o item com base no valor do rowid (argumento text do treeview).
            # Removendo valor da tabela.
            self.banco.remover_registro(rowid['text'])

            # Removendo valor do treeview.
            self.treeview.delete(item_selecionado)


root = tk.Tk()
app = Janela(master=root)
app.mainloop()