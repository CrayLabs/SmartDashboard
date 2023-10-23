def get_logs(file: str) -> str:
    """Get the logs of an entity

    :param file: Log file path of the entity
    :type file: str
    :return: Logs of the entity
    :rtype: str
    """
    try:
        with open(file, "r", encoding="utf-8") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return ""
