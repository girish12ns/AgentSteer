

# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """
    Set up logging with daily folder structure.
    Structure: logs/2024-11-30/application.log
    """
    
    # Create base logs directory
    base_log_dir = Path("logs")
    base_log_dir.mkdir(exist_ok=True)
    
    # Create daily folder (e.g., logs/2024-11-30/)
    daily_folder = base_log_dir / datetime.now().strftime('%Y-%m-%d')
    daily_folder.mkdir(exist_ok=True)
    
    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Application log file
    app_log_file = daily_folder / "application.log"
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(log_format)
    root_logger.addHandler(app_handler)
    
    # Error log file
    error_log_file = daily_folder / "errors.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    # Debug log file
    debug_log_file = daily_folder / "debug.log"
    debug_handler = RotatingFileHandler(
        debug_log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=3,
        encoding='utf-8'
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(log_format)
    root_logger.addHandler(debug_handler)
    
    logging.info(f"Logging initialized - Directory: {daily_folder.absolute()}")
    
    return root_logger

# Initialize logging
logger = setup_logging()
