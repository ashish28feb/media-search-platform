import React, { useEffect, useState } from 'react';
import { Box, Paper, Typography, Button, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const { login } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Initialize Google Sign-In
    if (window.google) {
      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        callback: handleGoogleSignIn,
      });

      window.google.accounts.id.renderButton(
        document.getElementById('google-signin-button'),
        {
          theme: 'outline',
          size: 'large',
          width: 300,
          text: 'signin_with',
        }
      );
    }
  }, []);

  const handleGoogleSignIn = async (response) => {
    setLoading(true);
    setError('');

    const result = await login(response.credential);
    
    if (!result.success) {
      setError(result.message || 'Login failed. Please try again.');
    }
    
    setLoading(false);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#0e1117',
      }}
    >
      <Paper sx={{ p: 6, maxWidth: 400, width: '100%', textAlign: 'center' }}>
        <Typography variant="h4" sx={{ mb: 2, color: '#fafafa' }}>
          📰 Media Search
        </Typography>
        
        <Typography variant="body1" sx={{ mb: 4, color: '#a6a6a6' }}>
          Sign in to access the news search and analysis dashboard
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mb: 3 }}>
          <div id="google-signin-button"></div>
        </Box>

        {loading && (
          <Typography variant="body2" sx={{ color: '#a6a6a6' }}>
            Signing you in...
          </Typography>
        )}
        
        <Typography variant="caption" sx={{ color: '#666', mt: 2, display: 'block' }}>
          Access is restricted to authorized users only
        </Typography>
      </Paper>
    </Box>
  );
};

export default Login;