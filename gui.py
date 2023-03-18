import tkinter as tk
import time
from tkinter import ttk
from directory_watcher import get_files
from telegram_bot import start_bot, stop_bot, DIRECTORY

def auto_refresh(file_list, directory, interval=1000):
    update_file_list(file_list, directory)
    file_list.after(interval, auto_refresh, file_list, directory)

def update_file_list(file_list, directory):
    files = sorted(get_files(directory), key=lambda x: x[0].lower())
    file_list.delete(0, tk.END)
    listbox_width = file_list.winfo_width() // file_list.winfo_reqwidth()  # Calculate the listbox width dynamically
    for file, creation_time in files:
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
        padded_file = file.ljust(listbox_width - len(formatted_time) - 3)  # Padding file path with spaces
        file_list.insert(tk.END, f"{padded_file} | {formatted_time}")

def main():
    global root
    root = tk.Tk()
    root.title("Atlas Telegram Bot")
    root.geometry("800x600")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    list_label = ttk.Label(main_frame, text="Current Files:")
    list_label.pack(anchor=tk.W)

    file_list = tk.Listbox(main_frame)
    file_list.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(file_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=file_list.yview)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)

    refresh_button = ttk.Button(button_frame, text="Refresh", command=lambda: update_file_list(file_list, DIRECTORY))
    refresh_button.pack(side=tk.LEFT)

    status_var = tk.StringVar()
    status_var.set("Bot stopped")

    start_button = ttk.Button(button_frame, text="Start", command=lambda: start_bot(status_var))
    start_button.pack(side="left")

    stop_button = ttk.Button(button_frame, text="Stop", command=lambda: stop_bot(status_var))
    stop_button.pack(side="left")

    # Status bar
    status_bar = ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w")
    status_bar.pack(side="bottom", fill="x")


    update_file_list(file_list, DIRECTORY)
    auto_refresh(file_list, DIRECTORY)

    root.mainloop()

if __name__ == '__main__':
    main()
