import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
import httpx

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

HEADERS = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_KEY
}

async def analyze_article(entity_name: str, entity_description: str, article: dict) -> dict:
    """
    Analyze a single article using Azure OpenAI and return structured results.
    Supports multilingual input and returns summary in English.
    """
    content = article.get("content") or article.get("description") or ""
    if not content.strip():
        return {
            "error": "Article content is empty.",
            "originalTitle": article.get("title", ""),
            "url": article.get("url", ""),
            "source": article.get("source", "")
        }

    system_prompt = """
You are an expert media analyst. Analyze the article below for its relevance to the specified entity and provide a structured summary of its content.

Return a JSON object with the following fields:
- subjectMatchScore (0-100): How strongly the article is about the entity.
- matchedDetails (list of strings): Specific phrases or sentences that mention the entity.
- tags (list of 3-5 keywords): Keywords that best describe the article's main topics.
- sentiment ("positive", "neutral", or "negative"): Overall sentiment of the article.
- crimeRelated (true/false): Whether the article involves crime-related content.
- unethicalRelated (true/false): Whether the article involves unethical behavior.
- confidence (0-100): Your confidence in the analysis.
- summary (in English, 2-3 sentences): A concise summary of the article's content and its relevance to the entity.
- catchyTitle (string): A short, attention-grabbing title in the same language as the article (e.g., Hindi or English).
- publishDate (ISO format or null): Use the provided Article Publish Date if available, otherwise null.
- isPaywalled (true/false): Whether the article is behind a paywall.

Respond ONLY with a valid JSON object. Do not include any explanation or commentary.
"""

    user_prompt = f"""
Entity Name: {entity_name}
Entity Description: {entity_description or "N/A"}
Article Title: {article.get("title", "")}
Article Content: {content}
Article Publish Date: {article.get("publishDate", "Unknown")}
"""

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        "temperature": 0.2,
        "max_tokens": 1000
    }

    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=HEADERS, json=payload)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            data = json.loads(content)

            # Preserve the original publishDate from news extraction, don't let AI override it
            original_publish_date = article.get("publishDate", None)
            ai_publish_date = data.get("publishDate", None)
            
            # Always prefer original date from news extraction over AI response
            # Only use AI date if original is completely missing
            if original_publish_date and original_publish_date.strip():
                final_publish_date = original_publish_date
                print(f"Using original date: {original_publish_date}")
            elif ai_publish_date and ai_publish_date.strip():
                final_publish_date = ai_publish_date
                print(f"Using AI date: {ai_publish_date}")
            else:
                # Last resort fallback if both are null/empty
                from datetime import datetime, timedelta
                yesterday = datetime.now() - timedelta(days=1)
                final_publish_date = yesterday.isoformat() + "Z"
                print(f"Using analyzer fallback date: {final_publish_date}")
            
            result = {
                "subjectMatchScore": data.get("subjectMatchScore", 0),
                "matchedDetails": data.get("matchedDetails", []),
                "tags": data.get("tags", []),
                "sentiment": data.get("sentiment", "neutral"),
                "crimeRelated": data.get("crimeRelated", False),
                "unethicalRelated": data.get("unethicalRelated", False),
                "confidence": data.get("confidence", 0),
                "summary": data.get("summary", "No summary available."),
                "catchyTitle": data.get("catchyTitle", ""),
                "publishDate": final_publish_date,
                "isPaywalled": data.get("isPaywalled", False),
                "originalTitle": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("source", "")
            }
            
            return result

    except Exception as e:
        return {
            "error": str(e),
            "originalTitle": article.get("title", ""),
            "url": article.get("url", ""),
            "source": article.get("source", "")
        }
