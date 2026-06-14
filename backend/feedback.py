import os
import json
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class StarAnalysis(BaseModel):
    situation: str = Field(description="The situation described by the candidate.")
    task: str = Field(description="The task the candidate had to perform.")
    action: str = Field(description="The actions taken by the candidate.")
    result: str = Field(description="The outcome or result achieved.")

class InterviewFeedback(BaseModel):
    puntaje_global: int = Field(ge=0, le=100, description="Overall score from 1 to 100.")
    analisis_star: StarAnalysis = Field(description="Detailed STAR method analysis.")
    mejoras_comunicacion: List[str] = Field(description="Specific suggestions for communication, grammar, and linguistic style improvements in the language used.")

class FeedbackGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

    def generate_feedback(self, transcription: str, job_description: str) -> InterviewFeedback:
        """
        Generates structured feedback using Deepseek API.
        """
        prompt = f"""
        Analyze the following interview transcription based on the job description. 
        The candidate may speak in Spanish or English. Evaluate the quality of the content, 
        clarity, and technical accuracy regardless of the language.

        Provide a structured feedback in JSON format. 
        IMPORTANT: The JSON keys MUST be in English exactly as specified below, 
        but the values (the content) should be in the same language as the candidate's response.

        REQUIRED JSON SCHEMA:
        - puntaje_global: (integer) Score from 1 to 100.
        - analisis_star: (object) 
            - situation: (string)
            - task: (string)
            - action: (string)
            - result: (string)
        - mejoras_comunicacion: (list of strings) 3-5 suggestions.

        Job Description: {job_description}
        Transcription: {transcription}
        """

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer. You must respond ONLY with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return InterviewFeedback.model_validate_json(content)
