import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Alert,
  Button,
  AppBar,
  Toolbar,
} from '@mui/material';
import SearchForm from './SearchForm';
import ResultsTable from './ResultsTable';
import { searchMedia } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (searchParams) => {
    setLoading(true);
    setError('');
    setResults([]);

    try {
      console.log('Searching with params:', searchParams);
      const response = await searchMedia(searchParams);
      
      setResults(response.results || []);
      console.log(`Found ${response.results?.length || 0} articles`);
    } catch (err) {
      console.error('Search error:', err);
      setError(err.message || 'An error occurred while searching');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Top Navigation Bar */}
      <AppBar position="static" sx={{ backgroundColor: '#1a1a1a', mb: 2 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            📰 Media Search Dashboard
          </Typography>
          <Typography variant="body2" sx={{ mr: 2, color: '#a6a6a6' }}>
            Welcome, {user?.name}
          </Typography>
          <Button 
            color="inherit" 
            onClick={logout}
            sx={{ color: '#ff4b4b' }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          {/* Header */}
          <Paper sx={{ p: 4, mb: 4, textAlign: 'center' }}>
            <Typography variant="h4" sx={{ mb: 2, color: '#fafafa' }}>
              📰 Media Search & Analysis Dashboard
            </Typography>
            <Typography variant="body1" sx={{ color: '#a6a6a6', maxWidth: '800px', mx: 'auto' }}>
              Search for news articles, analyze their content, and filter results with advanced criteria. 
              Get AI-powered insights including sentiment analysis, crime detection, and relevance scoring.
            </Typography>
          </Paper>

          {/* Search Form */}
          <SearchForm onSearch={handleSearch} loading={loading} />

          {/* Error Display */}
          {error && (
            <Box sx={{ mt: 3 }}>
              <Alert severity="error" sx={{ backgroundColor: '#dc2626', color: '#fafafa' }}>
                {error}
              </Alert>
            </Box>
          )}

          {/* Loading State */}
          {loading && (
            <Box sx={{ mt: 4 }}>
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  🔍 Searching and Analyzing Articles...
                </Typography>
                <Typography variant="body2" sx={{ color: '#a6a6a6' }}>
                  This may take a few moments while we fetch and analyze the latest news articles.
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <div className="loading-spinner">⏳</div>
                </Box>
              </Paper>
            </Box>
          )}

          {/* Results */}
          {!loading && results.length > 0 && (
            <Box sx={{ mt: 4 }}>
              <ResultsTable results={results} loading={loading} />
            </Box>
          )}

          {/* No Results */}
          {!loading && !error && results.length === 0 && (
            <Box sx={{ mt: 4 }}>
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 2, color: '#a6a6a6' }}>
                  🔍 Ready to Search
                </Typography>
                <Typography variant="body2" sx={{ color: '#a6a6a6' }}>
                  Enter your search terms above and click "Search Articles" to get started.
                </Typography>
              </Paper>
            </Box>
          )}
        </Box>
      </Container>
    </>
  );
};

export default Dashboard;