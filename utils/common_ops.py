from datetime import datetime, timezone, timedelta
import glob
import os
from typing import Optional

def unix_to_iso_with_timezone(unix_timestamp: int) -> str:
    dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    
    # Define the timezone offset for UTC+5:30
    offset = timedelta(hours=5, minutes=30)
    tz = timezone(offset)
    dt_with_tz = dt.astimezone(tz)

    iso_timestamp = dt_with_tz.isoformat()
    return iso_timestamp

def iso_to_unix(iso_timestamp: str) -> int:
    dt = datetime.fromisoformat(iso_timestamp)
    offset = timedelta(hours=5, minutes=30)
    tz = timezone(offset)
    dt_with_tz = dt.replace(tzinfo=tz)
    dt_utc = dt_with_tz.astimezone(timezone.utc)
    unix_timestamp = int(dt_utc.timestamp())
    
    return unix_timestamp

def get_latest_file(folder_path: str, extension: Optional[str] = '*.xlsx') -> str:
    # Search for files with the given extension
    files = glob.glob(os.path.join(folder_path, extension))
    if not files:
        raise FileNotFoundError("No files found in the specified directory.")
    # Get the latest file
    latest_file = max(files, key=os.path.getctime)
    return latest_file