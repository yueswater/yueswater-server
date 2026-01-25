import os
from datetime import datetime
from pathlib import Path

# 定義 Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 確保 Log 資料夾存在
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# 產生檔名：yyyy-mm-dd-HH-MM.log
current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
LOG_FILENAME = os.path.join(LOGS_DIR, f"{current_time}.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} [{name}:{lineno}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",  # 開發時 Console 輸出簡單格式
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILENAME,
            "formatter": "verbose",  # 寫入檔案詳細格式
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # 捕捉 Django 系統本身的錯誤
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        # 捕捉 App 的 Log
        "apps": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
        # 捕捉 DRF 的錯誤
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
