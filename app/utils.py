"""
Utility functions for MoodKeeper application.
Provides common helpers for CSV operations, validation, and formatting.
"""
import os
import csv
from datetime import datetime
from typing import Optional, List, Dict, Any


def ensure_csv_exists(path: str, headers: List[str]) -> None:
    """
    Ensure a CSV file exists with the given headers.
    Creates directory and file if they don't exist.
    
    Args:
        path: Absolute path to CSV file
        headers: List of column names
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def get_next_id(csv_path: str) -> int:
    """
    Get the next available ID for a CSV file.
    Scans existing IDs and returns max + 1.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Next available ID (1 if file is empty)
    """
    if not os.path.exists(csv_path):
        return 1
    
    max_id = 0
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    current_id = int(row.get('id', 0))
                    if current_id > max_id:
                        max_id = current_id
                except (ValueError, TypeError):
                    continue
    except Exception:
        pass
    
    return max_id + 1


def read_csv_as_dicts(csv_path: str) -> List[Dict[str, Any]]:
    """
    Read a CSV file and return as list of dictionaries.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of dictionaries (one per row)
    """
    if not os.path.exists(csv_path):
        return []
    
    rows = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except Exception:
        pass
    
    return rows


def append_to_csv(csv_path: str, row_data: List[Any]) -> bool:
    """
    Append a row to a CSV file.
    
    Args:
        csv_path: Path to CSV file
        row_data: List of values to append
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)
        return True
    except Exception:
        return False


def format_timestamp(dt: Optional[datetime] = None, iso: bool = True) -> str:
    """
    Format a datetime object as string.
    
    Args:
        dt: Datetime object (uses current time if None)
        iso: If True, use ISO-8601 format; otherwise use readable format
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        dt = datetime.now()
    
    if iso:
        return dt.isoformat()
    else:
        return dt.strftime('%Y-%m-%d %H:%M:%S')


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Parse a timestamp string to datetime object.
    Tries ISO-8601 format first, then common formats.
    
    Args:
        timestamp_str: String representation of datetime
        
    Returns:
        Datetime object or None if parsing fails
    """
    if not timestamp_str:
        return None
    
    # Try ISO-8601
    try:
        return datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError):
        pass
    
    # Try common formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    return None


def validate_range(value: Any, min_val: float, max_val: float, field_name: str = "Value") -> None:
    """
    Validate that a value is within a specified range.
    Raises ValueError if validation fails.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of field (for error message)
        
    Raises:
        ValueError: If value is outside range
    """
    try:
        num_value = float(value)
        if not (min_val <= num_value <= max_val):
            raise ValueError(f"{field_name} must be between {min_val} and {max_val}, got {num_value}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid {field_name}: {e}")


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """
    Safely convert value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """
    Safely convert value to int.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to specified length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_risk_color(risk_level: str) -> str:
    """
    Get color code for risk level visualization.
    
    Args:
        risk_level: Risk level (ALTO, MODERADO, BAJO)
        
    Returns:
        Hex color code
    """
    colors = {
        'ALTO': '#dc3545',      # Red
        'MODERADO': '#ffc107',  # Yellow/Orange
        'BAJO': '#198754',      # Green
    }
    return colors.get(risk_level.upper(), '#6c757d')  # Default gray


def get_risk_emoji(risk_level: str) -> str:
    """
    Get emoji representation of risk level.
    
    Args:
        risk_level: Risk level (ALTO, MODERADO, BAJO)
        
    Returns:
        Emoji string
    """
    emojis = {
        'ALTO': '🚨',
        'MODERADO': '⚠️',
        'BAJO': '✅',
    }
    return emojis.get(risk_level.upper(), '❓')


def calculate_days_since(timestamp_str: str) -> Optional[int]:
    """
    Calculate number of days since a given timestamp.
    
    Args:
        timestamp_str: ISO-8601 timestamp string
        
    Returns:
        Number of days (int) or None if parsing fails
    """
    dt = parse_timestamp(timestamp_str)
    if dt is None:
        return None
    
    delta = datetime.now() - dt
    return delta.days


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing potentially dangerous characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    # Limit length
    max_len = 255
    if len(sanitized) > max_len:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:max_len - len(ext)] + ext
    
    return sanitized or 'unnamed'


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


# Export all public functions
__all__ = [
    'ensure_csv_exists',
    'get_next_id',
    'read_csv_as_dicts',
    'append_to_csv',
    'format_timestamp',
    'parse_timestamp',
    'validate_range',
    'safe_float',
    'safe_int',
    'truncate_string',
    'get_risk_color',
    'get_risk_emoji',
    'calculate_days_since',
    'sanitize_filename',
    'format_file_size',
]
