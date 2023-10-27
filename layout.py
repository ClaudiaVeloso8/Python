from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkinter.tix import IMAGETEXT
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image 
import webbrowser 
import base64 
from tkinter import PhotoImage

import self

#criar variavel com nome da janela para abrir janela



class LoginPage:
    def __init__(self, root):
        self.root = root
        self.janela()
        self.imagem()
        self.icon()

    def icon(self):
        try:
            # Carregue o ícone em formato .ico
            self.root.iconbitmap("image.ico")
        except Exception as e:
            print(f"Erro ao carregar o ícone: {str(e)}")

    
    def janela(self):
        self.root.title("Login Registo Clientes")
        self.root.geometry("700x500")

    
    def imagem(self):
        bg_imagem = PhotoImage(file="registo.png")
        background_label = Label(self.root, image=bg_imagem)
        background_label.place(relwidth=1, relheight=1)

        # Defina o campos de entrada e botões acima da imagem
        self.user_label = Label(self.root, text="Login:")
        self.user_label.place(relx=0.2, rely=0.4)
        self.user_entry = Entry(self.root)
        self.user_entry.place(relx=0.3, rely=0.4, relwidth=0.4)

        self.pass_label = Label(self.root, text="Password:")
        self.pass_label.place(relx=0.2, rely=0.5)
        self.pass_entry = Entry(self.root, show="*")
        self.pass_entry.place(relx=0.3, rely=0.5, relwidth=0.4)

        self.login_button = Button(self.root, text="Enter", command=self.login)
        self.login_button.place(relx=0.4, rely=0.6, relwidth=0.2)

        background_label.image = bg_imagem

       

  
   


    def login(self):
        #  as credenciais de login aqui
        login = self.user_entry.get()
        password = self.pass_entry.get()

        if login == "admin" and password == "12345":
            self.abrir_aplicacao_principal()
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas.")


  

    def abrir_aplicacao_principal(self):
        app = Application(self.root)
        self.root.destroy()
        



    

        




class Pdf():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def gerarRelatorio(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.idRelatorio = self.id_entry.get()
        self.nomeRelatorio = self.nome_entry.get()
        self.nifRelatorio = self.nif_entry.get()
        self.enderecoRelatorio = self.endereco_entry.get()
        self.telemovelRelatorio = self.telemovel_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Dados do Cliente')

        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(50, 700, 'Id: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'NIF: ')
        self.c.drawString(50, 610, 'Endereço: ')
        self.c.drawString(50, 580, 'Telemóvel: ')

        self.c.setFont("Helvetica", 16)
        self.c.drawString(150, 700, self.idRelatorio)
        self.c.drawString(150, 670, self.nomeRelatorio)
        self.c.drawString(150, 640, self.nifRelatorio)
        self.c.drawString(150, 610, self.enderecoRelatorio)
        self.c.drawString(150, 580, self.telemovelRelatorio)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    #funcao para limpar campos
    def limpar_campos(self):
        self.id_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.nif_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.telemovel_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()
    def desconectar_bd(self):
        self.conn.close()
    def criar_tabelas(self):

    
        self.conecta_bd(); print("Ligando a base de dados")
        #Criar a tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                            id INTEGER PRIMARY KEY,
                            nome VARCHAR(40) NOT NULL,
                            nif int(15),
                            endereco VARCHAR(200),
                            telemovel VARCHAR(15)
                            );
                        """)
        self.conn.commit() 
        print("Base de dados criada")
        self.desconectar_bd()
    def variaveis(self):
        self.id = self.id_entry.get()
        self.nome = self.nome_entry.get()
        self.nif = self.nif_entry.get()
        self.endereco = self.endereco_entry.get()
        self.telemovel = self.telemovel_entry.get()

        
    def add_cliente(self):
        self.conecta_bd()
        self.variaveis()

        self.cursor.execute("""
                INSERT INTO clientes (nome, nif, endereco, telemovel)
                    values (?, ?, ?, ?)
                            """, (self.nome, self.nif, self.endereco, self.telemovel ))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_campos()
        self.desconectar_bd()

        messagebox.showinfo("Sucesso", "Cliente inserido com sucesso")


    def select_lista(self):

        self.listaCli.delete(*self.listaCli.get_children())  
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT id, nome, nif, endereco, telemovel from clientes ORDER BY nome ASC;""")

        for i in lista:
            self.listaCli.insert("", END, values=i)

        self.desconectar_bd()
    def pesquisar_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        nome = self.nome_entry.get()  # Obtenha o valor corretamente
        self.cursor.execute(
        """SELECT id, nome, nif, endereco, telemovel FROM clientes
        WHERE nome LIKE ? ORDER BY nome ASC""", ('%' + nome + '%',))  # Use ? como marcador de posição e passe o valor como uma tupla

        pesquisaNomeCli = self.cursor.fetchall()
        for i in pesquisaNomeCli:
         self.listaCli.insert("", END, values=i)

         self.limpar_campos()
         self.desconectar_bd()
    def imagens_base64(self):
        self.bt
    
    
    def OnDoubleClick(self, event):
        self.limpar_campos()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5 = self.listaCli.item(n, 'values')
            self.id_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.nif_entry.insert(END, col3)
            self.endereco_entry.insert(END, col4)
            self.telemovel_entry.insert(END, col5)

    
    def delete_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE id = ?
