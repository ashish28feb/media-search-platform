import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import App from './App.jsx'
import './styles/global.css'

// Streamlit-inspired theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff4b4b',
    },
    secondary: {
      main: '#0068c9',
    },
    background: {
      default: '#0e1117',
      paper: '#262730',
    },
    text: {
      primary: '#fafafa',
      secondary: '#a6a6a6',
    },
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
    h1: {
      fontSize: '3.5rem',
      fontWeight: 700,
      color: '#fafafa',
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      color: '#fafafa',
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '6px',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#262730',
            '& fieldset': {
              borderColor: '#4a4a4a',
            },
            '&:hover fieldset': {
              borderColor: '#ff4b4b',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#ff4b4b',
            },
          },
        },
      },
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <App />
      </LocalizationProvider>
    </ThemeProvider>
  </React.StrictMode>,
)