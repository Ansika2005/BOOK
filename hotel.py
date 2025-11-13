import tkinter as tk
from tkinter import ttk, messagebox
import random

hotels = ["Taj Palace", "Oberoi", "Leela", "ITC Grand", "Hyatt Regency", "Marriott"]
cities = ["Mumbai", "Delhi", "Chennai", "Kolkata", "Bangalore", "Goa"]
room_types = ["Single", "Double", "Deluxe", "Suite"]
users = {}

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏨 Hotel Room Booking System")
        self.root.geometry("900x600")
        self.root.config(bg="#f7faff")
        self.current_user = None
        self.login_page()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------------- LOGIN PAGE ----------------
    def login_page(self):
        self.clear()
        tk.Label(self.root, text="🏨 Hotel Booking System", font=("Helvetica", 28, "bold"),
                 bg="#f7faff", fg="#002b5c").pack(pady=40)
        tk.Label(self.root, text="Username", bg="#f7faff").pack()
        self.username = tk.Entry(self.root, font=("Arial", 14)); self.username.pack()
        tk.Label(self.root, text="Password", bg="#f7faff").pack(pady=5)
        self.password = tk.Entry(self.root, font=("Arial", 14), show="*"); self.password.pack()
        tk.Button(self.root, text="Login", bg="#0047b3", fg="white", font=("Arial", 12, "bold"),
                  command=self.login).pack(pady=20)
        reg = tk.Label(self.root, text="Register", fg="blue", bg="#f7faff", cursor="hand2")
        reg.pack()
        reg.bind("<Button-1>", lambda e: self.register_page())

    # ---------------- REGISTER PAGE ----------------
    def register_page(self):
        self.clear()
        tk.Label(self.root, text="🪪 Register", font=("Helvetica", 24, "bold"),
                 bg="#f7faff", fg="#002b5c").pack(pady=30)
        tk.Label(self.root, text="Username", bg="#f7faff").pack()
        self.reg_user = tk.Entry(self.root, font=("Arial", 14)); self.reg_user.pack()
        tk.Label(self.root, text="Password", bg="#f7faff").pack()
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

    # ---------------- LOGIN VALIDATION ----------------
    def login(self):
        u, p = self.username.get(), self.password.get()
        if users.get(u) == p:
            self.current_user = u
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    # ---------------- DASHBOARD ----------------
    def dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 20, "bold"),
                 bg="#002b5c", fg="white").pack(fill=tk.X)

        frame = tk.LabelFrame(self.root, text="Book Your Room", bg="#f7faff", font=("Arial", 14, "bold"))
        frame.pack(padx=30, pady=40, fill=tk.BOTH)

        tk.Label(frame, text="City:", bg="#f7faff").grid(row=0, column=0, padx=10, pady=5)
        self.city = ttk.Combobox(frame, values=cities, state="readonly", width=25); self.city.grid(row=0, column=1)
        tk.Label(frame, text="Hotel:", bg="#f7faff").grid(row=0, column=2, padx=10)
        self.hotel = ttk.Combobox(frame, values=hotels, state="readonly", width=25); self.hotel.grid(row=0, column=3)
        tk.Label(frame, text="Room Type:", bg="#f7faff").grid(row=1, column=0, padx=10, pady=5)
        self.room = ttk.Combobox(frame, values=room_types, state="readonly", width=25); self.room.grid(row=1, column=1)
        tk.Label(frame, text="No. of Nights:", bg="#f7faff").grid(row=1, column=2, padx=10)
        self.nights = tk.Entry(frame, font=("Arial", 14), width=10); self.nights.grid(row=1, column=3)

        tk.Button(frame, text="Book Room", bg="#009933", fg="white", font=("Arial", 14, "bold"),
                  command=self.book_room).grid(row=2, column=1, columnspan=2, pady=30)

    # ---------------- BOOKING FUNCTION ----------------
    def book_room(self):
        if not all([self.city.get(), self.hotel.get(), self.room.get(), self.nights.get()]):
            messagebox.showwarning("Missing", "Please fill all fields")
            return
        try:
            nights = int(self.nights.get())
            if nights <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Enter valid number of nights")
            return

        base_price = {"Single": 1500, "Double": 2500, "Deluxe": 4000, "Suite": 6000}
        total = base_price[self.room.get()] * nights
        tid = f"HTL{random.randint(1000,9999)}"

        # Ticket Window
        win = tk.Toplevel(self.root)
        win.title("🏨 Booking Confirmed")
        win.geometry("400x400")
        win.config(bg="#f7faff")

        tk.Label(win, text="✅ Room Booked Successfully!", font=("Helvetica", 18, "bold"),
                 fg="#009933", bg="#f7faff").pack(pady=15)
        info = f"Booking ID: {tid}\nHotel: {self.hotel.get()}\nCity: {self.city.get()}\nRoom: {self.room.get()}\nNights: {nights}\nTotal: ₹{total}"
        tk.Label(win, text=info, bg="#f7faff", font=("Arial", 13), justify="left").pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy, bg="#0047b3", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    HotelBookingApp(root)
    root.mainloop()
