from typing import Dict, Union, List
import json

from src.utils.vertex_ai_llama_client import vertex_ai_llama_request
from src.logger import get_logger

logger = get_logger(__name__)


def extract_key_research_findings_and_methodology(text: str) -> Dict[str, Union[str, List[str]]]:
    """Extract key research findings and methodology from the given text."""
    findings_prompt = f"""
    You are an AI assistant. From the research paper text provided, extract the following:

    - Methodology
    - Key Research Findings

    Provide the output in **valid JSON format** that strictly follows this JSON schema:

    {{
        "methodology": "string",          // The methodology used in the research.
        "key_research_findings": ["string"] // The key findings of the research.
    }}

    - Both fields are required: if any information is missing, set its value to null.
    - Extract the content exactly as it appears in the text, without any changes or modifications.
    - Do **not** include any additional text: output **only the JSON object**.

    Example:

    {{
    "methodology": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
    "key_research_findings": ["The proposed algorithm outperformed baseline models by 15% in accuracy and demonstrated robustness across multiple datasets."]
    }}

    Do not infer any data based on previous training, strictly use only source text given below:

    Text:
    \"\"\"
    {text}
    \"\"\"
    """

    try:
        logger.info("Extracting key research findings and methodology")
        return json.loads(vertex_ai_llama_request(findings_prompt).strip('```json').strip('```'))

    except Exception as e:
        logger.error(f"Error extracting key research findings and methodology: {e}")
        print(f"Error extracting key research findings and methodology: {e}")
        return {
            "methodology": None,
            "key_research_findings": None
        }