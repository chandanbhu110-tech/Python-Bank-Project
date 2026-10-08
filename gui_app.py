import tkinter as tk
from tkinter import ttk, messagebox
import register
from bank import Bank
from customer import Customer
from database import db_query

class BankGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Apex Bank - Management System")
        self.geometry("900" + "x" + "650")
        self.minsize(850, 600)
        self.configure(bg="#0f172a")  # Dark slate background

        # App state
        self.current_user = None
        self.bank_service = None
        self.account_info = None

        # Custom ttk styles
        self.setup_styles()

        # Main Container
        self.container = tk.Frame(self, bg="#0f172a")
        self.container.pack(fill="both", expand=True)

        # Show Auth Screen
        self.show_auth_screen()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Configure colors
        style.configure("TFrame", background="#0f172a")
        style.configure("Card.TFrame", background="#1e293b", relief="flat")
        
        style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#1e293b", foreground="#f8fafc", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#0f172a", foreground="#38bdf8", font=("Segoe UI", 20, "bold"))
        style.configure("SubHeader.TLabel", background="#1e293b", foreground="#94a3b8", font=("Segoe UI", 11))
        
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#0284c7", foreground="#ffffff", borderwidth=0, padding=8)
        style.map("Primary.TButton", background=[("active", "#0369a1")])

        style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background="#10b981", foreground="#ffffff", borderwidth=0, padding=8)
        style.map("Success.TButton", background=[("active", "#059669")])

        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background="#ef4444", foreground="#ffffff", borderwidth=0, padding=8)
        style.map("Danger.TButton", background=[("active", "#dc2626")])

        style.configure("Treeview", background="#1e293b", foreground="#f8fafc", fieldbackground="#1e293b", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#334155", foreground="#38bdf8", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#0284c7")], foreground=[("selected", "#ffffff")])

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ================= AUTHENTICATION SCREEN =================
    def show_auth_screen(self):
        self.clear_container()

        # Header Title
        title_frame = tk.Frame(self.container, bg="#0f172a")
        title_frame.pack(pady=25)
        
        tk.Label(title_frame, text="🏦 Apex Bank Management System", font=("Segoe UI", 24, "bold"), fg="#38bdf8", bg="#0f172a").pack()
        tk.Label(title_frame, text="Secure, Fast & Reliable Modern Banking Solution", font=("Segoe UI", 11), fg="#94a3b8", bg="#0f172a").pack(pady=4)

        # Tabbed Auth Card
        card = tk.Frame(self.container, bg="#1e293b", padx=30, pady=30)
        card.pack(pady=10, ipadx=10, ipady=10)

        notebook = ttk.Notebook(card)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Login
        login_tab = tk.Frame(notebook, bg="#1e293b", padx=20, pady=20)
        notebook.add(login_tab, text=" Sign In ")
        self.build_login_tab(login_tab)

        # Tab 2: Register
        register_tab = tk.Frame(notebook, bg="#1e293b", padx=20, pady=20)
        notebook.add(register_tab, text=" Create Account ")
        self.build_register_tab(register_tab)

    def build_login_tab(self, parent):
        tk.Label(parent, text="Username", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(5, 2))
        username_ent = tk.Entry(parent, font=("Segoe UI", 11), bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        username_ent.pack(fill="x", pady=(0, 15), ipady=5)

        tk.Label(parent, text="Password", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(5, 2))
        password_ent = tk.Entry(parent, font=("Segoe UI", 11), show="•", bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        password_ent.pack(fill="x", pady=(0, 20), ipady=5)

        def handle_login():
            u = username_ent.get().strip()
            p = password_ent.get().strip()

            success, msg, user_data = register.authenticate_user(u, p)
            if success:
                self.current_user = u
                self.account_info = user_data
                self.bank_service = Bank(u, user_data["account_number"])
                messagebox.showinfo("Login Success", f"Welcome back, {user_data['name']}!")
                self.show_dashboard_screen()
            else:
                messagebox.showerror("Login Error", msg)

        btn = tk.Button(parent, text="Sign In to Dashboard", font=("Segoe UI", 11, "bold"), bg="#0284c7", fg="#ffffff", activebackground="#0369a1", activeforeground="white", bd=0, cursor="hand2", command=handle_login)
        btn.pack(fill="x", ipady=8, pady=5)

    def build_register_tab(self, parent):
        # Grid layout for inputs
        fields = [
            ("Username", "reg_username", False),
            ("Password", "reg_password", True),
            ("Full Name", "reg_name", False),
            ("Age", "reg_age", False),
            ("City", "reg_city", False)
        ]

        self.reg_entries = {}
        for idx, (label_text, key, is_pwd) in enumerate(fields):
            tk.Label(parent, text=label_text, font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#1e293b").grid(row=idx, column=0, sticky="w", pady=4)
            entry = tk.Entry(parent, font=("Segoe UI", 10), bg="#0f172a", fg="#ffffff", insertbackground="white", show="•" if is_pwd else "", relief="solid", bd=1)
            entry.grid(row=idx, column=1, sticky="ew", pady=4, padx=(10, 0), ipady=4)
            self.reg_entries[key] = entry

        parent.columnconfigure(1, weight=1)

        def handle_register():
            u = self.reg_entries["reg_username"].get().strip()
            p = self.reg_entries["reg_password"].get().strip()
            n = self.reg_entries["reg_name"].get().strip()
            a = self.reg_entries["reg_age"].get().strip()
            c = self.reg_entries["reg_city"].get().strip()

            success, msg, acc_num = register.register_user(u, p, n, a, c)
            if success:
                messagebox.showinfo("Registration Success", msg)
                for entry in self.reg_entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Registration Error", msg)

        btn = tk.Button(parent, text="Create Account Now", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="#ffffff", activebackground="#059669", activeforeground="white", bd=0, cursor="hand2", command=handle_register)
        btn.grid(row=len(fields), column=0, columnspan=2, sticky="ew", pady=(15, 5), ipady=6)

    # ================= DASHBOARD SCREEN =================
    def show_dashboard_screen(self):
        self.clear_container()

        # Top Bar Navigation
        top_bar = tk.Frame(self.container, bg="#1e293b", padx=20, pady=12)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="🏦 Apex Banking Dashboard", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#1e293b").pack(side="left")

        user_details = f"User: {self.account_info['name']} | Account No: {self.bank_service.account_number}"
        tk.Label(top_bar, text=user_details, font=("Segoe UI", 10), fg="#94a3b8", bg="#1e293b").pack(side="left", padx=20)

        logout_btn = tk.Button(top_bar, text="Logout", font=("Segoe UI", 9, "bold"), bg="#ef4444", fg="#ffffff", bd=0, cursor="hand2", padx=12, pady=4, command=self.show_auth_screen)
        logout_btn.pack(side="right")

        # Main Body Grid (Left: Balance & Actions, Right: Transactions)
        body = tk.Frame(self.container, bg="#0f172a", padx=20, pady=15)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=4)
        body.columnconfigure(1, weight=6)
        body.rowconfigure(0, weight=1)

        # Left Frame (Balance & Banking Operations)
        left_frame = tk.Frame(body, bg="#0f172a")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Balance Card
        self.balance_card = tk.Frame(left_frame, bg="#0284c7", padx=20, pady=20)
        self.balance_card.pack(fill="x", pady=(0, 15))

        tk.Label(self.balance_card, text="CURRENT ACCOUNT BALANCE", font=("Segoe UI", 9, "bold"), fg="#bae6fd", bg="#0284c7").pack(anchor="w")
        
        self.balance_val_lbl = tk.Label(self.balance_card, text=f"${self.bank_service.get_balance():,.2f}", font=("Segoe UI", 24, "bold"), fg="#ffffff", bg="#0284c7")
        self.balance_val_lbl.pack(anchor="w", pady=5)

        tk.Label(self.balance_card, text=f"City: {self.account_info['city']} | Age: {self.account_info['age']}", font=("Segoe UI", 9), fg="#e0f2fe", bg="#0284c7").pack(anchor="w")

        # Banking Actions Tabs Card
        actions_card = tk.Frame(left_frame, bg="#1e293b", padx=15, pady=15)
        actions_card.pack(fill="both", expand=True)

        tk.Label(actions_card, text="Banking Services", font=("Segoe UI", 12, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w", pady=(0, 10))

        action_notebook = ttk.Notebook(actions_card)
        action_notebook.pack(fill="both", expand=True)

        # Deposit Tab
        dep_tab = tk.Frame(action_notebook, bg="#1e293b", padx=15, pady=15)
        action_notebook.add(dep_tab, text=" Deposit ")
        self.build_deposit_ui(dep_tab)

        # Withdraw Tab
        wth_tab = tk.Frame(action_notebook, bg="#1e293b", padx=15, pady=15)
        action_notebook.add(wth_tab, text=" Withdraw ")
        self.build_withdraw_ui(wth_tab)

        # Transfer Tab
        trf_tab = tk.Frame(action_notebook, bg="#1e293b", padx=15, pady=15)
        action_notebook.add(trf_tab, text=" Transfer ")
        self.build_transfer_ui(trf_tab)

        # Right Frame (Transaction History Table)
        right_frame = tk.Frame(body, bg="#1e293b", padx=15, pady=15)
        right_frame.grid(row=0, column=1, sticky="nsew")

        header_row = tk.Frame(right_frame, bg="#1e293b")
        header_row.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_row, text="Transaction History", font=("Segoe UI", 12, "bold"), fg="#38bdf8", bg="#1e293b").pack(side="left")
        refresh_btn = tk.Button(header_row, text="🔄 Refresh", font=("Segoe UI", 8, "bold"), bg="#334155", fg="#f8fafc", bd=0, cursor="hand2", command=self.refresh_dashboard)
        refresh_btn.pack(side="right")

        # Treeview Table
        cols = ("timedate", "remarks", "amount")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", selectmode="browse")
        
        self.tree.heading("timedate", text="Date & Time")
        self.tree.heading("remarks", text="Description")
        self.tree.heading("amount", text="Amount ($)")

        self.tree.column("timedate", width=140, anchor="w")
        self.tree.column("remarks", width=180, anchor="w")
        self.tree.column("amount", width=90, anchor="e")

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_dashboard()

    def refresh_dashboard(self):
        # Update Balance Label
        bal = self.bank_service.get_balance()
        self.balance_val_lbl.config(text=f"${bal:,.2f}")

        # Refresh Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = self.bank_service.get_transaction_history()
        for h in history:
            formatted_amt = f"${h['amount']:,.2f}"
            self.tree.insert("", "end", values=(h["timedate"], h["remarks"], formatted_amt))

    def build_deposit_ui(self, parent):
        tk.Label(parent, text="Enter Amount to Deposit ($)", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(5, 2))
        amt_ent = tk.Entry(parent, font=("Segoe UI", 11), bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        amt_ent.pack(fill="x", pady=(0, 15), ipady=4)

        def do_deposit():
            try:
                amt = float(amt_ent.get().strip())
                success, msg, _ = self.bank_service.deposit(amt)
                if success:
                    messagebox.showinfo("Deposit Success", msg)
                    amt_ent.delete(0, tk.END)
                    self.refresh_dashboard()
                else:
                    messagebox.showerror("Deposit Error", msg)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric amount.")

        btn = tk.Button(parent, text="Confirm Deposit", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="#ffffff", activebackground="#059669", bd=0, cursor="hand2", command=do_deposit)
        btn.pack(fill="x", ipady=6)

    def build_withdraw_ui(self, parent):
        tk.Label(parent, text="Enter Amount to Withdraw ($)", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(5, 2))
        amt_ent = tk.Entry(parent, font=("Segoe UI", 11), bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        amt_ent.pack(fill="x", pady=(0, 15), ipady=4)

        def do_withdraw():
            try:
                amt = float(amt_ent.get().strip())
                success, msg, _ = self.bank_service.withdraw(amt)
                if success:
                    messagebox.showinfo("Withdrawal Success", msg)
                    amt_ent.delete(0, tk.END)
                    self.refresh_dashboard()
                else:
                    messagebox.showerror("Withdrawal Error", msg)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric amount.")

        btn = tk.Button(parent, text="Confirm Withdrawal", font=("Segoe UI", 10, "bold"), bg="#ef4444", fg="#ffffff", activebackground="#dc2626", bd=0, cursor="hand2", command=do_withdraw)
        btn.pack(fill="x", ipady=6)

    def build_transfer_ui(self, parent):
        tk.Label(parent, text="Receiver Account Number", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(2, 2))
        rec_ent = tk.Entry(parent, font=("Segoe UI", 10), bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        rec_ent.pack(fill="x", pady=(0, 8), ipady=3)

        tk.Label(parent, text="Amount to Transfer ($)", font=("Segoe UI", 9, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(2, 2))
        amt_ent = tk.Entry(parent, font=("Segoe UI", 10), bg="#0f172a", fg="#ffffff", insertbackground="white", relief="solid", bd=1)
        amt_ent.pack(fill="x", pady=(0, 12), ipady=3)

        def do_transfer():
            try:
                rec = int(rec_ent.get().strip())
                amt = float(amt_ent.get().strip())
                success, msg, _ = self.bank_service.fundtransfer(rec, amt)
                if success:
                    messagebox.showinfo("Transfer Success", msg)
                    rec_ent.delete(0, tk.END)
                    amt_ent.delete(0, tk.END)
                    self.refresh_dashboard()
                else:
                    messagebox.showerror("Transfer Error", msg)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values.")

        btn = tk.Button(parent, text="Transfer Funds", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="#ffffff", activebackground="#0369a1", bd=0, cursor="hand2", command=do_transfer)
        btn.pack(fill="x", ipady=6)

if __name__ == "__main__":
    app = BankGUI()
    app.mainloop()
