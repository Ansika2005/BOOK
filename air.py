import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Static Data ---
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
airlines = ["Air India", "IndiGo", "Vistara", "SpiceJet", "GoAir", "Air Asia"]
classes = ["Economy", "Business", "First"]

# Generate flight_prices for all valid combos
flight_prices = {}
for s in cities:
    for d in cities:
        if s != d:
            for a in airlines:
                key = (s, d, a)
                distance_factor = abs(hash(f"{s}{d}{a}")) % 2000
                base_price = 3000 + distance_factor
                price = min(base_price, 7500)
                flight_prices[key] = price

# In-memory user database
users_db = {}


class AirlineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✈️ FlyAway Airline Booking")
        self.root.geometry("900x700")
        self.root.configure(bg="#e6f2ff")

        self.login_frame = None
        self.register_frame = None
        self.dashboard_frame = None
        self.booking_frame = None

        self.current_user = None
        self.create_login_frame()

    # Clear all frames
    def clear_all_frames(self):
        for f in (self.login_frame, self.register_frame, self.dashboard_frame, self.booking_frame):
            if f:
                f.destroy()

    # ---------------- LOGIN FRAME ----------------
    def create_login_frame(self):
        self.clear_all_frames()
        self.login_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.login_frame, text="✈️ FlyAway", font=("Helvetica", 28, "bold"),
                 bg="#e6f2ff", fg="#003366").pack(pady=40)
        tk.Label(self.login_frame, text="Username", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
        self.login_username = tk.Entry(self.login_frame, font=("Arial", 14), width=30)
        self.login_username.pack()
        tk.Label(self.login_frame, text="Password", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
        self.login_password = tk.Entry(self.login_frame, font=("Arial", 14), width=30, show="*")
        self.login_password.pack()
        tk.Button(self.login_frame, text="Login", font=("Arial", 14, "bold"),
                  bg="#0073e6", fg="white", width=20, command=self.login_user).pack(pady=20)
        link = tk.Label(self.login_frame, text="Register", fg="blue", bg="#e6f2ff",
                        cursor="hand2", font=("Arial", 12, "underline"))
        link.pack()
        link.bind("<Button-1>", lambda e: self.create_register_frame())

    def login_user(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Enter both username and password.")
            return
        if username in users_db and users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Welcome", f"Hello, {username}!")
            self.create_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    # ---------------- REGISTER FRAME ----------------
    def create_register_frame(self):
        self.clear_all_frames()
        self.register_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.register_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.register_frame, text="✈️ FlyAway - Register", font=("Helvetica", 24, "bold"),
                 bg="#e6f2ff", fg="#003366").pack(pady=30)
        tk.Label(self.register_frame, text="Username", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
        self.reg_username = tk.Entry(self.register_frame, font=("Arial", 14), width=30)
        self.reg_username.pack()
        tk.Label(self.register_frame, text="Password", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
        self.reg_password = tk.Entry(self.register_frame, font=("Arial", 14), width=30, show="*")
        self.reg_password.pack()
        tk.Label(self.register_frame, text="Confirm Password", font=("Arial", 14),
                 bg="#e6f2ff").pack(pady=5)
        self.reg_confirm = tk.Entry(self.register_frame, font=("Arial", 14), width=30, show="*")
        self.reg_confirm.pack()
        tk.Button(self.register_frame, text="Register", font=("Arial", 14, "bold"),
                  bg="#28a745", fg="white", width=20, command=self.register_user).pack(pady=20)
        link = tk.Label(self.register_frame, text="Login", fg="blue", bg="#e6f2ff",
                        cursor="hand2", font=("Arial", 12, "underline"))
        link.pack()
        link.bind("<Button-1>", lambda e: self.create_login_frame())

    def register_user(self):
        username = self.reg_username.get().strip()
        pw = self.reg_password.get().strip()
        cpw = self.reg_confirm.get().strip()
        if not username or not pw or not cpw:
            messagebox.showwarning("Input Error", "Fill all fields.")
            return
        if username in users_db:
            messagebox.showerror("Exists", "Username already exists.")
            return
        if pw != cpw:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        users_db[username] = pw
        messagebox.showinfo("Registered", "Registration successful! Please login.")
        self.create_login_frame()

    # ---------------- DASHBOARD FRAME ----------------
    def create_dashboard(self):
        self.clear_all_frames()
        self.root.title(f"FlyAway — {self.current_user}")
        self.dashboard_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self.dashboard_frame, bg="#003366", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"Welcome, {self.current_user}", font=("Helvetica", 20, "bold"),
                 bg="#003366", fg="white").pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(header, text="Logout", bg="#ff3333", fg="white", font=("Arial", 12, "bold"),
                  command=self.logout_to_login).pack(side=tk.RIGHT, padx=20, pady=20)

        # Search panel
        search_frame = tk.LabelFrame(self.dashboard_frame, text="Search Flights", bg="#e6f2ff",
                                     font=("Arial", 14, "bold"))
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="From:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
        self.dash_source = ttk.Combobox(search_frame, values=cities, state="readonly", width=15)
        self.dash_source.grid(row=0, column=1, padx=5, pady=5)
        self.dash_source.set("Select")

        tk.Label(search_frame, text="To:", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5)
        self.dash_dest = ttk.Combobox(search_frame, values=cities, state="readonly", width=15)
        self.dash_dest.grid(row=0, column=3, padx=5, pady=5)
        self.dash_dest.set("Select")

        tk.Label(search_frame, text="Airline:", bg="#e6f2ff").grid(row=0, column=4, padx=5, pady=5)
        self.dash_airline = ttk.Combobox(search_frame, values=["All"] + airlines, state="readonly", width=15)
        self.dash_airline.grid(row=0, column=5, padx=5, pady=5)
        self.dash_airline.set("All")

        tk.Label(search_frame, text="Class:", bg="#e6f2ff").grid(row=0, column=6, padx=5, pady=5)
        self.dash_class = ttk.Combobox(search_frame, values=["All"] + classes, state="readonly", width=15)
        self.dash_class.grid(row=0, column=7, padx=5, pady=5)
        self.dash_class.set("All")

        tk.Button(search_frame, text="Search", bg="#0073e6", fg="white", font=("Arial", 12, "bold"),
                  command=self.perform_search).grid(row=0, column=8, padx=10)

        # Result section
        result_frame = tk.Frame(self.dashboard_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        cols = ("Source", "Destination", "Airline", "Class", "Price")
        self.tree = ttk.Treeview(result_frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(self.dashboard_frame, text="Book Selected Flight", bg="#28a745", fg="white",
                  font=("Arial", 14, "bold"), command=self.open_booking_form).pack(pady=10)

        self.populate_flights()

    def logout_to_login(self):
        self.current_user = None
        self.create_login_frame()

    def populate_flights(self, filtered=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        data = filtered if filtered else []

        if not data:
            for key, price in flight_prices.items():
                s, d, a = key
                self.tree.insert("", tk.END, values=(s, d, a, "Economy", f"₹{price}"))
        else:
            # ✅ Fixed line
            for s, d, a, cl, price in data:
                self.tree.insert("", tk.END, values=(s, d, a, cl, f"₹{price}"))

    # ---------------- SEARCH FUNCTION ----------------
    def perform_search(self):
        s = self.dash_source.get()
        d = self.dash_dest.get()
        a = self.dash_airline.get()
        c = self.dash_class.get()

        if s == "Select" or d == "Select":
            messagebox.showwarning("Input Error", "Please select both source and destination.")
            return
        if s == d:
            messagebox.showerror("Invalid Route", "Source and destination cannot be the same.")
            return

        filtered = []
        for (src, dst, air), price in flight_prices.items():
            if src == s and dst == d:
                if a != "All" and air != a:
                    continue
                if c == "All":
                    for cl in classes:
                        mult = {"Economy": 1, "Business": 1.5, "First": 2}
                        price_cl = int(price * mult[cl])
                        filtered.append((src, dst, air, cl, price_cl))
                else:
                    mult = {"Economy": 1, "Business": 1.5, "First": 2}
                    price_cl = int(price * mult[c])
                    filtered.append((src, dst, air, c, price_cl))

        if not filtered:
            messagebox.showinfo("No Results", "No flights match your criteria.")
            self.populate_flights([])
        else:
            self.populate_flights(filtered)

    # ---------------- BOOKING FORM ----------------
    def open_booking_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a flight to book.")
            return

        flight_info = self.tree.item(selected[0])["values"]
        s, d, a, c, price_text = flight_info

        self.clear_all_frames()
        self.booking_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.booking_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.booking_frame, text="✈️ Flight Booking", font=("Helvetica", 24, "bold"),
                 bg="#e6f2ff", fg="#003366").pack(pady=20)

        form_frame = tk.Frame(self.booking_frame, bg="#e6f2ff")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name", font=("Arial", 14), bg="#e6f2ff").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_name = tk.Entry(form_frame, font=("Arial", 14), width=30); self.entry_name.grid(row=0, column=1, pady=5)
        tk.Label(form_frame, text="Age", font=("Arial", 14), bg="#e6f2ff").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_age = tk.Entry(form_frame, font=("Arial", 14), width=30); self.entry_age.grid(row=1, column=1, pady=5)
        tk.Label(form_frame, text="Gender", font=("Arial", 14), bg="#e6f2ff").grid(row=2, column=0, sticky="e", pady=5)
        self.gender_combo = ttk.Combobox(form_frame, values=["Male", "Female", "Other"],
                                         state="readonly", width=28)
        self.gender_combo.grid(row=2, column=1, pady=5)
        self.gender_combo.set("Male")

        tk.Label(form_frame, text="Price", font=("Arial", 14), bg="#e6f2ff").grid(row=3, column=0, sticky="e", pady=5)
        self.price_label = tk.Label(form_frame, text=price_text, font=("Arial", 14, "bold"),
                                    bg="#e6f2ff", fg="#333")
        self.price_label.grid(row=3, column=1, pady=5, sticky="w")

        tk.Button(self.booking_frame, text="Book Flight", font=("Arial", 16, "bold"),
                  bg="#28a745", fg="white", width=20, command=self.final_book).pack(pady=20)
        tk.Button(self.booking_frame, text="Back to Dashboard", font=("Arial", 12),
                  command=self.create_dashboard).pack()

    # ---------------- FINAL BOOKING ----------------
    def final_book(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        gender = self.gender_combo.get()
        price_text = self.price_label.cget("text")

        if not all([name, age, gender]):
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return
        try:
            age_n = int(age)
            if age_n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Age", "Enter valid age.")
            return

        ticket_id = f"FLY{random.randint(10000,99999)}"

        win = tk.Toplevel(self.root)
        win.title("✈️ Your Flight Ticket")
        win.geometry("450x400")
        win.configure(bg="#f9f9f9")

        tk.Label(win, text="✔️ Booking Confirmed!", font=("Helvetica", 18, "bold"),
                 fg="#28a745", bg="#f9f9f9").pack(pady=10)
        tk.Label(win, text=f"Ticket ID: {ticket_id}", font=("Arial", 14),
                 fg="#333", bg="#f9f9f9").pack(pady=5)

        info = f"Passenger: {name}\nAge: {age}\nGender: {gender}\nPrice: {price_text}"
        tk.Label(win, text=info, bg="#ffffff", bd=2, relief=tk.GROOVE,
                 font=("Arial", 12), justify="left").pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        tk.Button(win, text="Back to Dashboard", font=("Arial", 12, "bold"),
                  bg="#0073e6", fg="white", command=lambda: [win.destroy(), self.create_dashboard()]).pack(pady=10)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineApp(root)
    root.mainloop()
