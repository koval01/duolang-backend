import os
import re
import json

from typing import Literal, Optional

import google.generativeai as genai
from application.src.config import settings
from application.src.models import Lesson
from application.src.schemas import Prompt


class Gemini:
    def __init__(self) -> None:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompts_path = os.path.join(current_dir, "prompts.json")

        # Read and parse the JSON file
        with open(prompts_path, "r") as file:
            json_data = file.read()
            data_dict = json.loads(json_data)

        # select prompt like self.prompts.de_ru
        self.prompts: Prompt = Prompt(lang=data_dict)

    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        match_json = re.search(json_pattern, text, re.DOTALL)
        if match_json:
            json_str = match_json.group(1).strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                print("Failed to parse JSON")
                return None
        return None

    def execute(self, l_mode: Literal["de-ru"]) -> Lesson:
        if l_mode not in self.prompts.lang:
            raise ValueError(f"Invalid language mode: {l_mode}")

        prompt_text = self.prompts.lang[l_mode]

        response = self.model.generate_content(prompt_text)
        parsed = self._extract_json(response.text)

        return Lesson(**parsed)
