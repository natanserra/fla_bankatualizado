import tkinter as tk
from tkinter import messagebox, simpledialog

class FlaBanksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlaBank's - Sistema Bancário")
        self.root.geometry("450x400")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)
        
        self.usuarios = {  # Dicionário para armazenar usuários e seus dados
            "admin": {"senha": "123", "saldo": 1000.0, "historico": []},
            "joao": {"senha": "456", "saldo": 500.0, "historico": []},
            "maria": {"senha": "789", "saldo": 300.0, "historico": []}
        }
        
        self.usuario_atual = None
        
        self.frame_login = tk.Frame(self.root, bg="#34495E", padx=30, pady=30, bd=2, relief="ridge")
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(self.frame_login, text="Usuário:", fg="white", bg="#34495E", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_usuario = tk.Entry(self.frame_login, font=("Arial", 12), width=20, relief="flat", highlightbackground="#27AE60", highlightthickness=1)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame_login, text="Senha:", fg="white", bg="#34495E", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_senha = tk.Entry(self.frame_login, show="*", font=("Arial", 12), width=20, relief="flat", highlightbackground="#27AE60", highlightthickness=1)
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)
        
        self.btn_login = tk.Button(self.frame_login, text="Login", command=self.verificar_login, font=("Arial", 12, "bold"), bg="#27AE60", fg="white", width=20, relief="flat", bd=3, cursor="hand2")
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=15)
    
    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if usuario in self.usuarios and self.usuarios[usuario]["senha"] == senha:
            self.usuario_atual = usuario
            self.abrir_menu_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    
    def abrir_menu_principal(self):
        self.frame_login.destroy()
        
        self.frame_menu = tk.Frame(self.root, bg="#34495E", padx=30, pady=30, bd=2, relief="ridge")
        self.frame_menu.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(self.frame_menu, text=f"Bem-vindo ao FlaBank's, {self.usuario_atual}!", font=("Arial", 14, "bold"), fg="white", bg="#34495E").pack(pady=10)
        
        botoes = [
            ("Consultar Saldo", self.consultar_saldo),
            ("Depósito", self.depositar),
            ("Saque", self.sacar),
            ("Transferência", self.transferir),
            ("Histórico", self.consultar_historico),
            ("Sair", self.sair)
        ]
        
        cores = ["#2980B9", "#2980B9", "#2980B9", "#2980B9", "#2980B9", "#C0392B"]
        
        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(self.frame_menu, text=texto, width=25, font=("Arial", 12, "bold"), bg=cores[i], fg="white", relief="flat", bd=3, cursor="hand2", command=comando)
            btn.pack(pady=5)
    
    def consultar_saldo(self):
        saldo_atual = self.usuarios[self.usuario_atual]["saldo"]
        messagebox.showinfo("Saldo Atual", f"Seu saldo é: R$ {saldo_atual:.2f}")
    
    def depositar(self):
        valor = self.solicitar_valor("Depósito")
        if valor:
            self.usuarios[self.usuario_atual]["saldo"] += valor
            self.usuarios[self.usuario_atual]["historico"].append(f"Depósito: R$ {valor:.2f}")
            messagebox.showinfo("Depósito", f"Depósito de R$ {valor:.2f} realizado com sucesso! Novo saldo: R$ {self.usuarios[self.usuario_atual]['saldo']:.2f}")
    
    def sacar(self):
        valor = self.solicitar_valor("Saque")
        if valor:
            saldo_atual = self.usuarios[self.usuario_atual]["saldo"]
            if valor > saldo_atual:
                messagebox.showerror("Erro", "Saldo insuficiente!")
            else:
                self.usuarios[self.usuario_atual]["saldo"] -= valor
                self.usuarios[self.usuario_atual]["historico"].append(f"Saque: R$ {valor:.2f}")
                messagebox.showinfo("Saque", f"Saque de R$ {valor:.2f} realizado com sucesso! Novo saldo: R$ {self.usuarios[self.usuario_atual]['saldo']:.2f}")
    
    def transferir(self):
        valor = self.solicitar_valor("Transferência")
        if valor:
            saldo_atual = self.usuarios[self.usuario_atual]["saldo"]
            if valor > saldo_atual:
                messagebox.showerror("Erro", "Saldo insuficiente!")
            else:
                conta_destino = simpledialog.askstring("Conta Destino", "Informe o número da conta de destino:")
                if conta_destino:
                    self.usuarios[self.usuario_atual]["saldo"] -= valor
                    self.usuarios[self.usuario_atual]["historico"].append(f"Transferência: R$ {valor:.2f} para a conta {conta_destino}")
                    messagebox.showinfo("Transferência", f"Transferência de R$ {valor:.2f} realizada com sucesso para a conta {conta_destino}! Novo saldo: R$ {self.usuarios[self.usuario_atual]['saldo']:.2f}")
    
    def solicitar_valor(self, operacao):
        valor_str = simpledialog.askstring(operacao, f"Informe o valor para {operacao.lower()}:")
        if valor_str:
            try:
                valor = float(valor_str)
                if valor <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                    return None
                return valor
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        return None
    
    def consultar_historico(self):
        historico = self.usuarios[self.usuario_atual]["historico"]
        if historico:
            transacoes = "\n".join(historico)
            messagebox.showinfo("Histórico de Transações", transacoes)
        else:
            messagebox.showinfo("Histórico", "Nenhuma transação realizada ainda!")
    
    def sair(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlaBanksApp(root)
    root.mainloop()
