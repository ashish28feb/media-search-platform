# 📰 Media Search & Analysis Dashboard

A modern React-based dashboard for searching and analyzing news articles with AI-powered insights.

## ✨ Features

- **🔍 Advanced Search**: Search articles by keywords, date ranges, and geographic locations
- **📊 Data Table**: Interactive AG-Grid table with sorting, filtering, and pagination
- **🎯 AI Analysis**: Get sentiment analysis, crime detection, and relevance scoring
- **🔗 Clickable Links**: Direct access to original articles
- **🌙 Dark Theme**: Professional Streamlit-inspired dark interface
- **📱 Responsive**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies:**
   ```bash
   cd react-dashboard
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open in browser:**
   ```
   http://localhost:5173
   ```

## 📋 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🏗️ Architecture

### Components

- **`App.jsx`** - Main application component with theme and state management
- **`SearchForm.jsx`** - Search interface with validation and date pickers
- **`ResultsTable.jsx`** - AG-Grid table with custom renderers and filtering

### Services

- **`api.js`** - Axios-based API client for backend communication

### Styling

- **Material-UI** - Component library with custom dark theme
- **AG-Grid** - Professional data table with custom Streamlit theme
- **Inter Font** - Modern typography matching Streamlit design

## 🎨 Theme

The dashboard uses a custom dark theme inspired by Streamlit:

- **Background**: `#0e1117` (Streamlit dark background)
- **Paper**: `#1a1a1a` (Card/table background)
- **Primary**: `#0ea5e9` (Sky blue for accents)
- **Text**: `#fafafa` (High contrast white)
- **Secondary**: `#a6a6a6` (Muted gray)

## 📊 Table Features

### Columns

1. **S.No** - Row numbers (pinned left)
2. **Title** - Clickable article titles (pinned left)
3. **Source** - Publication source
4. **Date** - Publication date with sorting
5. **Catchy Title** - AI-generated catchy headlines
6. **Summary** - AI-generated summaries
7. **Match Score** - Relevance percentage with visual bar
8. **Crime Related** - Boolean indicator with chips
9. **Unethical Related** - Boolean indicator with chips
10. **Sentiment** - Color-coded sentiment analysis

### Interactions

- **🔄 Sorting**: Click column headers to sort
- **🔍 Filtering**: Use filter icons in column headers
- **📄 Pagination**: Navigate through large result sets
- **🔗 Links**: Click article titles to open in new tabs
- **📱 Responsive**: Table adapts to screen size

## 🔧 Configuration

### API Endpoint

Update the API base URL in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Styling Customization

Modify the theme in `src/App.jsx` or update AG-Grid styles in `src/styles/global.css`.

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure backend is running on `http://localhost:8000`
   - Check CORS settings in FastAPI backend

2. **Table Not Loading**
   - Check browser console for JavaScript errors
   - Verify API response format matches expected structure

3. **Styling Issues**
   - Clear browser cache and refresh
   - Check for CSS conflicts in developer tools

## 🔄 Backend Integration

The dashboard expects the following API structure:

```javascript
// POST /api/search
{
  "query": "search terms",
  "location": "optional location",
  "dateFrom": "2024-01-01",
  "dateTo": "2024-01-31"
}

// Response
{
  "success": true,
  "data": [
    {
      "originalTitle": "Article title",
      "url": "https://example.com/article",
      "source": "News Source",
      "publishDate": "2024-01-15",
      "catchyTitle": "AI-generated catchy title",
      "summary": "AI-generated summary",
      "subjectMatchScore": 85.5,
      "crimeRelated": false,
      "unethicalRelated": true,
      "sentiment": "positive"
    }
  ]
}
```

## 🚀 Production Deployment

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Deploy the `dist/` folder** to your web server

3. **Configure reverse proxy** to handle API requests

## 📦 Dependencies

### Core
- React 18
- Material-UI 5
- AG-Grid React
- Axios
- Day.js

### Development
- Vite
- ESLint
- @vitejs/plugin-react

## 📄 License

This project is licensed under the MIT License.