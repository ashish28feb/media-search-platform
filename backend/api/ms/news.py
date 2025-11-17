import os
import httpx
from typing import List, Dict
from dotenv import load_dotenv
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config
from trafilatura.meta import reset_caches
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
import re

load_dotenv()

def parse_relative_date(date_str: str) -> str:
    """
    Convert relative date strings like '2 hours ago', '1 day ago' to ISO format dates.
    Supports both English and Hindi relative dates.
    Returns ISO formatted date string or empty string if parsing fails.
    """
    if not date_str or date_str.strip() == "":
        return ""
    
    try:
        original_date_str = date_str
        date_str = date_str.lower().strip()
        now = datetime.now()
        
        # Extract number from the string
        number_match = re.search(r'(\d+)', date_str)
        if not number_match:
            # Try to parse as regular date if no numbers found
            try:
                parsed_date = parse(original_date_str)
                return parsed_date.isoformat() + "Z"
            except:
                return ""
        
        number = int(number_match.group(1))
        
        # Handle minutes - English and Hindi
        if any(word in date_str for word in ["minute", "मिनट"]):
            result_date = now - timedelta(minutes=number)
            return result_date.isoformat() + "Z"
        
        # Handle hours - English and Hindi  
        elif any(word in date_str for word in ["hour", "घंटे", "घंटा"]):
            result_date = now - timedelta(hours=number)
            return result_date.isoformat() + "Z"
        
        # Handle days - English and Hindi
        elif any(word in date_str for word in ["day", "दिन"]):
            result_date = now - timedelta(days=number)
            return result_date.isoformat() + "Z"
        
        # Handle weeks - English and Hindi
        elif any(word in date_str for word in ["week", "सप्ताह", "हफ्ता"]):
            result_date = now - timedelta(weeks=number)
            return result_date.isoformat() + "Z"
        
        # Handle months - English and Hindi (approximate)
        elif any(word in date_str for word in ["month", "महीना", "महीने"]):
            result_date = now - timedelta(days=number * 30)  # Approximate
            return result_date.isoformat() + "Z"
        
        # If no time unit matched, try to parse as regular date
        else:
            try:
                parsed_date = parse(original_date_str)
                return parsed_date.isoformat() + "Z"
            except:
                return ""
            
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return ""
    
    return ""

def extract_date_from_url_or_title(url: str, title: str = "") -> str:
    """
    Extract date from URL path or article title as a lightweight fallback.
    Many news URLs contain dates like: /2025/11/08/ or /article/125191511.cms
    """
    try:
        # Check URL for date patterns
        url_patterns = [
            r'/(\d{4})/(\d{1,2})/(\d{1,2})/',  # /2025/11/08/
            r'/(\d{4})-(\d{1,2})-(\d{1,2})',   # /2025-11-08
            r'(\d{4})(\d{2})(\d{2})',          # 20251108 in URL
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, url)
            if match:
                groups = match.groups()
                try:
                    if len(groups) == 3:
                        year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                        if 2020 <= year <= 2030 and 1 <= month <= 12 and 1 <= day <= 31:
                            result_date = datetime(year, month, day)
                            return result_date.isoformat() + "Z"
                except ValueError:
                    continue
        
        # Check title for date patterns (less common but possible)
        if title:
            title_patterns = [
                r'(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})',
                r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})',
            ]
            
            month_abbr_map = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            
            title_lower = title.lower()
            for pattern in title_patterns:
                match = re.search(pattern, title_lower)
                if match:
                    groups = match.groups()
                    try:
                        if groups[1] in month_abbr_map:  # Day Month Year format
                            day, month_abbr, year = int(groups[0]), groups[1], int(groups[2])
                            month = month_abbr_map[month_abbr]
                        elif groups[0] in month_abbr_map:  # Month Day Year format
                            month_abbr, day, year = groups[0], int(groups[1]), int(groups[2])
                            month = month_abbr_map[month_abbr]
                        else:
                            continue
                            
                        if 2020 <= year <= 2030 and 1 <= month <= 12 and 1 <= day <= 31:
                            result_date = datetime(year, month, day)
                            return result_date.isoformat() + "Z"
                    except (ValueError, KeyError):
                        continue
                        
    except Exception as e:
        print(f"Error extracting date from URL/title: {e}")
    
    return ""

def extract_date_from_content(content: str, url: str = "") -> str:
    """
    Extract publication date from article content using regex patterns.
    Returns ISO formatted date string or empty string if no date found.
    """
    if not content or content.strip() == "":
        return ""
    
    try:
        # Common date patterns to look for
        date_patterns = [
            # "Updated : 8 November 2025, 6:57 PM IST"
            r'(?:updated|published|posted)\s*:?\s*(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            # "8 November 2025"
            r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            # "November 8, 2025"
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})',
            # "2025-11-08"
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            # "08/11/2025" or "8/11/2025"
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            # "08-11-2025"
            r'(\d{1,2})-(\d{1,2})-(\d{4})',
        ]
        
        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        content_lower = content.lower()
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                
                try:
                    if len(groups) == 3:
                        if groups[1] in month_map:  # Month name format
                            if pattern.startswith(r'(january'):  # "November 8, 2025" format
                                month = month_map[groups[0]]
                                day = int(groups[1])
                                year = int(groups[2])
                            else:  # "8 November 2025" format
                                day = int(groups[0])
                                month = month_map[groups[1]]
                                year = int(groups[2])
                        elif groups[0].isdigit() and len(groups[0]) == 4:  # "2025-11-08" format
                            year = int(groups[0])
                            month = int(groups[1])
                            day = int(groups[2])
                        else:  # "08/11/2025" or "08-11-2025" format
                            day = int(groups[0])
                            month = int(groups[1])
                            year = int(groups[2])
                        
                        # Validate date components
                        if 1 <= day <= 31 and 1 <= month <= 12 and 2020 <= year <= 2030:
                            result_date = datetime(year, month, day)
                            return result_date.isoformat() + "Z"
                            
                except (ValueError, KeyError):
                    continue
                    
    except Exception as e:
        print(f"Error extracting date from content: {e}")
    
    return ""

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/news"
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": SERPER_API_KEY
}

