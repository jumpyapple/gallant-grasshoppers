import json


def jsonparse(data: str) -> dict:
    """Parses JSON and returns dict"""
    return json.loads(data)
