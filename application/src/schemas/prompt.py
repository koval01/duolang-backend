from pydantic import BaseModel
from typing import Dict, Any


class Prompt(BaseModel):
    lang: Dict[str, str]

    class Config:
        @staticmethod
        def validate_key(key: str) -> str:
            if not (len(key) == 5 and key[2] == '-' and key[:2].isalpha() and key[3:].isalpha()):
                raise ValueError(f"Invalid key format: {key}")
            return key

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_keys

    @classmethod
    def validate_keys(cls, value: Dict[str, str]):
        validated = {}
        for key, val in value.items():
            cls.validate_key(key)
            validated[key] = val
        return validated

    def __getattr__(self, name: str) -> Any:
        # Convert snake_case to the key format
        key = name.replace('_', '-')  # Replace underscores with hyphens
        if key in self.lang:
            return self.lang[key]
        raise AttributeError(f"Attribute '{name}' not found")
