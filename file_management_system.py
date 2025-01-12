import os
import shutil
from tkinter import Tk, filedialog, StringVar, Frame, Button, Label, Entry, Listbox, END, DISABLED, NORMAL
from tkinter.ttk import Treeview
from pathlib import Path
from datetime import datetime

class FileManagementSystemGUI:
    def __init__(self, master):
        """
        Initialize the File Management System with GUI.
        :param master: The root Tkinter window.
        """
        self.master = master
        self.master.title("File Management System")
        self.master.geometry("1000x700")
        self.current_path = StringVar(value="")
        self.is_path_set = False

        # Frame for path and navigation
        path_frame = Frame(master)
        path_frame.pack(fill="x")

        Label(path_frame, text="Current Path:").pack(side="left")
        self.path_entry = Entry(path_frame, textvariable=self.current_path, width=60)
        self.path_entry.pack(side="left", padx=5)

        Button(path_frame, text="Browse", command=self.browse_directory).pack(side="left")
        self.reset_browse_button = Button(path_frame, text="X", command=self.reset_browse, state=DISABLED, fg="red")
        self.reset_browse_button.pack(side="left")

        Button(path_frame, text="Logs", command=self.show_logs).pack(side="left")

        # File/Folder Actions Frame
        self.actions_frame = Frame(master)
        self.actions_frame.pack(fill="x", pady=10)

        self.create_folder_button = Button(self.actions_frame, text="Create Folder", command=self.select_command(self.create_folder), state=DISABLED)
        self.create_folder_button.pack(side="left", padx=5)
        self.delete_folder_button = Button(self.actions_frame, text="Delete Folder", command=self.select_command(self.delete_folder), state=DISABLED)
        self.delete_folder_button.pack(side="left", padx=5)
        self.rename_folder_button = Button(self.actions_frame, text="Rename Folder", command=self.select_command(self.rename_folder), state=DISABLED)
        self.rename_folder_button.pack(side="left", padx=5)
        self.create_file_button = Button(self.actions_frame, text="Create File", command=self.select_command(self.create_file), state=DISABLED)
        self.create_file_button.pack(side="left", padx=5)
        self.delete_file_button = Button(self.actions_frame, text="Delete File", command=self.select_command(self.delete_file), state=DISABLED)
        self.delete_file_button.pack(side="left", padx=5)
        self.rename_file_button = Button(self.actions_frame, text="Rename File", command=self.select_command(self.rename_file), state=DISABLED)
        self.rename_file_button.pack(side="left", padx=5)

        self.reset_command_button = Button(self.actions_frame, text="X", command=self.reset_command, state=DISABLED, fg="red")
        self.reset_command_button.pack(side="left", padx=5)

        # Treeview for directory structure
        self.tree = Treeview(master)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("#0", text="Directory Structure", anchor="w")
        self.populate_tree()

        # Input Panel below the Treeview
        self.input_frame = Frame(master)

        self.input_label_1 = Label(self.input_frame, text="Current Name:")
        self.input_entry_1 = Entry(self.input_frame, width=30)
        self.input_label_2 = Label(self.input_frame, text="New Name:")
        self.input_entry_2 = Entry(self.input_frame, width=30)
        self.submit_button = Button(self.input_frame, text="Submit", command=self.handle_input)

        self.input_frame.pack_forget()  # Initially hide the input panel

        self.active_command = None
        self.using_double_input = False

        # Log Panel
        self.log_frame = Frame(master)
        self.log_listbox = Listbox(self.log_frame, height=15)
        Button(self.log_frame, text="Back", command=self.hide_logs).pack(side="top", anchor="w")
        Label(self.log_frame, text="Logs:").pack(anchor="w")
        self.log_listbox.pack(fill="both", expand=True)

        # Footer
        Label(master, text="AZD", fg="gray").pack(side="bottom")

    def log(self, message, level="info"):
        """Log a message in the log panel."""
        self.log_listbox.insert(END, f"[{level.upper()}] {message}")
        self.log_listbox.see(END)

    def browse_directory(self):
        """Open a dialog to select a directory."""
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.current_path.set(selected_directory)
            self.is_path_set = True
            self.enable_buttons()
            self.populate_tree()
            self.reset_browse_button.config(state=NORMAL)
            self.log(f"Changed directory to {selected_directory}")

    def reset_browse(self):
        """Reset the browse selection and go back to the initial state."""
        self.reset_command()  # Reset any active command
        self.current_path.set("")
        self.is_path_set = False
        self.disable_buttons()
        self.populate_tree()
        self.reset_browse_button.config(state=DISABLED)
        self.log("Reset directory selection.")

    def reset_command(self):
        """Reset the current command selection and input fields."""
        self.active_command = None
        self.using_double_input = False
        self.input_entry_1.delete(0, END)
        self.input_entry_2.delete(0, END)
        self.input_frame.pack_forget()
        self.enable_buttons()
        self.reset_command_button.config(state=DISABLED)
        self.log("Reset command selection.")

    def enable_buttons(self):
        """Enable action buttons when a directory is selected."""
        self.create_folder_button.config(state=NORMAL)
        self.delete_folder_button.config(state=NORMAL)
        self.rename_folder_button.config(state=NORMAL)
        self.create_file_button.config(state=NORMAL)
        self.delete_file_button.config(state=NORMAL)
        self.rename_file_button.config(state=NORMAL)

    def disable_buttons(self):
        """Disable action buttons when no directory is selected."""
        self.create_folder_button.config(state=DISABLED)
        self.delete_folder_button.config(state=DISABLED)
        self.rename_folder_button.config(state=DISABLED)
        self.create_file_button.config(state=DISABLED)
        self.delete_file_button.config(state=DISABLED)
        self.rename_file_button.config(state=DISABLED)

    def populate_tree(self):
        """Populate the tree view with the directory structure."""
        self.tree.delete(*self.tree.get_children())
        root_path = self.current_path.get()
        if root_path:
            for item in os.listdir(root_path):
                item_path = os.path.join(root_path, item)
                if os.path.isdir(item_path):
                    self.tree.insert("", END, text=item, values=[item_path])
                elif os.path.isfile(item_path):
                    self.tree.insert("", END, text=item, values=[item_path])

    def select_command(self, func):
        """Wrap a command to handle selection and disable other buttons."""
        def wrapper():
            self.active_command = func
            self.input_entry_1.delete(0, END)
            self.input_entry_2.delete(0, END)

            # Ensure consistent order for rename inputs
            self.input_label_1.pack_forget()
            self.input_entry_1.pack_forget()
            self.input_label_2.pack_forget()
            self.input_entry_2.pack_forget()
            self.submit_button.pack_forget()

            self.input_frame.pack(fill="x", pady=10)  # Show input panel

            if func == self.rename_file or func == self.rename_folder:
                self.using_double_input = True
                self.input_label_1.config(text="Current Name:")
                self.input_label_1.pack(side="left", padx=5)
                self.input_entry_1.pack(side="left", padx=5)
                self.input_label_2.config(text="New Name:")
                self.input_label_2.pack(side="left", padx=5)
                self.input_entry_2.pack(side="left", padx=5)
            else:
                self.using_double_input = False
                self.input_label_1.config(text="Enter Input:")
                self.input_label_1.pack(side="left", padx=5)
                self.input_entry_1.pack(side="left", padx=5)
            self.submit_button.pack(side="left", padx=5)

            # Disable all other buttons and enable reset button
            self.disable_buttons()
            self.reset_command_button.config(state=NORMAL)
        return wrapper

    def handle_input(self):
        """Handle input from the input entry field."""
        if self.active_command:
            input_value_1 = self.input_entry_1.get()
            input_value_2 = self.input_entry_2.get() if self.using_double_input else None
            if self.using_double_input:
                self.active_command(input_value_1, input_value_2)
            else:
                self.active_command(input_value_1)
            self.reset_command()  # Reset after handling input

    def create_folder(self, folder_name):
        """Create a new folder in the current directory."""
        if folder_name:
            new_path = os.path.join(self.current_path.get(), folder_name)
            try:
                os.makedirs(new_path)
                self.log(f"Folder created: {new_path}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to create folder: {e}", "error")

    def delete_folder(self, folder_name):
        """Delete a selected folder."""
        if folder_name:
            target_path = os.path.join(self.current_path.get(), folder_name)
            try:
                shutil.rmtree(target_path)
                self.log(f"Folder deleted: {target_path}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to delete folder: {e}", "error")

    def rename_folder(self, old_name, new_name):
        """Rename a selected folder."""
        if old_name and new_name:
            old_path = os.path.join(self.current_path.get(), old_name)
            new_path = os.path.join(self.current_path.get(), new_name)
            try:
                os.rename(old_path, new_path)
                self.log(f"Folder renamed from {old_name} to {new_name}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to rename folder: {e}", "error")

    def create_file(self, file_name):
        """Create a new file in the current directory."""
        if file_name:
            new_path = os.path.join(self.current_path.get(), file_name)
            try:
                with open(new_path, 'w') as f:
                    f.write("")
                self.log(f"File created: {new_path}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to create file: {e}", "error")

    def delete_file(self, file_name):
        """Delete a selected file."""
        if file_name:
            target_path = os.path.join(self.current_path.get(), file_name)
            try:
                os.remove(target_path)
                self.log(f"File deleted: {target_path}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to delete file: {e}", "error")

    def rename_file(self, old_name, new_name):
        """Rename a selected file."""
        if old_name and new_name:
            old_path = os.path.join(self.current_path.get(), old_name)
            new_path = os.path.join(self.current_path.get(), new_name)
            try:
                os.rename(old_path, new_path)
                self.log(f"File renamed from {old_name} to {new_name}")
                self.populate_tree()
            except Exception as e:
                self.log(f"Failed to rename file: {e}", "error")

    def show_logs(self):
        """Show the logs panel."""
        self.actions_frame.pack_forget()
        self.tree.pack_forget()
        self.input_frame.pack_forget()
        self.log_frame.pack(fill="both", expand=True)

    def hide_logs(self):
        """Hide the logs panel and go back to the main view."""
        self.log_frame.pack_forget()
        self.actions_frame.pack(fill="x", pady=10)
        self.tree.pack(fill="both", expand=True)

# Main application entry
if __name__ == "__main__":
    root = Tk()
    app = FileManagementSystemGUI(root)
    root.mainloop()
