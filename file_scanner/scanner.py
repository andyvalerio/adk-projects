#!/usr/bin/env python3
import os, json, time
from pathlib import Path

ROOT = Path("/mnt/f/tv_series/")
OUTPUT = Path("/root/dev/adk-projects/storage/files.json")
CHECKPOINT_FILE = Path("/root/dev/adk-projects/storage/scanner_checkpoint.json")
BATCH_SIZE = 1000
SCAN_INTERVAL = 300  # seconds between full rescan

# Load or initialize inventory
if OUTPUT.exists():
    try:
        inventory = json.loads(OUTPUT.read_text())
    except Exception:
        inventory = {}
else:
    inventory = {}

def save_inventory(batch=None):
    global inventory
    if batch:
        inventory.update(batch)
    OUTPUT.write_text(json.dumps(inventory, indent=2))

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        try:
            return Path(json.loads(CHECKPOINT_FILE.read_text())["last_path"])
        except Exception:
            return ROOT
    return ROOT

def save_checkpoint(path):
    CHECKPOINT_FILE.write_text(json.dumps({"last_path": str(path)}))

def scan_incrementally(start_path):
    batch = {}
    count = 0
    for dirpath, _, filenames in os.walk(start_path):
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            try:
                stat = os.stat(full_path)
                rec = {"size": stat.st_size, "mtime": stat.st_mtime}
                # skip if unchanged
                if full_path in inventory and inventory[full_path] == rec:
                    continue
                batch[full_path] = rec
                count += 1
                if len(batch) >= BATCH_SIZE:
                    save_inventory(batch)
                    batch.clear()
            except Exception:
                continue
        # checkpoint per folder
        save_checkpoint(dirpath)
    # final batch
    if batch:
        save_inventory(batch)
    return count

def run_forever():
    global ROOT
    while True:
        print(f"Starting full scan at {time.ctime()}")
        start_path = load_checkpoint()
        added = scan_incrementally(start_path)
        print(f"Scan batch complete: {added} files added/updated. Total: {len(inventory)}")
        # reset checkpoint for next full scan
        save_checkpoint(str(ROOT))
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    run_forever()

