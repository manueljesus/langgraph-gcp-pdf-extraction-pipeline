from typing import Dict, Union, List
import json

from src.utils.vertex_ai_llama_client import vertex_ai_llama_request
from src.logger import get_logger

logger = get_logger(__name__)


def extract_metadata(text: str) -> Dict[str, Union[str, List[str]]]:
    """Extract metadata such as title, authors, publication date, and abstract."""
    metadata_prompt = f"""
    You are an AI assistant. Extract the following metadata from the research paper text:

    - Title
    - Authors
    - Publication Date
    - Abstract

    Provide the output in **valid JSON format** that strictly follows this JSON schema:

    {{
        "title": "string",                // The title of the paper.
        "authors": ["string"],            // An array of author names.
        "publication_date": "string",     // The publication date in "YYYY-MM-DD" format.
        "abstract": "string"              // The abstract of the paper.
    }}

    - All fields are required: if any information is missing, set its value to null.
    - Authors: should be an array of author names as strings.
    - Publication Date: must be in "YYYY-MM-DD" format. It can be found at the beginning or end of the text in most cases.
    - Abstract: must be included exactly as it appears in the text, without any changes or modifications.
    - Do not include any additional text: output only the JSON object.

    Example:

    {{
        "title": "Advancements in Machine Learning",
        "authors": ["Alice Johnson", "Bob Smith"],
        "publication_date": "2022-08-30",
        "abstract": "This study explores recent advancements in machine learning techniques."
    }}

    Do not infer any data based on previous training, strictly use only source text given below:

    Text:
    \"\"\"
    {text}
    \"\"\"
    """
    try:
        logger.info("Extracting metadata")
        return json.loads(vertex_ai_llama_request(metadata_prompt).strip('```json').strip('```'))

    except Exception as e:
        logger.error(f"Error extracting metadata: {e}")
        return {
            "title": None,
            "authors": None,
            "publication_date": None,
            "abstract": None
        }
