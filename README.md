# Media Search & Analysis Platform

A comprehensive news search and AI-powered analysis platform that fetches real-time news articles and provides intelligent insights with a modern React dashboard interface.

## 🚀 Features

### Core Functionality
- **Real-time News Search**: Search news articles by entity, country, and custom tags
- **AI-Powered Analysis**: Advanced sentiment analysis and content summarization using Azure OpenAI
- **Smart Date Filtering**: Search articles within specific date ranges
- **Multi-language Support**: Handles English and Hindi content with intelligent date parsing
- **Clickable Articles**: Direct links to original news sources
- **Advanced Filtering**: Column-based filtering similar to Excel/Google Sheets

### Technical Features  
- **Comprehensive Date Extraction**: Multi-layer date parsing system supporting:
  - Hindi relative dates ("2 घंटे पहले", "58 मिनट पहले")
  - URL-based date extraction
  - Content scraping for publication dates
  - Fallback date generation
- **Dark Theme UI**: Modern Material-UI dark theme interface
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Real-time Updates**: Live data fetching with loading states
- **Error Handling**: Robust error management and user feedback

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with automatic API documentation
- **News API**: Serper API integration for real-time news data
- **AI Integration**: Azure OpenAI for content analysis
- **CORS Support**: Cross-origin resource sharing enabled
- **Async Processing**: Non-blocking API calls for better performance

### Frontend (React + Vite)
- **Framework**: React 18 with Vite for fast development
- **Table Component**: AG-Grid for advanced data visualization
- **UI Library**: Material-UI for consistent design
- **HTTP Client**: Axios for API communication
- **Build Tool**: Vite for optimized production builds

## 📁 Project Structure

```
media_search/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main FastAPI application
│   ├── analyzer.py            # AI analysis engine
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── cfg/                   # Configuration modules
│   │   ├── config.py          # App configuration
│   │   └── logger.py          # Logging setup
│   └── api/                   # API modules
│       └── ms/                # Media Search modules
│           ├── analysis.py    # Analysis utilities
│           ├── models.py      # Data models
│           ├── news.py        # News fetching & date extraction
│           └── utils.py       # Helper utilities
├── react-dashboard/           # React Frontend
│   ├── src/
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # App entry point
│   │   ├── components/       # React components
│   │   │   ├── SearchForm.jsx    # Search interface
│   │   │   └── ResultsTable.jsx  # Data table with AG-Grid
│   │   ├── services/         # API services
│   │   │   └── api.js        # Backend communication
│   │   └── styles/           # CSS styles
│   │       └── global.css    # Global styling
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   └── index.html            # HTML template
└── .gitignore                # Git ignore patterns
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+**: For backend development
- **Node.js 16+**: For frontend development  
- **API Keys**: Serper API and Azure OpenAI credentials

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
Create `.env` file with:
```env
SERPER_API_KEY=your_serper_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

5. **Start the backend server**:
```bash
uvicorn main:app --reload
```
Backend will run on: `http://localhost:8000`

### Frontend Setup

1. **Navigate to React dashboard**:
```bash
cd react-dashboard
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```
Frontend will run on: `http://localhost:5173`

## 📊 API Endpoints

### POST `/search`
Search for news articles with advanced filtering.

**Request Body**:
```json
{
  "entity": "Technology",
  "country": "India", 
  "tags": ["AI", "Machine Learning"],
  "date_range": {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "S.No": 1,
      "originalTitle": "Article Title",
      "source": "News Source", 
      "link": "https://example.com/article",
      "publishDate": "10-11-2024",
      "snippet": "Article preview...",
      "analysis": {
        "sentiment": "positive",
        "summary": "AI-generated summary",
        "tags": ["tech", "innovation"]
      }
    }
  ]
}
```

## 🔧 Key Components

### News Fetching (`news.py`)
- **Serper API Integration**: Real-time news data retrieval
- **Date Extraction Engine**: Multi-layer date parsing system
- **Content Processing**: Article content extraction and cleaning
- **Error Handling**: Robust fallback mechanisms

### AI Analysis (`analyzer.py`) 
- **Sentiment Analysis**: Emotional tone detection
- **Content Summarization**: Key point extraction
- **Tag Generation**: Automatic keyword tagging
- **Date Preservation**: Maintains original publication dates

### React Table (`ResultsTable.jsx`)
- **AG-Grid Integration**: Advanced data table functionality  
- **Column Filtering**: Excel-like filtering capabilities
- **Clickable Links**: Direct navigation to news sources
- **Custom Rendering**: Styled serial numbers and dates
- **Responsive Design**: Mobile-friendly table layout

### Search Interface (`SearchForm.jsx`)
- **Dynamic Forms**: Real-time input validation
- **Date Pickers**: Intuitive date range selection
- **Tag Management**: Add/remove search tags
- **Loading States**: Visual feedback during searches

## 🌟 Advanced Features

### Date Intelligence
- **Multi-language Parsing**: English and Hindi date formats
- **Relative Date Processing**: "2 hours ago" → actual timestamps  
- **URL Date Extraction**: Parse dates from article URLs
- **Content Date Mining**: Extract publication dates from article content
- **Smart Fallbacks**: Generate reasonable dates when none found

### Performance Optimizations
- **Async Processing**: Non-blocking API calls
- **Efficient Rendering**: React optimizations for large datasets
- **Caching Strategy**: Reduce redundant API calls
- **Lazy Loading**: Load data as needed

### Error Handling
- **Graceful Degradation**: Fallback for missing data
- **User Feedback**: Clear error messages and loading states
- **Retry Logic**: Automatic retry for failed requests
- **Validation**: Input sanitization and validation

## 🚀 Production Deployment

### Backend Deployment
```bash
# Build for production
pip install -r requirements.txt

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment  
```bash
# Build for production
npm run build

# Serve static files
npm run preview
```

## 🔒 Security & Environment

- **Environment Variables**: Secure API key management
- **CORS Configuration**: Controlled cross-origin access  
- **Input Validation**: Sanitized user inputs
- **Error Sanitization**: No sensitive data in error responses

## 📈 Future Enhancements

- **User Authentication**: Personal search history
- **Advanced Analytics**: Trend analysis and insights
- **Export Functionality**: PDF/Excel export options
- **Real-time Notifications**: Alert system for breaking news
- **Multi-source Integration**: Additional news APIs
- **Machine Learning**: Personalized content recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the GitHub Issues page
- Review API documentation at `http://localhost:8000/docs`  
- Ensure all environment variables are properly configured

---

**Built with ❤️ using FastAPI, React, and AI technologies**