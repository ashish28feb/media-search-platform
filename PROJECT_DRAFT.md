# Media Search & Analysis Platform - Complete Project Draft

## 🎯 Project Overview
A comprehensive news search and AI-powered analysis platform built with FastAPI backend and React frontend. The system fetches real-time news articles, performs intelligent content analysis, and provides an advanced data visualization interface.

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MEDIA SEARCH & ANALYSIS PLATFORM                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 FRONTEND LAYER                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   SearchForm    │    │      App.jsx    │    │  ResultsTable   │
    │   Component     │    │   (Main State)  │    │   Component     │
    │                 │    │                 │    │                 │
    │ • Entity Input  │◄──►│ • Theme Config  │◄──►│ • AG-Grid Table │
    │ • Country Select│    │ • Error Handling│    │ • Column Filters│
    │ • Tags Input    │    │ • Loading States│    │ • Clickable URLs│
    │ • Date Range    │    │ • Result Storage│    │ • Pagination    │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
             │                       │                       │
             └───────────────────────┼───────────────────────┘
                                     │
                            ┌─────────────────┐
                            │    api.js       │
                            │  (HTTP Client)  │
                            │                 │
                            │ • Axios Config  │
                            │ • Error Handler │
                            │ • 5min Timeout  │
                            └─────────────────┘
                                     │
                                     │ HTTP POST /search
                                     │ JSON payload
                                     ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 BACKEND LAYER                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

                            ┌─────────────────┐
                            │    main.py      │
                            │ (FastAPI Server)│
                            │                 │
                            │ • CORS Setup    │
                            │ • /search Route │
                            │ • Error Handling│
                            │ • Async Orchestr│
                            └─────────────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     │               │               │
                     ▼               ▼               ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │    news.py      │ │   analyzer.py   │ │  api/ms/ modules│
        │ (News Fetching) │ │ (AI Analysis)   │ │   (Utilities)   │
        │                 │ │                 │ │                 │
        │ • Query Builder │ │ • Azure OpenAI  │ │ • models.py     │
        │ • Multi-lang    │ │ • Sentiment     │ │ • utils.py      │
        │ • Date Extract  │ │ • Crime Detect  │ │ • analysis.py   │
        │ • Content Scrape│ │ • Date Preserve │ │ • cfg/ folder   │
        └─────────────────┘ └─────────────────┘ └─────────────────┘
                 │                   │
                 │                   │
                 ▼                   ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SERVICES                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
    │   Serper API    │              │  Azure OpenAI   │              │  Trafilatura    │
    │ (News Search)   │              │ (AI Analysis)   │              │(Content Extract)│
    │                 │              │                 │              │                 │
    │ • Real-time     │              │ • GPT-4o-mini   │              │ • Article Text  │
    │ • Multi-country │              │ • Sentiment     │              │ • Date Mining   │
    │ • Date Filters  │              │ • Summarization │              │ • Clean Content │
    │ • Language Opt  │              │ • JSON Response │              │ • Metadata Ext  │
    └─────────────────┘              └─────────────────┘              └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               DATA FLOW PIPELINE                                │
└─────────────────────────────────────────────────────────────────────────────────┘

USER INPUT ──► SEARCH FORM ──► API CALL ──► FASTAPI ──► NEWS FETCHING ──► AI ANALYSIS ──► RESULTS

    │              │             │           │              │               │            │
    │              │             │           │              │               │            │
    ▼              ▼             ▼           ▼              ▼               ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐  ┌─────────┐  ┌─────────┐
