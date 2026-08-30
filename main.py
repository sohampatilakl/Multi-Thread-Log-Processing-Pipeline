import threading
import queue

# The Master Scoreboard
stats = {"processed": 0, "errors": 0, "status_codes": {}}

# The Magic Marker (Mutex Lock)
stats_lock = threading.Lock()
# The Conveyor belt that holds up to 100 pages at a time
log_queue = queue.Queue(maxsize=100)

def worker():
    while True:
        # Grab a page from the conveyor belt
        line = log_queue.get()
        
        # If it's a blank page (Go Home signal), stop working
        if line is None: 
            break
            
        try:
            # Read the page: get the last word (the status code)
            status_code = line.strip().split()[-1]
            if not status_code.isdigit():
                raise ValueError("Corrupted line")
                
            # Ask for the Magic Marker, then write on the board
            with stats_lock:
                stats["processed"] += 1
                stats["status_codes"][status_code] = stats["status_codes"].get(status_code, 0) + 1
                
        except Exception:
            # If the page is corrupted, mark an error safely
            with stats_lock:
                stats["errors"] += 1
                
        # Tell the conveyor belt this page is completely done
        log_queue.task_done()

import os
import kagglehub
import threading # (Assuming threading is already imported in Cell 1)

# 1. Download the NASA dataset via Kaggle
print("Downloading NASA dataset...")
path = kagglehub.dataset_download("adchatakora/nasa-http-access-logs")
print(f"Dataset downloaded to: {path}")

num_workers = 3
threads = []

# 2. Hire the 3 workers and tell them to start waiting at the belt
for _ in range(num_workers):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# 3. The Page Tearer: Read the actual NASA log files
# Kaggle gives us a folder path, so we iterate through the files inside it
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    
    # Check if it is a file (and not a sub-folder)
    if os.path.isfile(file_path):
        print(f"Producer is starting to read: {filename} ...")
        
        # Open the massive file and read line-by-line. 
        # Note: We use errors="ignore" because 1995 internet logs often contain weird text encodings.
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                log_queue.put(line)

# Drop 3 blank pages (None) onto the belt so all 3 workers know to stop
for _ in range(num_workers):
    log_queue.put(None)

# Wait here until every worker has safely clocked out (finished their loop)
for t in threads:
    t.join()

# Show the final math
print("Factory Closed. Final Scoreboard:")
print(stats)
  
