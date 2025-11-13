import tkinter as tk
from tkinter import ttk, messagebox
import random

movies = ["Jawan", "Pathaan", "Animal", "Leo", "Pushpa 2", "Kalki 2898 AD"]
theatres = ["INOX", "PVR", "Cinepolis", "Carnival Cinemas", "Miraj"]
timings = ["10:00 AM", "1:30 PM", "4:30 PM", "7:30 PM", "10:00 PM"]
seat_types = ["Regular", "Premium", "VIP"]

users = {}

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Ticket Booking")
        self.root.geometry("900x600")
        self.root.config(bg="#fff7f2")
        self.current_user = None
        self.login_page()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ------------------ LOGIN PAGE -------------------
    def login_page(self):
        self.clear()
        tk.Label(self.root, text="🎥 Movie Booking System", font=("Helvetica", 28, "bold"),
                 bg="#fff7f2", fg="#660000").pack(pady=40)
        tk.Label(self.root, text="Username", bg="#fff7f2").pack()
        self.username = tk.Entry(self.root, font=("Arial", 14)); self.username.pack()
        tk.Label(self.root, text="Password", bg="#fff7f2").pack(pady=5)
        self.password = tk.Entry(self.root, font=("Arial", 14), show="*"); self.password.pack()
        tk.Button(self.root, text="Login", bg="#cc3300", fg="white", font=("Arial", 12, "bold"),
                  command=self.login).pack(pady=20)
        reg = tk.Label(self.root, text="Register", fg="blue", bg="#fff7f2", cursor="hand2")
        reg.pack()
        reg.bind("<Button-1>", lambda e: self.register_page())

    # ------------------ REGISTER PAGE -------------------
    def register_page(self):
        self.clear()
        tk.Label(self.root, text="🪪 Register", font=("Helvetica", 24, "bold"),
                 bg="#fff7f2", fg="#660000").pack(pady=30)
        tk.Label(self.root, text="Username", bg="#fff7f2").pack()
        self.reg_user = tk.Entry(self.root, font=("Arial", 14)); self.reg_user.pack()
        tk.Label(self.root, text="Password", bg="#fff7f2").pack()
        self.reg_pass = tk.Entry(self.root, font=("Arial", 14), show="*"); self.reg_pass.pack()
        tk.Button(self.root, text="Register", bg="#009933", fg="white", font=("Arial", 12, "bold"),
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

    # ------------------ LOGIN VALIDATION -------------------
    def login(self):
        u, p = self.username.get(), self.password.get()
        if users.get(u) == p:
            self.current_user = u
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    # ------------------ DASHBOARD -------------------
    def dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 20, "bold"),
                 bg="#660000", fg="white").pack(fill=tk.X)

        frame = tk.LabelFrame(self.root, text="Book Movie Ticket", bg="#fff7f2", font=("Arial", 14, "bold"))
        frame.pack(padx=30, pady=40, fill=tk.BOTH)

        tk.Label(frame, text="Movie:", bg="#fff7f2").grid(row=0, column=0, padx=10, pady=5)
        self.movie = ttk.Combobox(frame, values=movies, state="readonly", width=25); self.movie.grid(row=0, column=1)
        tk.Label(frame, text="Theatre:", bg="#fff7f2").grid(row=0, column=2, padx=10)
        self.theatre = ttk.Combobox(frame, values=theatres, state="readonly", width=25); self.theatre.grid(row=0, column=3)
        tk.Label(frame, text="Time:", bg="#fff7f2").grid(row=1, column=0, padx=10, pady=5)
        self.time = ttk.Combobox(frame, values=timings, state="readonly", width=25); self.time.grid(row=1, column=1)
        tk.Label(frame, text="Seat Type:", bg="#fff7f2").grid(row=1, column=2, padx=10)
        self.seat = ttk.Combobox(frame, values=seat_types, state="readonly", width=25); self.seat.grid(row=1, column=3)

        tk.Button(frame, text="Book Ticket", bg="#cc3300", fg="white", font=("Arial", 14, "bold"),
                  command=self.book_ticket).grid(row=2, column=1, columnspan=2, pady=30)

    # ------------------ BOOKING -------------------
    def book_ticket(self):
        if not all([self.movie.get(), self.theatre.get(), self.time.get(), self.seat.get()]):
            messagebox.showwarning("Missing", "Please fill all fields")
            return

        base_price = {"Regular": 200, "Premium": 350, "VIP": 500}
        price = base_price[self.seat.get()]
        tid = f"MOV{random.randint(1000,9999)}"

        # Ticket Confirmation Window
        win = tk.Toplevel(self.root)
        win.title("🎟 Movie Ticket")
        win.geometry("400x400")
        win.config(bg="#fff7f2")

        tk.Label(win, text="🎉 Booking Confirmed!", font=("Helvetica", 18, "bold"),
                 fg="#009933", bg="#fff7f2").pack(pady=15)
        info = f"Ticket ID: {tid}\nMovie: {self.movie.get()}\nTheatre: {self.theatre.get()}\nTime: {self.time.get()}\nSeat: {self.seat.get()}\nPrice: ₹{price}"
        tk.Label(win, text=info, bg="#fff7f2", font=("Arial", 13), justify="left").pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy, bg="#cc3300", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    MovieBookingApp(root)
    root.mainloop()
