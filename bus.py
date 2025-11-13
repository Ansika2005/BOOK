import tkinter as tk
from tkinter import ttk, messagebox
import random

cities = ["Mumbai", "Pune", "Goa", "Nagpur", "Nashik", "Delhi"]
buses = ["RedBus", "Volvo Express", "Neeta Travels", "KSRTC", "Purple Travels"]
classes = ["Sleeper", "Seater", "AC", "Non-AC"]

users = {}

class BusBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚌 Bus Ticket Booking")
        self.root.geometry("900x600")
        self.root.config(bg="#f4f9ff")
        self.current_user = None
        self.login_page()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="🚌 Bus Booking System", font=("Helvetica", 28, "bold"),
                 bg="#f4f9ff", fg="#003366").pack(pady=40)
        tk.Label(self.root, text="Username", bg="#f4f9ff").pack()
        self.username = tk.Entry(self.root, font=("Arial", 14)); self.username.pack()
        tk.Label(self.root, text="Password", bg="#f4f9ff").pack(pady=5)
        self.password = tk.Entry(self.root, font=("Arial", 14), show="*"); self.password.pack()
        tk.Button(self.root, text="Login", bg="#0073e6", fg="white", font=("Arial", 12, "bold"),
                  command=self.login).pack(pady=20)
        reg = tk.Label(self.root, text="Register", fg="blue", bg="#f4f9ff", cursor="hand2")
        reg.pack()
        reg.bind("<Button-1>", lambda e: self.register_page())

    def register_page(self):
        self.clear()
        tk.Label(self.root, text="🪪 Register", font=("Helvetica", 24, "bold"),
                 bg="#f4f9ff", fg="#003366").pack(pady=30)
        tk.Label(self.root, text="Username", bg="#f4f9ff").pack()
        self.reg_user = tk.Entry(self.root, font=("Arial", 14)); self.reg_user.pack()
        tk.Label(self.root, text="Password", bg="#f4f9ff").pack()
        self.reg_pass = tk.Entry(self.root, font=("Arial", 14), show="*"); self.reg_pass.pack()
        tk.Button(self.root, text="Register", bg="#28a745", fg="white", font=("Arial", 12, "bold"),
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
                 bg="#003366", fg="white").pack(fill=tk.X)
        frame = tk.LabelFrame(self.root, text="Book Bus Ticket", bg="#f4f9ff", font=("Arial", 14, "bold"))
        frame.pack(padx=30, pady=40, fill=tk.BOTH)

        tk.Label(frame, text="From:", bg="#f4f9ff").grid(row=0, column=0, padx=10, pady=5)
        self.src = ttk.Combobox(frame, values=cities, state="readonly", width=20); self.src.grid(row=0, column=1)
        tk.Label(frame, text="To:", bg="#f4f9ff").grid(row=0, column=2, padx=10)
        self.dst = ttk.Combobox(frame, values=cities, state="readonly", width=20); self.dst.grid(row=0, column=3)
        tk.Label(frame, text="Bus Operator:", bg="#f4f9ff").grid(row=1, column=0, padx=10, pady=5)
        self.bus = ttk.Combobox(frame, values=buses, state="readonly", width=20); self.bus.grid(row=1, column=1)
        tk.Label(frame, text="Class:", bg="#f4f9ff").grid(row=1, column=2, padx=10)
        self.cls = ttk.Combobox(frame, values=classes, state="readonly", width=20); self.cls.grid(row=1, column=3)

        tk.Button(frame, text="Book Ticket", bg="#28a745", fg="white", font=("Arial", 14, "bold"),
                  command=self.book_ticket).grid(row=2, column=1, columnspan=2, pady=20)

    def book_ticket(self):
        if not all([self.src.get(), self.dst.get(), self.bus.get(), self.cls.get()]):
            messagebox.showwarning("Missing", "Please fill all fields")
            return
        if self.src.get() == self.dst.get():
            messagebox.showerror("Invalid", "Source and destination can't be same")
            return
        price = random.randint(300, 1200)
        tid = f"BUS{random.randint(1000,9999)}"
        messagebox.showinfo("Ticket Confirmed", f"Ticket ID: {tid}\nBus: {self.bus.get()}\nPrice: ₹{price}")
        self.dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    BusBookingApp(root)
    root.mainloop()
