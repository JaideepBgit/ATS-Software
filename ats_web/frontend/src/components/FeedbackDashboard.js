import { useState, useEffect } from 'react';
import {
  Box, Paper, Typography, Grid, Card, CardContent, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Chip, LinearProgress, Button, TextField, IconButton, Tooltip,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import DownloadIcon from '@mui/icons-material/Download';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

function FeedbackDashboard({ open, onClose }) {
  const [stats, setStats] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) {
      loadStatistics();
    }
  }, [open]);

  const loadStatistics = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/feedback/statistics');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.get('/api/feedback/search', {
        params: { query: searchQuery, n_results: 10 }
      });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    // Trigger CSV export
    window.open('/api/feedback/export-csv', '_blank');
  };

  const getRatingColor = (rating) => {
    if (rating >= 4) return '#4caf50';
    if (rating >= 3) return '#ff9800';
    return '#f44336';
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: {
          minHeight: '80vh',
          backgroundColor: '#FBFAFA'
        }
      }}
    >
      <DialogTitle sx={{ color: '#3B1C55', pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Feedback Database Dashboard</Typography>
          <Box>
            <Tooltip title="Refresh">
              <IconButton onClick={loadStatistics} disabled={loading}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            <IconButton onClick={onClose}>
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
      </DialogTitle>

      <DialogContent>
        {loading && <LinearProgress sx={{ mb: 2 }} />}

        {/* Statistics Cards */}
        {stats && (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ backgroundColor: 'rgba(99, 51, 148, 0.1)' }}>
                <CardContent>
                  <Typography variant="h4" sx={{ color: '#633394', fontWeight: 'bold' }}>
                    {stats.total_feedback}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Feedback
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ backgroundColor: 'rgba(255, 152, 0, 0.1)' }}>
                <CardContent>
                  <Typography variant="h4" sx={{ color: '#ff9800', fontWeight: 'bold' }}>
                    {stats.average_rating.toFixed(1)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Average Rating
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ backgroundColor: 'rgba(76, 175, 80, 0.1)' }}>
                <CardContent>
                  <Typography variant="h4" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
                    {stats.chromadb_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    ChromaDB Entries
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ backgroundColor: 'rgba(33, 150, 243, 0.1)' }}>
                <CardContent>
                  <Typography variant="h4" sx={{ color: '#2196f3', fontWeight: 'bold' }}>
                    {stats.faiss_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    FAISS Index
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {/* Search */}
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55' }}>
            Search Feedback
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search for similar feedback..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              disabled={loading || !searchQuery.trim()}
              startIcon={<SearchIcon />}
              sx={{
                backgroundColor: '#633394',
                '&:hover': { backgroundColor: '#3B1C55' }
              }}
            >
              Search
            </Button>
          </Box>

          {/* Search Results */}
          {searchResults && searchResults.documents && searchResults.documents[0] && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Found {searchResults.documents[0].length} similar entries:
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Similarity</TableCell>
                      <TableCell>Rating</TableCell>
                      <TableCell>Query</TableCell>
                      <TableCell>Response</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {searchResults.documents[0].map((doc, index) => {
                      const metadata = searchResults.metadatas[0][index];
                      const distance = searchResults.distances[0][index];
                      const similarity = (1 - distance) * 100;

                      return (
                        <TableRow key={index}>
                          <TableCell>
                            <Chip
                              label={`${similarity.toFixed(0)}%`}
                              size="small"
                              sx={{
                                backgroundColor: similarity > 80 ? 'rgba(76, 175, 80, 0.2)' : 'rgba(255, 152, 0, 0.2)',
                                color: similarity > 80 ? '#2e7d32' : '#e65100'
                              }}
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                              {'⭐'.repeat(metadata.rating)}
                            </Box>
                          </TableCell>
                          <TableCell sx={{ maxWidth: 200 }}>
                            <Typography variant="body2" noWrap>
                              {metadata.query}
                            </Typography>
                          </TableCell>
                          <TableCell sx={{ maxWidth: 300 }}>
                            <Typography variant="body2" noWrap>
                              {metadata.response}
                            </Typography>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}
        </Paper>

        {/* Database Location Info */}
        <Paper sx={{ p: 2, backgroundColor: 'rgba(59, 28, 85, 0.05)' }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55' }}>
            Database Locations
          </Typography>
          <Box sx={{ pl: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              📁 <strong>ChromaDB:</strong> <code>backend/feedback_db/chroma/</code>
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              📁 <strong>FAISS Index:</strong> <code>backend/feedback_db/faiss_index.bin</code>
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              📁 <strong>JSONL Backup:</strong> <code>backend/feedback_db/interactions.jsonl</code>
            </Typography>
          </Box>

          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              View database from command line:
            </Typography>
            <Box sx={{ 
              p: 1, 
              backgroundColor: '#2d2d2d', 
              borderRadius: 1,
              fontFamily: 'monospace',
              color: '#f0f0f0',
              fontSize: '0.85rem'
            }}>
              cd ats_web/backend<br/>
              python view_database.py
            </Box>
          </Box>
        </Paper>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={onClose}>
          Close
        </Button>
        <Button
          variant="outlined"
          startIcon={<DownloadIcon />}
          onClick={handleExport}
          sx={{
            borderColor: '#633394',
            color: '#633394',
            '&:hover': {
              borderColor: '#3B1C55',
              backgroundColor: 'rgba(99, 51, 148, 0.05)'
            }
          }}
        >
          Export CSV
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default FeedbackDashboard;
