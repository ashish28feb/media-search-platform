import React from 'react';
import { Box, Paper, Typography, Button } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Unauthorized = () => {
  const { logout, user } = useAuth();

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
      <Paper sx={{ p: 6, maxWidth: 500, width: '100%', textAlign: 'center' }}>
        <Typography variant="h5" sx={{ mb: 2, color: '#fafafa' }}>
          🚫 Access Denied
        </Typography>
        
        <Typography variant="body1" sx={{ mb: 2, color: '#a6a6a6' }}>
          Hello {user?.name || 'User'}, your account ({user?.email}) is not authorized to access this application.
        </Typography>

        <Typography variant="body2" sx={{ mb: 4, color: '#666' }}>
          Please contact the administrator to request access to the Media Search Dashboard.
        </Typography>

        <Button
          variant="outlined"
          onClick={logout}
          sx={{
            borderColor: '#ff4b4b',
            color: '#ff4b4b',
            '&:hover': {
              borderColor: '#e13e3e',
              backgroundColor: 'rgba(255, 75, 75, 0.1)',
            },
          }}
        >
          Sign Out
        </Button>
      </Paper>
    </Box>
  );
};

export default Unauthorized;