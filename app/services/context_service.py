import json
from pathlib import Path


class ContextService:
    def __init__(self):
        path = Path(__file__).parent.parent / "data" / "mock_context.json"
        with open(path, "r") as f:
            self.context = json.load(f)

    def get_context(self):
        return self.context


context_service = ContextService()