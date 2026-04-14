import json
import os
import time
from groq import Groq
from dotenv import load_dotenv
from .models import TestCase, GenerationHistory


load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class AIService:

    @staticmethod
    def _generate(code, language):
        """
        Core function that calls the Groq LLM.
        This does NOT touch the database.
        """

        system_prompt = (
            "You are a Senior QA Automation Engineer. Analyze the provided code and "
            "identify edge cases, boundary conditions, and potential bugs. "
            "Return ONLY a JSON object with key 'test_cases' containing a list of test cases."
        )

        user_prompt = f"""
Language: {language}

Code:
{code}

Generate 3–5 critical edge test cases.

For each test case provide:
- title
- description
- input
- expected_output
- severity (Critical, High, Medium)
"""

        start_time = time.time()

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
            temperature=0.2
        )

        end_time = time.time()

        response_content = chat_completion.choices[0].message.content
        data = json.loads(response_content)

        return data.get("test_cases", []), end_time - start_time


  

    @staticmethod
    def generate_from_code(code, language):
        """
        Used by the VS Code extension.
        Only returns generated test cases.
        """

        test_cases, generation_time = AIService._generate(code, language)

        return {
            "test_cases": test_cases,
            "generation_time": generation_time
        }


   

    @staticmethod
    def generate_and_store(source_code_obj):
 

        try:
            test_cases, _ = AIService._generate(
                source_code_obj.code_text,
                source_code_obj.language
            )

            for item in test_cases:
                TestCase.objects.create(
                    source_code=source_code_obj,
                    test_title=item.get("title"),
                    test_description=item.get("description"),
                    test_input=item.get("input"),
                    expected_output=item.get("expected_output"),
                    severity_level=item.get("severity")
                )

            GenerationHistory.objects.create(
                source_code=source_code_obj,
                model_used="groq/gpt-oss-120b",
                status="Success"
            )

            return test_cases

        except Exception as e:

            GenerationHistory.objects.create(
                source_code=source_code_obj,
                model_used="groq/gpt-oss-120b",
                status=f"Failed: {str(e)}"
            )

            raise e