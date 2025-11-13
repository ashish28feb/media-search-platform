from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime, timezone
from api.ms.news import get_all_news_data
from analyzer import analyze_article
from auth import authenticate_google_user, GoogleCredential
from dependencies import get_current_user

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "https://your-frontend-url.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class DateRange(BaseModel):
    from_date: Optional[str] = None
    to_date: Optional[str] = None

class MediaSearchInput(BaseModel):
    entity: str
    country: str
    tags: Optional[List[str]] = []
    date_range: Optional[DateRange] = None

def filter_articles_by_date(articles, date_range):
    """Filter articles to only include those within the specified date range."""
    if not date_range or not date_range.from_date or not date_range.to_date:
        print("No date range specified, returning all articles")
        return articles
    
    try:
        # Parse the date range
        from_date = datetime.strptime(date_range.from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(date_range.to_date, "%Y-%m-%d").date()
        
        print(f"Filtering articles for date range: {from_date} to {to_date}")
        filtered_articles = []
        
        for i, article in enumerate(articles):
            try:
                # Debug: Print article structure for first few articles
                if i < 3:
                    print(f"Article {i+1} structure: {list(article.keys()) if isinstance(article, dict) else 'Not a dict'}")
                
                # Check if article has a date field
                article_date = None
                
                # Try different possible date field names
                if isinstance(article, dict):
                    # Try common date field names including publishDate from your news.py
                    for date_field in ['publishDate', 'date', 'published', 'publishedAt', 'datePublished', 'pub_date']:
                        if date_field in article and article[date_field]:
                            article_date = article[date_field]
                            if i < 3:  # Debug first few articles
                                print(f"Found date in field '{date_field}': {article_date}")
                            break
                elif hasattr(article, 'publishDate'):
                    article_date = article.publishDate
                
                if not article_date:
                    print(f"No date found for article: {article.get('title', 'No title')[:50]}...")
                    # If no date found, exclude the article to be strict
                    continue
                
                # Parse article date - handle various formats
                parsed_date = None
                if isinstance(article_date, str):
                    # Try different date formats
                    date_formats = [
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%dT%H:%M:%SZ", 
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%d",
                        "%d/%m/%Y",
                        "%m/%d/%Y"
                    ]
                    
                    for fmt in date_formats:
                        try:
                            parsed_date = datetime.strptime(article_date, fmt).date()
                            break
                        except ValueError:
                            continue
                            
                    # If standard formats don't work, try parsing with dateutil
                    if not parsed_date:
                        try:
                            from dateutil.parser import parse
                            parsed_datetime = parse(article_date)
                            parsed_date = parsed_datetime.date()
                        except:
                            pass
                            
                elif isinstance(article_date, datetime):
                    parsed_date = article_date.date()
                
                # If we couldn't parse the date, skip the article
                if not parsed_date:
                    print(f"Could not parse date '{article_date}' for article: {article.get('title', 'No title')[:50]}...")
                    continue
                
                # Debug: Show date comparison for first few articles
                if i < 3:
                    print(f"Article date: {parsed_date}, Range: {from_date} to {to_date}, In range: {from_date <= parsed_date <= to_date}")
                
                # Check if article date is within range
                if from_date <= parsed_date <= to_date:
                    filtered_articles.append(article)
                else:
                    print(f"Filtered out article '{article.get('title', 'No title')[:50]}...' with date {parsed_date} (outside range {from_date} to {to_date})")
                    
            except Exception as e:
                print(f"Error processing article date: {e}")
                # If there's an error, skip the article to be strict
                continue
        
        print(f"Date filtering: {len(articles)} articles -> {len(filtered_articles)} articles")
        return filtered_articles
        
    except Exception as e:
        print(f"Error in date filtering: {e}")
        return articles  # Return original articles if filtering fails

@app.get("/")
async def root():
    return {"message": "Media Search API is running"}

@app.post("/search")
async def search_media(input_data: MediaSearchInput, current_user: dict = Depends(get_current_user)):
    """Protected search endpoint - requires authentication."""
    try:
        print(f"Search request from user: {current_user['email']}")
        
        # Your existing search logic remains the same
        query = {
            "query": input_data.entity,
            "advanced_options": {
                "country": [input_data.country],
                "detailed_query": input_data.tags or [],
                "date_range": input_data.date_range.dict() if input_data.date_range else None
            }
        }

        articles = await get_all_news_data(query=query)

        if not articles:
            return {"results": []}

        # Apply strict date filtering after getting results from Serper API
        if input_data.date_range:
            articles = filter_articles_by_date(articles, input_data.date_range)
            print(f"After date filtering: {len(articles)} articles remaining")

        if not articles:
            return {"results": [], "message": "No articles found within the specified date range"}

        # Step 2: Analyze each article
        tasks = [
            analyze_article(
                entity_name=input_data.entity,
                entity_description="",
                article=article.dict() if hasattr(article, "dict") else article
            )
            for article in articles
        ]

        results = await asyncio.gather(*tasks)
        
        # Add serial numbers
        for i, result in enumerate(results):
            result["S.No"] = i + 1

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/google")
async def google_auth(credential: GoogleCredential):
    """Handle Google OAuth authentication."""
    try:
        result = await authenticate_google_user(credential)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
