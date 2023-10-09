def get_logs(file: str) -> str:
    try:
        with open(file, "r", encoding="utf-8") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return ""