OPENAI_HEADERS = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_KEY
}


def extract_full_content(url: str) -> str:
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "20")
    config.set("DEFAULT", "FETCH_TIMEOUT", "10")
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", "250")
    config.set("DEFAULT", "MAX_EXTRACTED_SIZE", "10000000")
    try:
        downloaded = fetch_url(url, config=config)
        if downloaded:
            article_content = extract(
                downloaded,
                config=config,
                include_comments=False,
                include_tables=False,
                include_links=False,
                include_images=False,
                include_formatting=False,
                no_fallback=True,
                with_metadata=True,
                output_format='txt',
            )
            reset_caches()
            return article_content or ""
    except Exception as e:
        print(f"Trafilatura error for {url}: {e}")
    return ""

async def translate_keywords(keywords: List[str], target_language: str) -> List[str]:
    if not keywords:
        return []
    prompt = f"Translate the following keywords into {target_language}. Return only a comma-separated list.\n\n" + ", ".join(keywords)
    payload = {
        "messages": [
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 100
    }
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, headers=OPENAI_HEADERS, json=payload)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return [kw.strip() for kw in content.split(",") if kw.strip()]
    except Exception as e:
        print(f"Translation error: {e}")
        return []

def generate_query_variants(entity: str, tags: List[str], translated_tags: List[str]) -> List[str]:
    queries = [entity]  # Simple entity search
    
    # Add simple tag-based queries without complex operators
    if tags:
        for tag in tags[:3]:  # Limit to first 3 tags
            queries.append(f'{entity} {tag}')
    
    # Add simple translated tag queries
    if translated_tags:
        for tag in translated_tags[:2]:  # Limit to first 2 translated tags
            queries.append(f'{entity} {tag}')
    return queries

async def get_all_news_data(query: Dict) -> List[Dict]:
    entity = query.get("query")
    options = query.get("advanced_options", {})
    country = options.get("country", ["US"])[0].lower()
    tags = options.get("detailed_query", [])
    date_range = options.get("date_range")

    translated_tags = await translate_keywords(tags, "Hindi" if country == "in" else "local language")
    query_variants = generate_query_variants(entity, tags, translated_tags)

    articles = []
    seen_urls = set()

    try:
        async with httpx.AsyncClient(timeout=100) as client:
            for q in query_variants:
                for lang in ["en", "hi", "auto"]:
                    payload = {
                        "q": q,
                        "hl": lang,
                        "gl": country,
                        "num": 100  # Reduced to get more relevant results
                    }
                    
                    if date_range:
                        from_date = date_range.get("from_date")
                        to_date = date_range.get("to_date")
                        if from_date and to_date:
                            payload["publishedAfter"] = from_date
                            payload["publishedBefore"] = to_date
                    
                    try:
                        response = await client.post(SERPER_API_URL, headers=HEADERS, json=payload)
                        response.raise_for_status()
                        data = response.json()
                        news_items = data.get("news", [])
                        
                        for item in news_items:
                            url = item.get("link", "")
                            if url in seen_urls:
                                continue
                            seen_urls.add(url)
                            
                            # Parse the relative date from Serper API first
                            raw_date = item.get("date", "")
                            parsed_date = parse_relative_date(raw_date)
                            
                            # If no date from Serper, try multiple fallback methods
                            if not parsed_date or parsed_date.strip() == "":
                                print(f"No date from Serper for {url}, trying fallbacks...")
                                
                                # Try URL/title extraction first (faster)
                                title = item.get("title", "")
                                url_date = extract_date_from_url_or_title(url, title)
                                if url_date:
                                    parsed_date = url_date
                                    print(f"Found date in URL/title: {url_date}")
                                    content = item.get("snippet", "")  # Use snippet since we found date elsewhere
                                else:
                                    # Fall back to content extraction (slower)
                                    print(f"Trying content extraction for {url}...")
                                    full_content = extract_full_content(url)
                                    if full_content:
                                        content_date = extract_date_from_content(full_content, url)
                                        if content_date:
                                            parsed_date = content_date
                                            print(f"Found date in content: {content_date}")
                                        content = full_content
                                    else:
                                        print(f"No content extracted for {url}")
                                        content = item.get("snippet", "")
                                
                                # Final fallback: use recent date for news articles if we still don't have a date
                                # Most news without dates are recent, so use yesterday as reasonable estimate
                                if not parsed_date or parsed_date.strip() == "":
                                    yesterday = datetime.now() - timedelta(days=1)
                                    parsed_date = yesterday.isoformat() + "Z"
                                    print(f"Using fallback date (yesterday): {parsed_date}")
                            else:
                                # Use snippet if we have date from Serper
                                content = item.get("snippet", "")
                            
                            articles.append({
                                "title": item.get("title", ""),
                                "content": content,
                                "url": url,
                                "source": item.get("source", "Unknown"),
                                "publishDate": parsed_date
                            })
                    except Exception as e:
                        print(f"Error fetching query '{q}' with lang '{lang}': {e}")
    except Exception as e:
        print(f"Error initializing client: {e}")

    return articles
