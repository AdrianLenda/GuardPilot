"""
Utility to append conversation logs to a Parquet file with a simple hash-chain for immutability.
"""

from typing import Any, Dict
import os
import hashlib
from pathlib import Path

import pandas as pd

# Directory where logs and hash chain will be stored
LOGS_DIR = Path(os.getenv("LOGS_DIR", "/data"))
LOGS_DIR.mkdir(parents=True, exist_ok=True)

PARQUET_FILE = LOGS_DIR / "conversations.parquet"
HASH_FILE = LOGS_DIR / "parquet_hash_chain.txt"


def _compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hash of given bytes."""
    return hashlib.sha256(data).hexdigest()


def append_log(entry: Dict[str, Any]) -> None:
    """
    Append a single log entry (dictionary) to the Parquet file.
    Maintains a simple hash chain: each line in HASH_FILE is the hash of
    the previous hash concatenated with the CSV representation of the new row.
    """
    # Convert entry to DataFrame
    df = pd.DataFrame([entry])

    # Write or append to Parquet file
    if PARQUET_FILE.exists():
        df.to_parquet(PARQUET_FILE, engine="pyarrow", append=True, index=False)
    else:
        df.to_parquet(PARQUET_FILE, engine="pyarrow", index=False)

    # Compute new hash chaining previous hash and new row data
    prev_hash = ""
    if HASH_FILE.exists():
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                prev_hash = lines[-1].strip()

    # Use CSV representation of the DataFrame row for hashing consistency
    new_data = df.to_csv(index=False).encode("utf-8")
    new_hash = _compute_sha256(prev_hash.encode("utf-8") + new_data)

    # Append new hash to the chain file
    with open(HASH_FILE, "a", encoding="utf-8") as f:
        f.write(new_hash + "\n")
