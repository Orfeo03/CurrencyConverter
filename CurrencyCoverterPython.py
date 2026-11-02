
import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "https://api.frankfurter.dev/v2/rate/{}/{}"
CURRENCIES = ["EUR", "USD", "GBP", "ALL"]


def convert():
    try:
        amount = float(amount_entry.get())

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        from_currency = from_var.get()
        to_currency = to_var.get()

        if from_currency == to_currency:
            rate = 1
            date = "Same currency"
        else:
            url = API_URL.format(from_currency, to_currency)
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            rate = float(data["rate"])
            date = data.get("date", "N/A")

        result = amount * rate

        result_label.config(
            text=f"{result:,.2f} {to_currency}"
        )
        rate_label.config(
            text=f"1 {from_currency} = {rate:.4f} {to_currency}"
        )
        date_label.config(text=f"Rate date: {date}")

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid positive number."
        )
    except requests.RequestException:
        messagebox.showerror(
            "Connection Error",
            "Could not retrieve exchange rates."
        )


def swap():
    current_from = from_var.get()
    from_var.set(to_var.get())
    to_var.set(current_from)
    convert()


root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x400")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Currency Converter",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

tk.Label(root, text="Enter Amount:").pack()

amount_entry = tk.Entry(
    root,
    font=("Arial", 14),
    justify="center"
)
amount_entry.pack(pady=10)
amount_entry.insert(0, "100")

from_var = tk.StringVar(value="EUR")
to_var = tk.StringVar(value="ALL")

tk.Label(root, text="From:").pack()
from_menu = ttk.Combobox(
    root,
    textvariable=from_var,
    values=CURRENCIES,
    state="readonly"
)
from_menu.pack(pady=5)

tk.Button(
    root,
    text="Swap ⇅",
    command=swap
).pack(pady=10)

tk.Label(root, text="To:").pack()
to_menu = ttk.Combobox(
    root,
    textvariable=to_var,
    values=CURRENCIES,
    state="readonly"
)
to_menu.pack(pady=5)

tk.Button(
    root,
    text="Convert",
    command=convert,
    font=("Arial", 12)
).pack(pady=15)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold")
)
result_label.pack()

rate_label = tk.Label(root, text="")
rate_label.pack(pady=5)

date_label = tk.Label(root, text="")
date_label.pack()

root.bind("<Return>", lambda event: convert())

root.mainloop()
