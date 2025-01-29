from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBaYkOY_pT-mPTtsEy-MmdmqrkImtDKTds")
model = genai.GenerativeModel("gemini-1.5-flash")

import google.generativeai as genai
import json
import re

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBaYkOY_pT-mPTtsEy-MmdmqrkImtDKTds")
model = genai.GenerativeModel("gemini-1.5-flash")


def get_input(query):
    prompt = f""" {query}
    Generate a JSON object for a job posting in the following format:

    {{
        "jobTitle": "Job Title",
        "jobDetails": "Full time, On site/Remote/Hybrid, Location",
        "experience": "Experience Range",
        "skills": ["Skill1", "Skill2", "Skill3", ...],
        "aboutRole": "A brief description of the role, responsibilities, and desired candidate traits.",
        "roleAndResponsibility": ["Responsibility1", "Responsibility2", "Responsibility3", ...],
        "softSkillsAndEducation": ["Soft Skill1", "Soft Skill2", "Educational Requirement1", ...],
        "niceToHave": ["Additional Skill1", "Additional Skill2", ...],
        "candidatesWithExperienceAtCompanies": ["Company1", "Company2", "Company3", ...],
        "interviewProcess": ["Stage1", "Stage2", "Stage3", ...]
    }}

    Generate a similar JSON object for a job posting based on the role description provided below:
    {query}
    """

    # Request response from Gemini API
    response = model.generate_content(prompt)

    # Debugging: Print raw response
    print("Raw Response from Gemini API:", response.text)

    # Ensure the response is not empty
    if not response.text.strip():
        return {"error": "Gemini API returned an empty response"}

    # ✅ Remove backticks and "json" keyword if present
    cleaned_response = re.sub(r"```json\n|\n```", "", response.text.strip())

    try:
        return json.loads(cleaned_response)  # Convert cleaned response to JSON
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON response from Gemini API",
            "details": str(e),
            "raw_response": cleaned_response
        }

# Django API View
@csrf_exempt
def generate_job_description(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get("query", "")

            if not query:
                return JsonResponse({"error": "Query parameter is required."}, status=400)

            result = get_input(query)
            return JsonResponse(result, safe=False)  # Send JSON response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
