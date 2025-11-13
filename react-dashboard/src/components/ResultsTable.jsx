import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { Box, Typography, Paper } from '@mui/material';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

// Custom cell renderer component for clickable links
const LinkCellRenderer = (props) => {
  const { data, value } = props;
  
  if (data.URL && data.URL !== '#') {
    return (
      <a 
        href={data.URL} 
        target="_blank" 
        rel="noopener noreferrer"
        style={{ 
          color: '#1f77b4', 
          textDecoration: 'underline', 
          cursor: 'pointer' 
        }}
      >
        {value}
      </a>
    );
  }
  
  return <span>{value}</span>;
};

const ResultsTable = ({ results, loading }) => {
  // Process data exactly like Streamlit
  const processedData = useMemo(() => {
    if (!results || !Array.isArray(results)) return [];
    
    return results.map((article, index) => {
      // Format date exactly like Streamlit
      let publishedDate = "N/A";
      
      const rawDate = article.publishDate;
      if (rawDate && rawDate !== "N/A" && rawDate.trim() !== "" && rawDate !== "null" && rawDate !== null) {
        try {
          // Handle ISO format dates (2025-11-10T13:27:53.937777Z)
          let dateToProcess = rawDate;
          
          // Clean up the date string if needed
          if (typeof dateToProcess === 'string') {
            dateToProcess = dateToProcess.trim();
          }
          
          const parsed = new Date(dateToProcess);
          
          // Validate the parsed date
          if (!isNaN(parsed.getTime()) && parsed.getFullYear() > 1900 && parsed.getFullYear() < 2100) {
            // Format as DD-MM-YYYY like Streamlit
            const day = String(parsed.getDate()).padStart(2, '0');
            const month = String(parsed.getMonth() + 1).padStart(2, '0');
            const year = String(parsed.getFullYear());
            
            // Ensure all components are valid
            if (day && month && year && day !== "NaN" && month !== "NaN" && year !== "NaN") {
              publishedDate = `${day}-${month}-${year}`;
            }
          }
        } catch (error) {
          console.log(`Date parsing error for: ${rawDate}`, error);
        }
      }

      const processedItem = {
        "S.No": index + 1,
        "Title": article.originalTitle || "No title",
        "URL": article.url || "#",
        "Source": article.source || "Unknown",
        "Date": publishedDate,
        "Catchy Title": article.catchyTitle || "No catchy title",
        "Summary": article.summary || "No summary available.",
        "Match Score %": article.subjectMatchScore || 0,
        "Crime Related": article.crimeRelated ? "✅" : "❌",
        "Unethical Related": article.unethicalRelated ? "✅" : "❌",
        "Sentiment": article.sentiment || "N/A"
      };
      
      // Debug: log first few items to check S.No values
      if (index < 3) {
        console.log(`Row ${index + 1} - S.No:`, processedItem["S.No"]);
      }
      
      return processedItem;
    });
  }, [results]);

  // Column definitions with set filters like your screenshot
  const columnDefs = useMemo(() => [
    {
      field: "S.No",
      headerName: "Serial No",
      width: 100,
      minWidth: 100,
      filter: false,
      sortable: true,
      resizable: true,
      cellStyle: { 
        textAlign: 'center',
        fontWeight: 'bold',
        fontSize: '14px'
      },
      valueGetter: (params) => {
        console.log('S.No valueGetter:', params.data);
        return params.data ? params.data["S.No"] : undefined;
      }
    },
    {
      field: "Title",
      width: 350,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      wrapText: true,
      autoHeight: true,
      cellRenderer: (params) => {
        const { data, value } = params;
        
        const formatResponsiveText = (text, targetLines = 2) => {
          if (!text) return "No title available";
          
          const words = text.split(' ');
          
          // For shorter text, don't force line breaks
          if (words.length <= 6) {
            return text;
          }
          
          // Calculate approximate words per line based on column width
          // Assuming average character width and column width
          const columnWidth = params.column.getActualWidth();
          const avgCharWidth = 8; // Approximate character width in pixels
          const padding = 20; // Account for cell padding
          const availableWidth = columnWidth - padding;
          const avgWordLength = 6; // Average word length
          const wordsPerLine = Math.max(1, Math.floor(availableWidth / (avgWordLength * avgCharWidth)));
          
          // Split into lines based on available width
          const lines = [];
          for (let i = 0; i < words.length; i += wordsPerLine) {
            lines.push(words.slice(i, i + wordsPerLine).join(' '));
            if (lines.length >= targetLines) {
              // If we have enough lines, put remaining words in last line
              if (i + wordsPerLine < words.length) {
                lines[lines.length - 1] += ' ' + words.slice(i + wordsPerLine).join(' ');
              }
              break;
            }
          }
          
          return lines.join('\n');
        };
        
        const formattedTitle = formatResponsiveText(value, 2);
        
        if (data.URL && data.URL !== '#') {
          return (
            <a 
              href={data.URL} 
              target="_blank" 
              rel="noopener noreferrer"
              style={{ 
                color: '#1f77b4', 
                textDecoration: 'underline', 
                cursor: 'pointer',
                whiteSpace: 'pre-wrap',
                lineHeight: '1.4',
                display: 'block',
                padding: '4px 0',
                wordBreak: 'break-word',
                overflowWrap: 'break-word'
              }}
            >
              {formattedTitle}
            </a>
          );
        }
        
        return (
          <div style={{ 
            whiteSpace: 'pre-wrap', 
            lineHeight: '1.4',
            padding: '4px 0',
            wordBreak: 'break-word',
            overflowWrap: 'break-word'
          }}>
            {formattedTitle}
          </div>
        );
      },
      menuTabs: ['filterMenuTab'],
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep',
        buttons: ['reset', 'apply']
      }
    },
    {
      field: "Source",
      width: 140,
      filter: 'agSetColumnFilter',
      floatingFilter: false,
      sortable: true,
      resizable: true,
      filterParams: {
        values: ['Navbharat', 'News Today', 'Newsonair', 'PIB', 'DIP', 'Jagran', 'India Education'],
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Date",
      width: 110,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      menuTabs: ['filterMenuTab'],
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep',
        buttons: ['reset', 'apply']
      }
    },
    {
      field: "Catchy Title",
      width: 280,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      wrapText: true,
      autoHeight: false,
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Summary",
      width: 300,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      wrapText: true,
      autoHeight: true,
      cellRenderer: (params) => {
        const formatResponsiveSummary = (text) => {
          if (!text) return "No summary available.";
          
          const words = text.split(' ');
          
          // Calculate words per line based on column width
          const columnWidth = params.column.getActualWidth();
          const avgCharWidth = 8; // Approximate character width in pixels
          const padding = 20; // Account for cell padding
          const availableWidth = columnWidth - padding;
          const avgWordLength = 6; // Average word length
          const wordsPerLine = Math.max(3, Math.floor(availableWidth / (avgWordLength * avgCharWidth)));
          
          // Split text into lines based on available width
          const lines = [];
          for (let i = 0; i < words.length; i += wordsPerLine) {
            lines.push(words.slice(i, i + wordsPerLine).join(' '));
          }
          
          return lines.join('\n');
        };
        
        return (
          <div style={{ 
            whiteSpace: 'pre-wrap', 
            lineHeight: '1.4',
            padding: '4px 0',
            wordBreak: 'break-word',
            overflowWrap: 'break-word'
          }}>
            {formatResponsiveSummary(params.value)}
          </div>
        );
      },
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Match Score %",
      width: 120,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      hide: true,
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Crime Related",
      width: 110,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      filterParams: {
        values: ['✅', '❌'],
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Unethical Related",
      width: 130,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      hide: true,
      filterParams: {
        values: ['✅', '❌'],
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "Sentiment",
      width: 90,
      filter: 'agSetColumnFilter',
      sortable: true,
      resizable: true,
      hide:true,
      filterParams: {
        suppressMiniFilter: false,  // Show search box
        suppressSelectAll: false,   // Show "(Select All)"
        newRowsAction: 'keep'
      }
    },
    {
      field: "URL",
      hide: true // Hidden but kept in data for links
    }
  ], []);

  // Default column definition
  const defaultColDef = useMemo(() => ({
    sortable: true,
    resizable: true,
    wrapText: true,
    autoHeight: false,
    floatingFilter: false
  }), []);

  // Grid options
  const gridOptions = useMemo(() => ({
    pagination: true,
    paginationAutoPageSize: false,
    paginationPageSize: 15,
    suppressMenuHide: false,
    enableCellTextSelection: true,
    suppressRowClickSelection: true,
    enableFilter: true,
    suppressHeaderFilterButton: false  // Make sure filter icons are shown
  }), []);

  if (loading) {
    return (
      <Paper sx={{ p: 3 }}>
        <div className="loading-spinner">
          🔄 Searching and analyzing articles...
        </div>
      </Paper>
    );
  }

  if (!results || results.length === 0) {
    return null;
  }

  return (
    <Paper sx={{ p: 0, borderRadius: 2 }}>
      <Box className="results-header" sx={{ px: 3, py: 2, borderBottom: '1px solid #4a4a4a' }}>
        <Typography variant="h6" sx={{ color: '#fafafa' }}>
          📊 Search Results ({results.length} articles found)
        </Typography>
      </Box>
      
      <Box sx={{ height: 600, width: '100%' }}>
        <AgGridReact
          rowData={processedData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          gridOptions={gridOptions}
          className="ag-theme-alpine"
          onGridReady={(params) => {
            // Don't auto-fit columns on load like Streamlit
            // params.api.sizeColumnsToFit();
          }}
        />
      </Box>
    </Paper>
  );
};

export default ResultsTable;