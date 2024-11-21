from typing import Dict, Union, List
import json

from src.utils.vertex_ai_llama_client import vertex_ai_llama_request

def extract_summary_and_keywords(text: str) -> Dict[str, Union[str, List[str]]]:
    """Extract a summary and keywords from the given text."""
    summary_prompt = f"""
    You are an AI assistant. From the research paper text provided, perform the following tasks:

    1. **Generate a concise summary**: Provide a brief summary of the paper in your own words.

    2. **Extract Keywords**: List the most relevant keywords or phrases that represent the main topics of the paper.

    Provide the output in **valid JSON format** that strictly follows this JSON schema:

    {{
        "summary": "string",      // A concise summary of the paper.
        "keywords": ["string"]    // An array of keywords or key phrases.
    }}


    - Both fields are required: if any information is missing, set its value to null.
    - Keywords: should be an array of strings, each representing a keyword or key phrase.
    - Do **not** include any additional text: output **only the JSON object**. Do not begin with any introductory text or  "```json" line.

    Example:

    {{
        "summary": "This paper explores the impact of artificial intelligence on job automation, analyzing employment data to reveal significant correlations.",
        "keywords": ["Artificial Intelligence", "Job Automation", "Employment Data", "Economic Impact"]
    }}

    Do not infer any data based on previous training, strictly use only source text given below:

    Text:
    \"\"\"
    {text}
    \"\"\"
    """
    try:
        return json.loads(vertex_ai_llama_request(summary_prompt).strip('```json').strip('```'))
    except Exception as e:
        print(e)
        response_text = None


    # Parse response assuming JSON format or key-value pairs
    if response_text:
        return json.loads(response_text)

    return {
            "summary": None,
            "keywords": None
        }