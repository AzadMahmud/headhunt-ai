import json

from mistralai.client import Mistral

from app.core.config import settings
from app.schemas.analysis import ResumeAnalysisResponse

PROMPT_TEMPLATE = """You are an experienced technical recruiter.

Analyze the following resume.

Return ONLY a JSON object with exactly 4 keys:
strengths
weaknesses
missing_skills
recommendations

Each key must be a flat array of strings (no nested objects).

Resume:
{resume_text}"""


def analyze_resume(resume_text: str) -> ResumeAnalysisResponse:
    client = Mistral(api_key=settings.MISTRAL_API_KEY)

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": PROMPT_TEMPLATE.format(resume_text=resume_text)}
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    return ResumeAnalysisResponse(**data)
