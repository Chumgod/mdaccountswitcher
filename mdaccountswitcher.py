import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class AccountProfileGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MD Account Switcher")

        # Create labels and entry fields for user input
        self.username_label = tk.Label(self.master, text="Username")
        self.username_label.pack(fill='x', expand=True)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(fill='x', expand=True)

        self.password_label = tk.Label(self.master, text="Password")
        self.password_label.pack(fill='x', expand=True)
        self.password_entry = tk.Entry(self.master)
        self.password_entry.pack(fill='x', expand=True)

        self.useragent_label = tk.Label(self.master, text="Useragent")
        self.useragent_label.pack(fill='x', expand=True)
        self.useragent_entry = tk.Entry(self.master)
        self.useragent_entry.pack(fill='x', expand=True)

        self.nickname_label = tk.Label(self.master, text="Nickname")
        self.nickname_label.pack(fill='x', expand=True)
        self.nickname_entry = tk.Entry(self.master)
        self.nickname_entry.pack(fill='x', expand=True)

        # Create buttons for saving, clearing, and deleting/loading profiles

        self.save_button = tk.Button(self.master, text="Save", command=self.save_profile)
        self.save_button.pack(side='left', fill='x', expand=True)

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_input)
        self.clear_button.pack(side='left', fill='x', expand=True)

        self.load_button = tk.Button(self.master, text="Load", command=self.load_profile)
        self.load_button.pack(side='left', fill='x', expand=True)

        self.delete_button = tk.Button(self.master, text="Delete", command=self.delete_profile)
        self.delete_button.pack(side='left', fill='x', expand=True)

        # Read account profiles from file
        with open('account_profiles.txt', 'r') as f:
            string_list = f.read().splitlines()

        # Create a Combobox widget and populate it with the first string of each line
        self.combo = ttk.Combobox(self.master, values=[s.split(',')[0] for s in string_list])
        self.combo.pack(side='left', fill='x', expand=True)
        self.combo.bind('<FocusIn>', self.repopulate_combobox)
        self.combo.bind('<Button-1>', self.repopulate_combobox)

        # Create output box for displaying saved profiles
        self.output_box = tk.Text(self.master, height=1, width=50)
        self.output_box.pack(fill='x', expand=True)

    def delete_profile(self):
        # Get the selected string from the Combobox
        selected_string = self.combo.get()

        # Read account profiles from file
        with open('account_profiles.txt', 'r') as f:
            string_list = f.read().splitlines()

        # Find the full string in the list
        full_string = [s for s in string_list if s.startswith(selected_string)][0]

        # Remove the full string from the list
        string_list.remove(full_string)

        # Write the list back to the file
        with open('account_profiles.txt', 'w') as f:
            for item in string_list:
                f.write(f'{item}\n')

    def repopulate_combobox(self, event):
        # Repopulate the combobox options whenever the combobox is clicked on
        with open('account_profiles.txt', 'r') as f:
            string_list = f.read().splitlines()
        self.combo['values'] = [s.split(',')[0] for s in string_list]

    def save_profile(self):
        # Get user input from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()
        useragent = self.useragent_entry.get()
        nickname = self.nickname_entry.get()

        # Check if any fields are empty
        if not username or not password or not useragent or not nickname:
            messagebox.showwarning("Warning", "All fields are required!")
        else:
            # Save user input to a file
            with open("account_profiles.txt", "a") as file:
                file.write(f"{nickname},{username},{password},{useragent}\n")

            # Clear input fields and show success message
            self.clear_input()
            messagebox.showinfo("Success", "Profile saved successfully!")
            with open('account_profiles.txt', 'r') as f:
                string_list = f.read().splitlines()

    def clear_input(self):
        # Clear input fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.useragent_entry.delete(0, tk.END)
        self.nickname_entry.delete(0, tk.END)

    def load_profile(self):
        # Clear the output box
        self.output_box.delete("1.0", tk.END)

        with open('account_profiles.txt', 'r') as f:
            string_list = f.read().splitlines()

        # Get the selected string from the Combobox
        selected_string = self.combo.get()

        # Find the full string in the list
        full_string = [s for s in string_list if s.startswith(selected_string)][0]

        # Extract the second and third strings from the full string
        parts = full_string.split(',')
        output_text = f'{parts[1]} : {parts[2]}'

        # Insert the formatted string into the output box
        self.output_box.insert(tk.END, output_text)

        # Get the fourth string in the full string
        folder_name = full_string.split(',')[3]

        # Rename the LocalData folder
        try:
            with open('config.txt', 'r') as z:
                path = z.read()
            old_path = next(entry for entry in os.scandir(path) if entry.is_dir())
            new_path = os.path.join(os.path.dirname(old_path), folder_name)
            shutil.move(old_path, new_path)
        except Exception as e:
            print(f'Error renaming folder: {e}')

    def clear_output(self):
        # Clear the output box
        self.output_box.delete("1.0", tk.END)


if __name__ == "__main__":
    # Create the root window and run the GUI application
    root = tk.Tk()
    root.geometry("600x200")
    app = AccountProfileGUI(root)
    root.mainloop()
