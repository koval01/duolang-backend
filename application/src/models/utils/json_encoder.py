import json
from typing import Any

from sqlalchemy.types import TypeDecorator, TEXT


class JSONEncodedList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value: Any | None, dialect: Any) -> str | None:
        """Convert Python list or dict to JSON string before storing in the database."""
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value: str | None, dialect: Any) -> Any | None:
        """Convert JSON string from the database back to Python list or dict."""
        if value is None:
            return None
        return json.loads(value)
