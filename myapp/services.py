import json
import os
from groq import Groq
from .models import TestCase, GenerationHistory

# Initialize the Groq client
client = Groq(api_key="REMOVED2BXO5RnZ5WKXSk3sRhfEWGdyb3FYEOYyhyQ4m6lMnpcGfkepSRBw")

class AIService:
    @staticmethod
    def generate_test_cases(source_code_obj):
        # 1. Craft the System Prompt
        system_prompt = (
            "You are a Senior QA Automation Engineer. Analyze the provided code and "
            "identify potential edge cases, boundary conditions, and security risks. "
            "Return ONLY a JSON object with a key 'test_cases' containing an array of objects."
        )

        # 2. Craft the User Prompt
        user_prompt = f"""
        Language: {source_code_obj.language}
        Code:
        {source_code_obj.code_text}
        
        Generate 3-5 critical edge-case scenarios. For each, provide:
        - title: Short name of the test
        - description: What is being tested
        - input: The specific input values
        - expected_output: The expected behavior
        - severity: 'Critical', 'High', or 'Medium'
        """

        try:
            # 3. Call Groq API
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="openai/gpt-oss-120b", 
                response_format={"type": "json_object"}, 
                temperature=0.2, 
            )
            

            # 4. Parse Response
            response_content = chat_completion.choices[0].message.content
            data = json.loads(response_content)
            
            # 5. Save TestCases to DB
            test_cases_data = data.get('test_cases', [])
            for item in test_cases_data:
                TestCase.objects.create(
                    source_code=source_code_obj,
                    test_title=item.get('title'),
                    test_description=item.get('description'),
                    test_input=item.get('input'),
                    expected_output=item.get('expected_output'),
                    severity_level=item.get('severity')
                )

            # 6. Log History
            GenerationHistory.objects.create(
                source_code=source_code_obj,
                model_used="groq/gpt-oss-120b",
                status="Success"
            )
            
            return True

        except Exception as e:
            # Log failure in history
            GenerationHistory.objects.create(
                source_code=source_code_obj,
                model_used="groq/llama3-70b",
                status=f"Failed: {str(e)}"
            )
            raise e