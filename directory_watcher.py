import os
from telegram.error import TelegramError

# Global variable to store previously seen files
previous_files = set()

def get_files(directory):
    file_list = []
    allowed_extensions = ('.stl', '.zzn', '.obj', '.pdf')
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(allowed_extensions):
                file_path = os.path.join(root, file)
                creation_time = os.path.getctime(file_path)
                file_list.append((os.path.relpath(file_path, start=directory), creation_time))
    return file_list

def get_current_files(directory):
    current_files = set()
    allowed_extensions = ('.stl', '.zzn', '.obj', '.pdf')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(allowed_extensions):
                file_relative_path = os.path.relpath(os.path.join(root, file), start=directory)
                current_files.add(file_relative_path)
    return sorted(current_files)

async def check_directory_task(bot, chat_id, directory):
    global previous_files
    current_files = get_current_files(directory)

    # Check for new files
    new_files = [file for file in current_files if file not in previous_files]

    if new_files:
        message_chunks = [list(new_files)[i:i + 5] for i in range(0, len(new_files), 5)]
        for chunk in message_chunks:
            message = "New files added: "
            for file in chunk:
                message += f"\n<pre> <code> {file} </code> </pre>"
            try:
                await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
            except TelegramError as e:
                print(e)

    previous_files = current_files
