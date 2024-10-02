# Import necessary modules
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import yaml
import subprocess
import csv
from datetime import datetime
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AMMInfo, AccountLines
from xrpl.utils import drops_to_xrp

class AirdropGUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Airdrop Tool GUI")
        self.root.geometry("1000x800")  # Adjusted window size for better readability

        # Initialize variables
        self.pool_address = "rkXhTduDBANLFXHqEg4obsoCepHVXj3qa"
        self.lp_token_holders_data = []

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Configuration Frame
        config_frame = tk.LabelFrame(self.root, text="Configuration")
        config_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # Config File Path
        tk.Label(config_frame, text="Config File:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.config_path_var = tk.StringVar()
        self.config_entry = tk.Entry(config_frame, textvariable=self.config_path_var, width=50)
        self.config_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(config_frame, text="Browse", command=self.browse_config).grid(row=0, column=2, padx=5, pady=5)

        # Issuer Address
        tk.Label(config_frame, text="Issuer Address:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.issuer_var = tk.StringVar()
        self.issuer_entry = tk.Entry(config_frame, textvariable=self.issuer_var, width=50)
        self.issuer_entry.grid(row=1, column=1, padx=5, pady=5)

        # Secret Key
        tk.Label(config_frame, text="Secret Key:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.secret_var = tk.StringVar()
        self.secret_entry = tk.Entry(config_frame, textvariable=self.secret_var, width=50, show="*")
        self.secret_entry.grid(row=2, column=1, padx=5, pady=5)

        # Network Selection
        tk.Label(config_frame, text="Network:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.network_var = tk.StringVar(value="mainnet")
        network_options = ["mainnet", "testnet", "devnet"]
        self.network_menu = tk.OptionMenu(config_frame, self.network_var, *network_options)
        self.network_menu.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Airdrop Amount
        tk.Label(config_frame, text="Total Airdrop Amount:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(config_frame, textvariable=self.amount_var, width=20)
        self.amount_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Token Currency
        tk.Label(config_frame, text="Token Currency:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.currency_var = tk.StringVar()
        self.currency_entry = tk.Entry(config_frame, textvariable=self.currency_var, width=20)
        self.currency_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Snapshot Date
        tk.Label(config_frame, text="Snapshot Date (YYYY-MM-DD):").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.snapshot_var = tk.StringVar()
        self.snapshot_entry = tk.Entry(config_frame, textvariable=self.snapshot_var, width=20)
        self.snapshot_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # AMM Pool Address
        tk.Label(config_frame, text="AMM Pool Address:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.amm_address_var = tk.StringVar(value=self.pool_address)
        self.amm_address_entry = tk.Entry(config_frame, textvariable=self.amm_address_var, width=50)
        self.amm_address_entry.grid(row=7, column=1, padx=5, pady=5)

        # Save and Load Config Buttons
        config_buttons_frame = tk.Frame(config_frame)
        config_buttons_frame.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        tk.Button(config_buttons_frame, text="Load Config", command=self.load_config).pack(side="left", padx=5)
        tk.Button(config_buttons_frame, text="Save Config", command=self.save_config).pack(side="left", padx=5)

        # Action Buttons Frame
        actions_frame = tk.LabelFrame(self.root, text="Actions")
        actions_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.root.grid_rowconfigure(1, weight=0)

        tk.Button(actions_frame, text="Update Pool Info", command=self.update_ui).pack(side="left", padx=10, pady=10)
        tk.Button(actions_frame, text="Calculate Airdrop", command=self.run_calculate_airdrop).pack(side="left", padx=10, pady=10)
        tk.Button(actions_frame, text="Distribute Airdrop", command=self.run_distribute_airdrop).pack(side="left", padx=10, pady=10)
        tk.Button(actions_frame, text="Save as CSV", command=self.export_to_csv).pack(side="left", padx=10, pady=10)

        # PanedWindow to hold the Log Output and LP Token Holders
        paned_window = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        paned_window.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        self.root.grid_rowconfigure(2, weight=1)

        # Log Output Frame
        log_frame = tk.LabelFrame(paned_window, text="Log Output")
        paned_window.add(log_frame, height=200)  # Set initial height

        self.log_text = tk.Text(log_frame, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # LP Token Holders Frame (scrollable)
        lp_frame = tk.LabelFrame(paned_window, text="LP Token Holders")
        paned_window.add(lp_frame, stretch='always')

        # Canvas and scrollbar
        self.canvas = tk.Canvas(lp_frame, borderwidth=0, background="#f0f0f0")
        self.scrollable_frame = tk.Frame(self.canvas, background="#f0f0f0")
        self.vsb = tk.Scrollbar(lp_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Initialize holders frame
        self.holders_frame_instance = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        self.holders_frame_instance.pack(fill=tk.BOTH, expand=True)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Method to browse for configuration file
    def browse_config(self):
        filepath = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=[("YAML Files", "*.yaml"), ("All Files", "*.*")]
        )
        if filepath:
            self.config_path_var.set(filepath)
            self.load_config(filepath)

    # Method to load configuration from file
    def load_config(self, filepath=None):
        if not filepath:
            filepath = self.config_path_var.get()
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "Configuration file not found.")
            return
        try:
            with open(filepath, 'r') as file:
                config = yaml.safe_load(file)
            # Update UI fields with loaded configuration
            self.issuer_var.set(config.get('issuer_address', ''))
            self.secret_var.set(config.get('secret_key', ''))
            self.network_var.set(config.get('network', 'mainnet'))
            self.amount_var.set(str(config.get('total_airdrop_amount', '')))
            self.currency_var.set(config.get('token_currency', ''))
            self.snapshot_var.set(config.get('snapshot_date', ''))
            self.amm_address_var.set(config.get('amm_address', ''))
            self.append_log(f"Configuration loaded from {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")

    # Method to save configuration to file
    def save_config(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML Files", "*.yaml"), ("All Files", "*.*")]
        )
        if filepath:
            config = {
                'issuer_address': self.issuer_var.get(),
                'secret_key': self.secret_var.get(),
                'network': self.network_var.get(),
                'total_airdrop_amount': float(self.amount_var.get() or 0),
                'token_currency': self.currency_var.get(),
                'snapshot_date': self.snapshot_var.get(),
                'amm_address': self.amm_address_var.get(),
            }
            try:
                with open(filepath, 'w') as file:
                    yaml.dump(config, file)
                self.config_path_var.set(filepath)
                self.append_log(f"Configuration saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")

    # Method to append messages to the log output
    def append_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    # Function to format numbers in an abbreviated way (e.g., 1M, 2.5K)
    def format_abbreviated_value(self, number):
        try:
            number = float(number)
        except (ValueError, TypeError):
            return "Invalid"

        if number >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.1f}K"
        else:
            return f"{number:.6f}"

    # Function to get AMM Pool info
    def get_amm_poz_xrp_info(self, amm_address):
        try:
            client = JsonRpcClient("https://s1.ripple.com:51234/")
            request = AMMInfo(amm_account=amm_address)
            response = client.request(request)
            amm_data = response.result['amm']

            # Parse and format data
            poz_balance = float(amm_data['amount2']['value'])
            xrp_balance = float(drops_to_xrp(amm_data['amount']))
            lp_token_balance = float(amm_data['lp_token']['value'])

            print(f"Fetched AMM Info - POZ: {poz_balance}, XRP: {xrp_balance}, LP Tokens: {lp_token_balance}")
            return poz_balance, xrp_balance, lp_token_balance
        except Exception as e:
            print(f"Error fetching POZ/XRP reserves: {e}")
            messagebox.showerror("Error", f"Failed to fetch POZ/XRP reserves:\n{e}")
            return None, None, None

    # Function to fetch LP token holders for the pool
    def get_lp_token_holders(self, pool_address):
        try:
            client = JsonRpcClient("https://s1.ripple.com:51234/")
            results = []
            marker = None

            while True:
                request = AccountLines(account=pool_address, marker=marker)
                response = client.request(request)
                lines = response.result.get('lines', [])
                if not lines:
                    break
                results.extend(lines)
                marker = response.result.get('marker')
                if not marker:
                    break

            # Extract relevant data and sort by LP Tokens in descending order
            holders = []
            for line in results:
                try:
                    account = line['account']
                    currency = line['currency']
                    balance = float(line['balance'])

                    # Exclude the pool address itself from the holders list
                    if account.lower() == pool_address.lower():
                        continue

                    holders.append({
                        "Account": account,
                        "Currency": currency,
                        "LP Tokens": abs(balance)  # Convert to absolute value
                    })
                except (KeyError, ValueError) as e:
                    print(f"Skipping a line due to error: {e}")
                    continue  # Skip lines with missing or invalid data

            holders = sorted(holders, key=lambda x: x['LP Tokens'], reverse=True)  # Sort by LP Tokens in descending order
            print(f"Total LP Token Holders Fetched: {len(holders)}")  # Debugging statement
            return holders
        except Exception as e:
            print(f"Error fetching LP token holders: {e}")
            messagebox.showerror("Error", f"Failed to fetch LP token holders:\n{e}")
            return []

    # Function to update the UI with fetched data
    def update_ui(self):
        threading.Thread(target=self.fetch_and_update_ui).start()

    def fetch_and_update_ui(self):
        # Disable buttons to prevent multiple clicks
        # self.update_button.config(state='disabled')  # Uncomment if you add update_button
        # self.export_button.config(state='disabled')  # Uncomment if you add export_button

        # Clear existing holders_frame_instance if it exists to refresh data
        if hasattr(self, 'holders_frame_instance') and self.holders_frame_instance.winfo_exists():
            self.holders_frame_instance.destroy()

        # Fetch LP token holders
        amm_address = self.amm_address_var.get()
        lp_token_holders = self.get_lp_token_holders(amm_address)

        if not lp_token_holders:
            messagebox.showinfo("No Data", "No LP token holders found.")
            return

        # Calculate total LP tokens for percentage calculation
        total_lp_tokens = sum(holder['LP Tokens'] for holder in lp_token_holders)

        if total_lp_tokens == 0:
            messagebox.showinfo("No Data", "Total LP Tokens is zero. Cannot calculate percentages.")
            return

        # Update the holders_frame
        self.create_holders_frame()
        holders_frame = self.holders_frame_instance

        # Initialize data storage for CSV export
        self.lp_token_holders_data = []

        # Display each holder in the holders_frame
        for holder in lp_token_holders:
            holder_frame = tk.Frame(holders_frame, pady=5, padx=5, bd=1, relief=tk.RIDGE, bg="#ffffff")
            holder_frame.pack(fill=tk.X, padx=5, pady=2)

            # Full Account Address
            account_label = tk.Label(holder_frame, text=holder['Account'], font=("Arial", 12, "bold"), bg="#ffffff", wraplength=900, justify="left")
            account_label.pack(anchor="w")

            # Percentage of Total LP Tokens
            percentage = (holder['LP Tokens'] / total_lp_tokens) * 100 if total_lp_tokens > 0 else 0
            percentage_label = tk.Label(holder_frame, text=f"Percentage: {percentage:.6f}%", font=("Arial", 10), fg="blue", bg="#ffffff")
            percentage_label.pack(anchor="w")

            # Abbreviated LP Token Amount
            abbreviated_lp = self.format_abbreviated_value(holder['LP Tokens'])
            lp_label_holder = tk.Label(holder_frame, text=f"LP Tokens: {abbreviated_lp}", font=("Arial", 10), fg="green", bg="#ffffff")
            lp_label_holder.pack(anchor="w")

            # Store data for CSV export
            holder['Percentage'] = f"{percentage:.6f}%"
            holder['Abbreviated LP Tokens'] = abbreviated_lp
            self.lp_token_holders_data.append(holder)

        # Re-enable buttons after updating
        # self.update_button.config(state='normal')  # Uncomment if you add update_button
        # self.export_button.config(state='normal')  # Uncomment if you add export_button

    # Function to create the holders frame (scrollable)
    def create_holders_frame(self):
        if hasattr(self, 'holders_frame_instance') and self.holders_frame_instance.winfo_exists():
            self.holders_frame_instance.destroy()
        self.holders_frame_instance = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        self.holders_frame_instance.pack(fill=tk.BOTH, expand=True)

    # Function to export data to CSV
    def export_to_csv(self):
        # Get all holder data
        if not self.lp_token_holders_data:
            messagebox.showinfo("No Data", "There is no data to export.")
            return

        # Prompt user to select file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save as"
        )
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write headers
                writer.writerow(["Account", "Currency", "LP Tokens", "Percentage"])
                # Write data
                for holder in self.lp_token_holders_data:
                    writer.writerow([
                        holder['Account'],
                        holder['Currency'],
                        holder['LP Tokens'],
                        holder['Percentage']
                    ])
            messagebox.showinfo("Success", f"Data successfully exported to {file_path}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            messagebox.showerror("Error", f"Failed to export data to CSV:\n{e}")

    # Method to run the airdrop calculation
    def run_calculate_airdrop(self):
        threading.Thread(target=self.calculate_airdrop).start()

    # Method to calculate airdrop allocations
    def calculate_airdrop(self):
        try:
            total_airdrop_amount = float(self.amount_var.get())
            if total_airdrop_amount <= 0:
                messagebox.showerror("Error", "Total airdrop amount must be greater than zero.")
                return

            if not self.lp_token_holders_data:
                messagebox.showerror("Error", "No LP token holders data available. Please update pool info first.")
                return

            total_lp_tokens = sum(holder['LP Tokens'] for holder in self.lp_token_holders_data)

            if total_lp_tokens == 0:
                messagebox.showerror("Error", "Total LP Tokens is zero. Cannot calculate airdrop.")
                return

            # Calculate airdrop allocations
            for holder in self.lp_token_holders_data:
                holder['Airdrop Amount'] = (holder['LP Tokens'] / total_lp_tokens) * total_airdrop_amount

            # Save allocations to a CSV file
            file_path = "airdrop_allocations.csv"
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Account", "LP Tokens", "Percentage", "Airdrop Amount"])
                for holder in self.lp_token_holders_data:
                    writer.writerow([
                        holder['Account'],
                        holder['LP Tokens'],
                        holder['Percentage'],
                        holder['Airdrop Amount']
                    ])

            self.append_log(f"Airdrop calculations completed. Allocations saved to {file_path}")
            messagebox.showinfo("Success", f"Airdrop allocations saved to {file_path}")
        except Exception as e:
            self.append_log(f"Error calculating airdrop: {e}")
            messagebox.showerror("Error", f"Failed to calculate airdrop:\n{e}")

    # Method to run the airdrop distribution
    def run_distribute_airdrop(self):
        threading.Thread(target=self.distribute_airdrop).start()

    # Method to distribute the airdrop
    def distribute_airdrop(self):
        try:
            # Ensure airdrop allocations are available
            allocations_file = "airdrop_allocations.csv"
            if not os.path.exists(allocations_file):
                messagebox.showerror("Error", "Airdrop allocations file not found. Please run calculations first.")
                return

            # Load allocations
            with open(allocations_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                allocations = list(reader)

            # Simulate distribution (Replace this with actual XRPL transactions)
            for allocation in allocations:
                account = allocation['Account']
                amount = float(allocation['Airdrop Amount'])
                self.append_log(f"Distributing {amount} {self.currency_var.get()} to {account}")
                # Here you would create and submit the transaction to the XRPL

            self.append_log("Airdrop distribution completed.")
            messagebox.showinfo("Success", "Airdrop distribution simulated. Check logs for details.")
        except Exception as e:
            self.append_log(f"Error distributing airdrop: {e}")
            messagebox.showerror("Error", f"Failed to distribute airdrop:\n{e}")

    # Additional methods can be added here if needed

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    # Instantiate the AirdropGUI class with the root window
    app = AirdropGUI(root)
    # Run the main event loop
    root.mainloop()