""", (self.id,))
        self.conn.commit()

        self.desconectar_bd()
        self.limpar_campos()
        self.select_lista()
        messagebox.showinfo("Sucesso", "Cliente apagado com sucesso")

    def update_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE CLIENTES SET nome = ?, nif = ?, endereco = ?,
                            telemovel = ? WHERE id = ?""", (self.nome, self.nif, self.endereco, self.telemovel, self.id))
        self.conn.commit()


        self.desconectar_bd()
        self.select_lista()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")

        
       





    

                             
                            

    




class Application(Funcs, Pdf):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.janela()
        self.frames__da__janela()
        self.widgets_frame1()
        self.lista_frame2()
        self.criar_tabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()# criar um loop para a janela permanecer aberta

    def janela(self):#criar uma funcao Janela para colocar o titulo da aplicacao e depois inicar ela na classe application
        self.root.title("Registo de Clientes", )
        self.root.configure(background='#49A')#cor de fundo
        self.root.geometry("700x500") # definir o tamanho da janela
        self.root.resizable(True, True) # para a janela ficar responsiva
       
       

    #função para frames
    def frames__da__janela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='lightgrey')
        self.frame_1.place(relx=0.05, rely=0.02, relwidth=0.90, relheight=0.46)
        self.frame_2 = Frame(self.root, bd=4, bg='lightgrey')
        self.frame_2.place(relx=0.05, rely=0.5, relwidth=0.90, relheight=0.46)

    #funcao para criar botoes
    def widgets_frame1(self):
       
    #criacao do botao limpar
        self.btn_limpar= Button(self.frame_1, text="Limpar", bd=2, bg='#107db2', fg='black', font=('verdana', 8, 'bold'), command=self.limpar_campos)
        self.btn_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
    #criacao do botao pesquisar
        self.btn_pesquisar=Button(self.frame_1, text="Pesquisar", bd=2, bg='#107db2', fg='black', font=('verdana', 8, 'bold'), command=self.pesquisar_cliente)
        self.btn_pesquisar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
    #criacao do botao inserir
        self.btn_inserir=Button(self.frame_1, text="Inserir",  bd=2, bg='#107db2', fg='black', font=('verdana', 8, 'bold'), command= self.add_cliente)
        self.btn_inserir.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

    # Criação do botão alterar
        self.btn_alterar = Button(self.frame_1, text="Alterar", bd=2, bg='#107db2', fg='black', font=('verdana', 8, 'bold'), command= self.update_cliente)
        self.btn_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

    #criacao do botao apagar
        self.btn_apagar=Button(self.frame_1, text="Apagar",  bd=2, bg='#107db2', fg='black', font=('verdana', 8, 'bold'), command=self.delete_cliente)
        self.btn_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

    #Criacao da label e entrada do ID
        self.lb_id = Label(self.frame_1, text="#", bg='#107db2', fg='white')
        self.lb_id.place(relx=0.05, rely=0.05)

        self.id_entry = Entry(self.frame_1)
        self.id_entry.place(relx=0.05, rely=0.15, relwidth=0.05)
        
    #Criacao da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#107db2', fg='white')
        self.lb_nome.place(relx=0.05, rely=0.3)

        self.nome_entry = Entry(self.frame_1) #width=40 #
        self.nome_entry.place(relx=0.05, rely=0.4, relwidth=0.4)

     #Criacao da label e entrada do nif
        self.lb_nif = Label(self.frame_1, text="Contribuinte", bg='#107db2', fg='white')
        self.lb_nif.place(relx=0.55, rely=0.3)

        self.nif_entry = Entry(self.frame_1)
        self.nif_entry.place(relx=0.55, rely=0.4, relwidth=0.2)

    #Criacao da label e entrada do endereço
        self.lb_endereco = Label(self.frame_1, text="Endereço", bg='#107db2', fg='white')
        self.lb_endereco.place(relx=0.05, rely=0.65)

        self.endereco_entry = Entry(self.frame_1)
        self.endereco_entry.place(relx=0.05, rely=0.75, relwidth=0.6)
  
  

    #Criacao da label e entrada do telemovel
        self.lb_telemovel = Label(self.frame_1, text="Telemóvel", bg='#107db2', fg='white')
        self.lb_telemovel.place(relx=0.7, rely=0.65)

        self.telemovel_entry = Entry(self.frame_1)
        self.telemovel_entry.place(relx=0.7, rely=0.75, relwidth=0.3)


    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("coll1", "coll2", "coll3", "coll4", "coll5"))   
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="#")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Contribuinte")
        self.listaCli.heading("#4", text="Endereço")
        self.listaCli.heading("#5", text="Telemóvel")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        self.listaCli.column("#5", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu= Menu(menubar)
        filemenu1=Menu(menubar)
        
        filemenu2 = Menu(menubar)
       

        def Quit(): 
            self.root.destroy()

        menubar.add_cascade(label="Opçoes", menu = filemenu)
        
        menubar.add_cascade(label="Gerar PDF", menu=filemenu1)

        menubar.add_cascade(label="Sair", menu= filemenu2)


        filemenu2.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Inserir Cliente", command=self.add_cliente)
        filemenu.add_command(label="Atualizar Cliente", command=self.update_cliente)
        filemenu.add_command(label="Apagar Cliente", command=self.delete_cliente)
        filemenu1.add_command(label="Gerar PDF", command=self.gerarRelatorio)

        
        

if __name__ == "__main__":
    root = Tk()
    app = LoginPage(root)
    root.mainloop()







        
        
        



        








Application()