│Entity   │  │Form     │  │HTTP     │  │Route    │  │Multi-Query  │  │Content  │  │AG-Grid │
│Country  │  │Valid-   │  │Request  │  │Handler  │  │Variants     │  │Analysis │  │Table   │
│Tags     │  │ation    │  │JSON     │  │Async    │  │Translation  │  │Sentiment│  │Filters │
│Dates    │  │Submit   │  │Payload  │  │Orchestr │  │Date Extract │  │Scoring  │  │Links   │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────────┘  └─────────┘  └─────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATE EXTRACTION HIERARCHY                          │
└─────────────────────────────────────────────────────────────────────────────────┘

                                ┌─────────────────┐
                                │  Article Input  │
                                │   (from Serper) │
                                └─────────────────┘
                                         │
                                         ▼
                         ┌─────────────────────────────────┐
                         │    1. Serper API Date Parse     │
                         │   parse_relative_date()         │
                         │   • English: "2 hours ago"      │
                         │   • Hindi: "2 घंटे पहले"        │
                         └─────────────────────────────────┘
                                         │
                                    ┌────┴────┐
                                    │ Success │
                                    └────┬────┘
                                    NO   │   YES
                                    ┌────▼────┐
                                    │         │
                                    ▼         ▼
                    ┌─────────────────────────────────┐     ┌─────────────────┐
                    │   2. URL Pattern Extract        │     │  Use Parsed     │
                    │   extract_date_from_url_or_     │     │     Date        │
                    │   title()                       │     │                 │
                    │   • /2025/11/08/ patterns       │     └─────────────────┘
                    │   • Title date extraction       │
                    └─────────────────────────────────┘
                                    │
                               ┌────┴────┐
                               │ Success │
                               └────┬────┘
                               NO   │   YES
                               ┌────▼────┐
                               │         │
                               ▼         ▼
           ┌─────────────────────────────────┐     ┌─────────────────┐
           │    3. Content Scraping          │     │  Use URL/Title  │
           │    extract_date_from_content()  │     │     Date        │
           │    • Full article download      │     │                 │
           │    • Multiple regex patterns    │     └─────────────────┘
           │    • Various date formats       │
           └─────────────────────────────────┘
                           │
                      ┌────┴────┐
                      │ Success │
                      └────┬────┘
                      NO   │   YES
                      ┌────▼────┐
                      │         │
                      ▼         ▼
        ┌─────────────────────────────────┐     ┌─────────────────┐
        │     4. Fallback Date            │     │ Use Content     │
        │     (Yesterday's Date)          │     │     Date        │
        │     • Last resort mechanism     │     │                 │
        │     • Reasonable estimate       │     └─────────────────┘
        └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          TECHNOLOGY STACK OVERVIEW                              │
└─────────────────────────────────────────────────────────────────────────────────┘

FRONTEND                    BACKEND                     EXTERNAL APIs
┌─────────────┐            ┌─────────────┐            ┌─────────────┐
│ React 18    │            │ FastAPI     │            │ Serper API  │
│ Material-UI │            │ Python 3.8+ │            │ Azure OpenAI│
│ AG-Grid     │     ◄──────┤ Async/Await │     ──────►│ Trafilatura │
│ Axios       │            │ Pydantic    │            │             │
│ Vite        │            │ HTTPX       │            │             │
└─────────────┘            └─────────────┘            └─────────────┘

FEATURES                   PROCESSING                  OUTPUT
┌─────────────┐            ┌─────────────┐            ┌─────────────┐
│ Dark Theme  │            │ Multi-lang  │            │ JSON API    │
│ Date Pickers│            │ Date Parsing│            │ Structured  │
│ Tag Chips   │     ◄──────┤ AI Analysis │     ──────►│ Data Table  │
│ Filtering   │            │ Content Ext │            │ Clickable   │
│ Pagination  │            │ Error Handle│            │ Links       │
└─────────────┘            └─────────────┘            └─────────────┘

```

---

## 📁 Project Structure & File Analysis

### 🖥️ Backend (`/backend/`)

#### **Core Application Files**

##### 1. `main.py` - FastAPI Server Entry Point
**Purpose**: Main FastAPI application with API endpoints and CORS configuration  
**Key Functions**:
- `root()` - Health check endpoint (`GET /`)
- `search_media(input_data)` - Main search endpoint (`POST /search`)

**Function Details**:
```python
@app.post("/search")
async def search_media(input_data: MediaSearchInput):
    # Step 1: Build query object from input parameters
    # Step 2: Fetch news articles using get_all_news_data()
    # Step 3: Analyze each article using analyze_article()
    # Step 4: Return structured results
```

**Dependencies**: 
- Uses `get_all_news_data()` from `api.ms.news`
- Uses `analyze_article()` from `analyzer`
- Handles MediaSearchInput model with entity, country, tags, date_range

##### 2. `analyzer.py` - AI Analysis Engine  
**Purpose**: Azure OpenAI integration for intelligent article analysis
**Key Functions**:
- `analyze_article(entity_name, entity_description, article)` - Main analysis function

**Function Details**:
```python
async def analyze_article(entity_name: str, entity_description: str, article: dict) -> dict:
    # Step 1: Extract content from article
    # Step 2: Build AI prompt with system/user messages
    # Step 3: Call Azure OpenAI API
    # Step 4: Parse JSON response
    # Step 5: Preserve original publish dates (priority over AI dates)
    # Step 6: Return structured analysis results
```

**Analysis Output**:
- `subjectMatchScore` (0-100): Relevance to entity
- `matchedDetails`: Specific phrases mentioning entity
- `tags`: 3-5 keywords describing content
- `sentiment`: positive/neutral/negative
- `crimeRelated`: Boolean crime detection
- `unethicalRelated`: Boolean unethical behavior detection
- `confidence`: Analysis confidence (0-100)
- `summary`: 2-3 sentence English summary
- `catchyTitle`: Attention-grabbing title
- `publishDate`: Preserved original or AI-generated date
- `isPaywalled`: Paywall detection

**Date Preservation Logic**: Always prioritizes original dates from news extraction over AI-generated dates

#### **API Module (`/backend/api/ms/`)**

##### 3. `news.py` - News Fetching & Date Processing Engine
**Purpose**: Serper API integration with comprehensive date extraction system
**Key Functions**:

**Date Processing Functions**:
```python
def parse_relative_date(date_str: str) -> str:
    # Converts relative dates ("2 hours ago", "58 मिनट पहले") to ISO format
    # Supports English and Hindi time expressions
    # Returns ISO formatted date string
```

```python
def extract_date_from_url_or_title(url: str, title: str = "") -> str:
    # Extracts dates from URL patterns (/2025/11/08/) 
    # Checks title for date patterns (Jan 8, 2025)
    # Lightweight fallback for missing dates
```

```python
def extract_date_from_content(content: str, url: str = "") -> str:
    # Scrapes publication dates from article content
    # Uses multiple regex patterns for date extraction
    # Handles various date formats (DD-MM-YYYY, Month DD, YYYY)
```

**Content Processing Functions**:
```python
def extract_full_content(url: str) -> str:
    # Uses trafilatura library for content extraction
    # Configured for news article optimization
    # Returns clean article text
```

**API Integration Functions**:
```python
async def translate_keywords(keywords: List[str], target_language: str) -> List[str]:
    # Translates search keywords using Azure OpenAI
    # Supports multilingual search capabilities
```

```python
def generate_query_variants(entity: str, tags: List[str], translated_tags: List[str]) -> List[str]:
    # Creates multiple search query combinations
    # Limits variants to prevent excessive API calls
```

```python
async def get_all_news_data(query: Dict) -> List[Dict]:
    # Main news fetching orchestrator
    # Handles multiple query variants and languages
    # Implements comprehensive date extraction pipeline
    # Returns processed article list with dates
```

**Date Extraction Pipeline**:
1. **Serper API Date**: Parse relative dates from API response
2. **URL Date Extraction**: Extract dates from URL patterns
3. **Content Date Mining**: Scrape dates from article content  
4. **Fallback Date**: Use yesterday's date as last resort

**Multi-Language Support**: Handles English and Hindi relative dates:
- English: "2 hours ago", "1 day ago", "3 weeks ago"
- Hindi: "2 घंटे पहले", "58 मिनट पहले", "1 दिन पहले"

##### 4. Other API Files
- `analysis.py` - Empty (placeholder for future analysis utilities)
- `models.py` - Empty (placeholder for data models)
- `utils.py` - Empty (placeholder for utility functions)

#### **Configuration (`/backend/cfg/`)**
- `config.py` - Empty (placeholder for app configuration)
- `logger.py` - Empty (placeholder for logging setup)

#### **Environment & Dependencies**
- `.env` - Environment variables (API keys, endpoints)
- `requirements.txt` - Python dependencies
- `.venv/` - Virtual environment (excluded from repository)

---

### 🖼️ Frontend (`/react-dashboard/`)

#### **Core Application Files**

##### 1. `src/App.jsx` - Main React Application
**Purpose**: Root component with theme configuration and state management
**Key Functions**:
- `handleSearch(searchParams)` - Orchestrates search API calls
- Theme configuration using Material-UI createTheme
- Global error and loading state management

**Component Structure**:
```jsx
function App() {
    // State: results, loading, error
    // Theme: Custom dark theme matching Streamlit aesthetic
    // Layout: Container with header, search form, results display
    // Error handling: User-friendly error messages
}
```

**Theme Features**:
- Dark mode with Streamlit-inspired colors
- Custom Material-UI component styling
- Consistent typography (Inter font family)
- Custom input field styling with focus states

##### 2. `src/main.jsx` - Application Entry Point
**Purpose**: React DOM rendering with date picker provider
**Dependencies**: DatePicker provider for MUI date components

#### **Components (`/src/components/`)**

##### 3. `SearchForm.jsx` - Search Interface Component
**Purpose**: User input form with validation and parameter handling
**Key Functions**:
- `handleInputChange(field, value)` - Updates search parameters
- `handleDateChange(field, date)` - Manages date range selection  
- `handleSubmit(e)` - Processes form submission and validation

**Form Features**:
```jsx
SearchForm Component:
    // Fields: entity (required), country, tags, date range
    // Validation: Entity required, valid date range
    // Tag processing: Comma-separated string to array conversion
    // Date handling: dayjs integration with Material-UI DatePicker
    // Countries: Predefined list [India, US, UK, Canada, Australia]
```

**User Experience**:
- Real-time tag visualization with chips
- Form validation with disabled states
- Date range constraints (from < to, max = today)
- Clear visual feedback for required fields

##### 4. `ResultsTable.jsx` - Data Visualization Component  
**Purpose**: AG-Grid table with advanced filtering matching Streamlit functionality
**Key Functions**:
- `processedData` (useMemo) - Transforms API results to table format
- `LinkCellRenderer` - Custom renderer for clickable article links
- Column definitions with filtering configuration

**Data Processing**:
```jsx
processedData Pipeline:
    // Input: Raw API results array
    // Serial numbering: Auto-generated S.No column
    // Date formatting: ISO → DD-MM-YYYY format
    // URL handling: Clickable links with validation
    // Field mapping: API fields → Table columns
    // Output: AG-Grid compatible data structure
```

**Column Configuration**:
```jsx
Column Definitions:
    S.No: Serial numbers (100px, center-aligned, bold)
    Title: Article titles (350px, clickable links)
    Source: News sources (140px, predefined filter values)  
    Date: Publication dates (110px, DD-MM-YYYY format)
    Catchy Title: AI-generated titles (280px)
    Summary: AI analysis summaries (300px)
    Match Score %: Relevance scoring (120px)
    Crime Related: Boolean indicators (110px, ✅/❌)
    Unethical Related: Boolean indicators (130px, ✅/❌)
    Sentiment: AI sentiment analysis (90px)
    URL: Hidden field for link functionality
```

**AG-Grid Features**:
- Set column filters with search boxes
- Pagination (15 rows per page)
- Column resizing and sorting
- Text selection enabled
- No auto-fit columns (preserves manual sizing)

#### **Services (`/src/services/`)**

##### 5. `api.js` - Backend Communication Layer
**Purpose**: Axios HTTP client for FastAPI integration
**Key Functions**:
- `searchMedia(searchParams)` - POST request to `/search` endpoint
- `healthCheck()` - GET request to `/` endpoint for server status

**Configuration**:
```javascript
API Client Setup:
    Base URL: http://localhost:8000
    Timeout: 300 seconds (5 minutes)
    Headers: Content-Type: application/json
    Error handling: Structured error message extraction
```

#### **Styling (`/src/styles/`)**
- `global.css` - Global CSS overrides and custom styles

#### **Build Configuration**
- `package.json` - Dependencies and scripts
- `vite.config.js` - Vite build configuration
- `index.html` - HTML template

---

## 🔗 Function Dependencies & Data Flow

### **Search Request Flow**
```
User Input (SearchForm.jsx)
    ↓ handleSubmit()
API Call (api.js)  
    ↓ searchMedia()
FastAPI Server (main.py)
    ↓ search_media()
News Fetching (news.py)
    ↓ get_all_news_data()
        ↓ Multiple query variants + languages
        ↓ Serper API calls
        ↓ Date extraction pipeline:
            • parse_relative_date()
            • extract_date_from_url_or_title() 
            • extract_date_from_content()
        ↓ extract_full_content() for missing dates
AI Analysis (analyzer.py)
    ↓ analyze_article() for each article
    ↓ Azure OpenAI API call
    ↓ Date preservation logic
Results Display (ResultsTable.jsx)
    ↓ processedData transformation
    ↓ AG-Grid rendering
```

### **Date Processing Hierarchy**
```
1. Serper API relative dates → parse_relative_date()
2. URL pattern extraction → extract_date_from_url_or_title()  
3. Content scraping → extract_date_from_content()
4. AI analysis dates → analyze_article() (lower priority)
5. Fallback date → yesterday's date
```

### **Cross-Component Communication**
```
App.jsx (State Manager)
    ↓ onSearch prop
SearchForm.jsx (Input Handler)
    ↓ API call result
App.jsx (State Update)
    ↓ results prop  
ResultsTable.jsx (Data Display)
```

---

## 🛠️ Key Technical Features

### **Backend Capabilities**
1. **Async Processing**: Concurrent article analysis using asyncio.gather()
2. **Multi-language Support**: English and Hindi date parsing + keyword translation
3. **Robust Date Extraction**: 4-layer fallback system for publication dates
4. **AI Integration**: Azure OpenAI for content analysis and sentiment detection
5. **Error Handling**: Comprehensive exception handling with user-friendly messages
6. **CORS Configuration**: Frontend-backend communication setup

### **Frontend Capabilities**  
1. **Real-time Validation**: Form validation with immediate feedback
2. **Advanced Data Table**: AG-Grid with Streamlit-equivalent filtering
3. **Responsive Design**: Material-UI responsive grid system
4. **Dark Theme**: Custom Streamlit-inspired theme
5. **Date Management**: MUI DatePicker with validation constraints
6. **Link Handling**: Clickable article URLs with security attributes

### **Data Processing Pipeline**
1. **Input Sanitization**: Tag processing and parameter validation
2. **Query Optimization**: Multiple search variants with translation
3. **Content Extraction**: Full article content when needed for dates
4. **AI Analysis**: Structured JSON output with confidence scoring
5. **Date Standardization**: Consistent DD-MM-YYYY formatting
6. **Result Aggregation**: Duplicate URL filtering and ranking

---

## 🚀 Future Development Areas

### **Backend Enhancements**
- Implement actual configuration in `config.py`
- Add structured logging in `logger.py`  
- Create data models in `models.py`
- Add utility functions in `utils.py`
- Implement caching for improved performance
- Add rate limiting and API quotas

### **Frontend Improvements**
- Add export functionality (PDF/Excel)
- Implement user authentication
- Add search history and bookmarks
- Create advanced analytics dashboard
- Implement real-time notifications
- Add mobile-responsive optimizations

### **Analysis Features**
- Machine learning for personalized recommendations
- Trend analysis and pattern detection
- Multi-source news aggregation
- Real-time sentiment monitoring
- Custom entity recognition
- Advanced filtering and sorting options

---

## 📋 Function Reference

### **Backend Functions by File**

#### `main.py`
- `root()` → Health check response
- `search_media(input_data)` → Main search orchestration

#### `analyzer.py`  
- `analyze_article(entity_name, entity_description, article)` → AI analysis results

#### `news.py`
- `parse_relative_date(date_str)` → ISO date from relative string
- `extract_date_from_url_or_title(url, title)` → Date from URL patterns  
- `extract_date_from_content(content, url)` → Date from article content
- `extract_full_content(url)` → Full article text via trafilatura
- `translate_keywords(keywords, target_language)` → Translated search terms
- `generate_query_variants(entity, tags, translated_tags)` → Query combinations
- `get_all_news_data(query)` → Complete news fetching pipeline

### **Frontend Functions by File**

#### `App.jsx`
- `handleSearch(searchParams)` → Search orchestration and state management

#### `SearchForm.jsx`  
- `handleInputChange(field, value)` → Form field updates
- `handleDateChange(field, date)` → Date range management
- `handleSubmit(e)` → Form submission and validation

#### `ResultsTable.jsx`
- `processedData` (useMemo) → API data transformation  
- `LinkCellRenderer(props)` → Clickable link component
- Column definitions → AG-Grid configuration

#### `api.js`
- `searchMedia(searchParams)` → Backend search API call
- `healthCheck()` → Server status verification

---

This comprehensive project draft provides complete visibility into your Media Search & Analysis Platform, documenting every folder, file, function, and their interactions. The system demonstrates sophisticated news processing capabilities with AI-powered analysis and professional-grade data visualization.