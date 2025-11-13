import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { Search as SearchIcon, Clear as ClearIcon } from '@mui/icons-material';
import dayjs from 'dayjs';

const SearchForm = ({ onSearch, loading, error, onClearResults }) => {
  const [searchParams, setSearchParams] = useState({
    entity: '',
    country: 'None',
    tags: '',
    date_range: {
      from_date: dayjs().subtract(1, 'month').format('YYYY-MM-DD'),
      to_date: dayjs().format('YYYY-MM-DD'),
    },
  });

  const [fromDate, setFromDate] = useState(dayjs().subtract(1, 'month'));
  const [toDate, setToDate] = useState(dayjs());

  const handleInputChange = (field, value) => {
    setSearchParams(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleDateChange = (field, date) => {
    if (field === 'from_date') {
      setFromDate(date);
    } else {
      setToDate(date);
    }
    
    setSearchParams(prev => ({
      ...prev,
      date_range: {
        ...prev.date_range,
        [field]: date ? date.format('YYYY-MM-DD') : '',
      },
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!searchParams.entity.trim()) {
      return;
    }

    const tagsArray = searchParams.tags
      ? searchParams.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      : [];

    const searchData = {
      entity: searchParams.entity.trim(),
      country: searchParams.country,
      tags: tagsArray,
      date_range: searchParams.date_range,
    };

    onSearch(searchData);
  };

  const isFormValid = searchParams.entity.trim() && fromDate && toDate && fromDate.isBefore(toDate);

  const countries = ['None', 'India', 'US', 'UK', 'Canada', 'Australia','China'];

  return (
    <Paper className="search-form" elevation={2}>
      <Typography variant="h6" gutterBottom sx={{ color: '#fafafa', mb: 3 }}>
        🔍 Search Parameters
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Entity Name"
              placeholder="e.g., John Doe, Company Name"
              value={searchParams.entity}
              onChange={(e) => handleInputChange('entity', e.target.value)}
              required
              variant="outlined"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Country</InputLabel>
              <Select
                value={searchParams.country}
                onChange={(e) => handleInputChange('country', e.target.value)}
                label="Country"
              >
                {countries.map((country) => (
                  <MenuItem key={country} value={country}>
                    {country}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Tags (comma-separated)"
              placeholder="e.g., fraud, corruption, investigation"
              value={searchParams.tags}
              onChange={(e) => handleInputChange('tags', e.target.value)}
              helperText="Enter relevant keywords separated by commas"
            />
            {searchParams.tags && (
              <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {searchParams.tags.split(',').map((tag, index) => (
                  tag.trim() && (
                    <Chip
                      key={index}
                      label={tag.trim()}
                      size="small"
                      color="primary"
                    />
                  )
                ))}
              </Box>
            )}
          </Grid>

          <Grid item xs={12} md={6}>
            <DatePicker
              label="From Date"
              value={fromDate}
              onChange={(date) => handleDateChange('from_date', date)}
              maxDate={dayjs()}
              slotProps={{
                textField: {
                  fullWidth: true,
                  required: true,
                },
              }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <DatePicker
              label="To Date"
              value={toDate}
              onChange={(date) => handleDateChange('to_date', date)}
              minDate={fromDate}
              maxDate={dayjs()}
              slotProps={{
                textField: {
                  fullWidth: true,
                  required: true,
                },
              }}
            />
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
              <Button
                type="button"
                variant="outlined"
                startIcon={<ClearIcon />}
                onClick={onClearResults}
                disabled={loading}
              >
                Clear Results
              </Button>
              <Button
                type="submit"
                variant="contained"
                startIcon={<SearchIcon />}
                disabled={!isFormValid || loading}
                sx={{
                  backgroundColor: '#ff4b4b',
                  '&:hover': {
                    backgroundColor: '#e13e3e',
                  },
                }}
              >
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default SearchForm;