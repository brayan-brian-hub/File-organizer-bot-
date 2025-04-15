import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time

WATCHED_FOLDER = os.path.expanduser("~/Desktop")
DEST_FOLDER = os.path.join(WATCHED_FOLDER, "Organized")

FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Others': []
}

# Create folders
for folder in FILE_TYPES.keys():
    os.makedirs(os.path.join(DEST_FOLDER, folder), exist_ok=True)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            moved = False
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    new_filename = f"{timestamp}_{os.path.basename(file_path)}"
                    dest_path = os.path.join(DEST_FOLDER, folder, new_filename)
                    shutil.move(file_path, dest_path)
                    print(f"Moved: {file_path} -> {dest_path}")
                    moved = True
                    break
            if not moved:
                dest_path = os.path.join(DEST_FOLDER, 'Others', os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                print(f"Moved to Others: {file_path} -> {dest_path}")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    print(f"📁 Monitoring folder: {WATCHED_FOLDER}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
