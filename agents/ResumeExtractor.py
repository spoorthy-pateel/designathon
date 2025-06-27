def build_prompt(resume_text):
    return f"""
IMPORTANT: Respond ONLY with a valid JSON object. 
NO markdown, NO code fences, NO explanations, NO comments, NO extra text.
If you include anything other than the JSON object, the result will be discarded.

Output must be a pure JSON object matching this structure:
{{
  "skills": [
    {{
      "technologies_known": "string (e.g., Python, JavaScript, etc.)",
      "years_of_experience": number (e.g., 3.5),
      "strength_of_skill": integer (1-10, how strong this skill is based on the resume)
    }}
  ],
  "certifications": [
    {{
      "certification_name": "string",
      "issued_date": "YYYY-MM-DD",
      "valid_till": "YYYY-MM-DD or null"
    }}
  ],
  "professional": {{
    "last_worked_organization": "string",
    "recent_role": "string",
    "recent_project": "string or null",
    "recent_start_date": "YYYY-MM-DD or null",
    "recent_project_release_date": "YYYY-MM-DD or null"
  }}
}}

Guidelines:
- Estimate years_of_experience as accurately as possible from the resume.
- For strength_of_skill, give an integer 1 (weakest) to 10 (strongest) for each skill, based on emphasis and context.
- Use ISO 8601 date format (YYYY-MM-DD) for all dates.
- If any information is missing, set its value to null.

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""