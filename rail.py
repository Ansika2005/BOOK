import tkinter as tk
from tkinter import ttk, messagebox
import random

stations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Pune"]
trains = ["Rajdhani Express", "Duronto Express", "Shatabdi Express", "Tejas Express", "Garib Rath"]
classes = ["Sleeper", "AC 2-Tier", "AC 3-Tier"]

users = {}

class RailwayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Indian Railways Booking")
        self.root.geometry("900x650")
        self.root.config(bg="white")
        self.current_user = None
        self.login_page()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="🚉 Indian Railways", font=("Helvetica", 28, "bold"), bg="white", fg="navy").pack(pady=40)
        tk.Label(self.root, text="Username", bg="white").pack()
        self.username = tk.Entry(self.root, font=("Arial", 14))
        self.username.pack()
        tk.Label(self.root, text="Password", bg="white").pack(pady=5)
        self.password = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", bg="blue", fg="white", font=("Arial", 12, "bold"),
                  command=self.login).pack(pady=20)
        link = tk.Label(self.root, text="Register", fg="blue", bg="white", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: self.register_page())

    def register_page(self):
        self.clear()
        tk.Label(self.root, text="🪪 Register", font=("Helvetica", 24, "bold"), bg="white", fg="navy").pack(pady=30)
        tk.Label(self.root, text="Username", bg="white").pack()
        self.reg_user = tk.Entry(self.root, font=("Arial", 14))
        self.reg_user.pack()
        tk.Label(self.root, text="Password", bg="white").pack()
        self.reg_pass = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.reg_pass.pack()
        tk.Button(self.root, text="Register", bg="green", fg="white", font=("Arial", 12, "bold"),
                  command=self.register_user).pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.login_page).pack()

    def register_user(self):
        u, p = self.reg_user.get(), self.reg_pass.get()
        if not u or not p:
            messagebox.showwarning("Empty", "Please fill all fields")
            return
        if u in users:
            messagebox.showerror("Exists", "Username already exists")
            return
        users[u] = p
        messagebox.showinfo("Success", "Registration successful!")
        self.login_page()

    def login(self):
        u, p = self.username.get(), self.password.get()
        if users.get(u) == p:
            self.current_user = u
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 20, "bold"),
                 bg="navy", fg="white").pack(fill=tk.X)
        frame = tk.LabelFrame(self.root, text="Book Train Ticket", bg="white", font=("Arial", 14, "bold"))
        frame.pack(padx=30, pady=30, fill=tk.BOTH)

        tk.Label(frame, text="From:", bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.src = ttk.Combobox(frame, values=stations, width=20, state="readonly"); self.src.grid(row=0, column=1)
        tk.Label(frame, text="To:", bg="white").grid(row=0, column=2, padx=10)
        self.dst = ttk.Combobox(frame, values=stations, width=20, state="readonly"); self.dst.grid(row=0, column=3)
        tk.Label(frame, text="Train:", bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.train = ttk.Combobox(frame, values=trains, width=20, state="readonly"); self.train.grid(row=1, column=1)
        tk.Label(frame, text="Class:", bg="white").grid(row=1, column=2, padx=10)
        self.cls = ttk.Combobox(frame, values=classes, width=20, state="readonly"); self.cls.grid(row=1, column=3)

        tk.Button(frame, text="Book Ticket", bg="green", fg="white", font=("Arial", 14, "bold"),
                  command=self.book_ticket).grid(row=2, column=1, columnspan=2, pady=20)

    def book_ticket(self):
        if not all([self.src.get(), self.dst.get(), self.train.get(), self.cls.get()]):
            messagebox.showwarning("Missing", "Please fill all fields")
            return
        if self.src.get() == self.dst.get():
            messagebox.showerror("Invalid", "Source and destination can't be same")
            return

        self.price = random.randint(500, 1500)
        self.ticket_id = f"RLY{random.randint(1000,9999)}"
        self.open_payment_window()

    def open_payment_window(self):
        pay_win = tk.Toplevel(self.root)
        pay_win.title("Payment Portal")
        pay_win.geometry("400x400")
        pay_win.config(bg="lightblue")

        tk.Label(pay_win, text="💰 Payment Portal", font=("Helvetica", 20, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)
        tk.Label(pay_win, text=f"Amount to Pay: ₹{self.price}", bg="lightblue", font=("Arial", 14)).pack(pady=10)
        tk.Label(pay_win, text="Select Payment Method:", bg="lightblue", font=("Arial", 12, "bold")).pack(pady=5)

        payment_mode = tk.StringVar(value="UPI")
        tk.Radiobutton(pay_win, text="UPI", variable=payment_mode, value="UPI", bg="lightblue").pack()
        tk.Radiobutton(pay_win, text="Card", variable=payment_mode, value="Card", bg="lightblue").pack()

        form_frame = tk.Frame(pay_win, bg="lightblue")
        form_frame.pack(pady=10)

        def show_fields():
            for widget in form_frame.winfo_children():
                widget.destroy()
            if payment_mode.get() == "UPI":
                tk.Label(form_frame, text="UPI ID:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
            else:
                tk.Label(form_frame, text="Card Number:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
                tk.Label(form_frame, text="Expiry (MM/YY):", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
                tk.Label(form_frame, text="CVV:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12), show="*").pack()

        payment_mode.trace("w", lambda *args: show_fields())
        show_fields()

        tk.Button(pay_win, text="Pay & Generate Ticket", bg="green", fg="white",
                  font=("Arial", 12, "bold"),
                  command=lambda: [messagebox.showinfo("Payment Successful", "Your payment has been processed successfully!"),
                                   pay_win.destroy(),
                                   self.generate_ticket(payment_mode.get())]).pack(pady=20)

    def generate_ticket(self, mode):
        ticket_win = tk.Toplevel(self.root)
        ticket_win.title("Ticket Details")
        ticket_win.geometry("450x400")
        ticket_win.config(bg="white")

        tk.Label(ticket_win, text="🎟️ Railway Ticket", font=("Helvetica", 22, "bold"), bg="navy", fg="white").pack(fill=tk.X)
        tk.Label(ticket_win, text=f"Ticket ID: {self.ticket_id}", font=("Arial", 14), bg="white").pack(pady=10)
        tk.Label(ticket_win, text=f"Passenger: {self.current_user}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"From: {self.src.get()} → To: {self.dst.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Train: {self.train.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Class: {self.cls.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Payment Mode: {mode}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Amount Paid: ₹{self.price}", font=("Arial", 14, "bold"), bg="white", fg="green").pack(pady=10)
        tk.Button(ticket_win, text="Close", bg="red", fg="white", font=("Arial", 12, "bold"),
                  command=ticket_win.destroy).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import random

stations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Pune"]
trains = ["Rajdhani Express", "Duronto Express", "Shatabdi Express", "Tejas Express", "Garib Rath"]
classes = ["Sleeper", "AC 2-Tier", "AC 3-Tier"]

users = {}

class RailwayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Indian Railways Booking")
        self.root.geometry("900x650")
        self.root.config(bg="white")
        self.current_user = None
        self.login_page()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="🚉 Indian Railways", font=("Helvetica", 28, "bold"), bg="white", fg="navy").pack(pady=40)
        tk.Label(self.root, text="Username", bg="white").pack()
        self.username = tk.Entry(self.root, font=("Arial", 14))
        self.username.pack()
        tk.Label(self.root, text="Password", bg="white").pack(pady=5)
        self.password = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", bg="blue", fg="white", font=("Arial", 12, "bold"),
                  command=self.login).pack(pady=20)
        link = tk.Label(self.root, text="Register", fg="blue", bg="white", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: self.register_page())

    def register_page(self):
        self.clear()
        tk.Label(self.root, text="🪪 Register", font=("Helvetica", 24, "bold"), bg="white", fg="navy").pack(pady=30)
        tk.Label(self.root, text="Username", bg="white").pack()
        self.reg_user = tk.Entry(self.root, font=("Arial", 14))
        self.reg_user.pack()
        tk.Label(self.root, text="Password", bg="white").pack()
        self.reg_pass = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.reg_pass.pack()
        tk.Button(self.root, text="Register", bg="green", fg="white", font=("Arial", 12, "bold"),
                  command=self.register_user).pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.login_page).pack()

    def register_user(self):
        u, p = self.reg_user.get(), self.reg_pass.get()
        if not u or not p:
            messagebox.showwarning("Empty", "Please fill all fields")
            return
        if u in users:
            messagebox.showerror("Exists", "Username already exists")
            return
        users[u] = p
        messagebox.showinfo("Success", "Registration successful!")
        self.login_page()

    def login(self):
        u, p = self.username.get(), self.password.get()
        if users.get(u) == p:
            self.current_user = u
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 20, "bold"),
                 bg="navy", fg="white").pack(fill=tk.X)
        frame = tk.LabelFrame(self.root, text="Book Train Ticket", bg="white", font=("Arial", 14, "bold"))
        frame.pack(padx=30, pady=30, fill=tk.BOTH)

        tk.Label(frame, text="From:", bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.src = ttk.Combobox(frame, values=stations, width=20, state="readonly"); self.src.grid(row=0, column=1)
        tk.Label(frame, text="To:", bg="white").grid(row=0, column=2, padx=10)
        self.dst = ttk.Combobox(frame, values=stations, width=20, state="readonly"); self.dst.grid(row=0, column=3)
        tk.Label(frame, text="Train:", bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.train = ttk.Combobox(frame, values=trains, width=20, state="readonly"); self.train.grid(row=1, column=1)
        tk.Label(frame, text="Class:", bg="white").grid(row=1, column=2, padx=10)
        self.cls = ttk.Combobox(frame, values=classes, width=20, state="readonly"); self.cls.grid(row=1, column=3)

        tk.Button(frame, text="Book Ticket", bg="green", fg="white", font=("Arial", 14, "bold"),
                  command=self.book_ticket).grid(row=2, column=1, columnspan=2, pady=20)

    def book_ticket(self):
        if not all([self.src.get(), self.dst.get(), self.train.get(), self.cls.get()]):
            messagebox.showwarning("Missing", "Please fill all fields")
            return
        if self.src.get() == self.dst.get():
            messagebox.showerror("Invalid", "Source and destination can't be same")
            return

        self.price = random.randint(500, 1500)
        self.ticket_id = f"RLY{random.randint(1000,9999)}"
        self.open_payment_window()

    def open_payment_window(self):
        pay_win = tk.Toplevel(self.root)
        pay_win.title("Payment Portal")
        pay_win.geometry("400x400")
        pay_win.config(bg="lightblue")

        tk.Label(pay_win, text="💰 Payment Portal", font=("Helvetica", 20, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)
        tk.Label(pay_win, text=f"Amount to Pay: ₹{self.price}", bg="lightblue", font=("Arial", 14)).pack(pady=10)
        tk.Label(pay_win, text="Select Payment Method:", bg="lightblue", font=("Arial", 12, "bold")).pack(pady=5)

        payment_mode = tk.StringVar(value="UPI")
        tk.Radiobutton(pay_win, text="UPI", variable=payment_mode, value="UPI", bg="lightblue").pack()
        tk.Radiobutton(pay_win, text="Card", variable=payment_mode, value="Card", bg="lightblue").pack()

        form_frame = tk.Frame(pay_win, bg="lightblue")
        form_frame.pack(pady=10)

        def show_fields():
            for widget in form_frame.winfo_children():
                widget.destroy()
            if payment_mode.get() == "UPI":
                tk.Label(form_frame, text="UPI ID:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
            else:
                tk.Label(form_frame, text="Card Number:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
                tk.Label(form_frame, text="Expiry (MM/YY):", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12)).pack()
                tk.Label(form_frame, text="CVV:", bg="lightblue").pack(pady=5)
                tk.Entry(form_frame, font=("Arial", 12), show="*").pack()

        payment_mode.trace("w", lambda *args: show_fields())
        show_fields()

        tk.Button(pay_win, text="Pay & Generate Ticket", bg="green", fg="white",
                  font=("Arial", 12, "bold"),
                  command=lambda: [messagebox.showinfo("Payment Successful", "Your payment has been processed successfully!"),
                                   pay_win.destroy(),
                                   self.generate_ticket(payment_mode.get())]).pack(pady=20)

    def generate_ticket(self, mode):
        ticket_win = tk.Toplevel(self.root)
        ticket_win.title("Ticket Details")
        ticket_win.geometry("450x400")
        ticket_win.config(bg="white")

        tk.Label(ticket_win, text="🎟️ Railway Ticket", font=("Helvetica", 22, "bold"), bg="navy", fg="white").pack(fill=tk.X)
        tk.Label(ticket_win, text=f"Ticket ID: {self.ticket_id}", font=("Arial", 14), bg="white").pack(pady=10)
        tk.Label(ticket_win, text=f"Passenger: {self.current_user}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"From: {self.src.get()} → To: {self.dst.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Train: {self.train.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Class: {self.cls.get()}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Payment Mode: {mode}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(ticket_win, text=f"Amount Paid: ₹{self.price}", font=("Arial", 14, "bold"), bg="white", fg="green").pack(pady=10)
        tk.Button(ticket_win, text="Close", bg="red", fg="white", font=("Arial", 12, "bold"),
                  command=ticket_win.destroy).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayApp(root)
    root.mainloop()
