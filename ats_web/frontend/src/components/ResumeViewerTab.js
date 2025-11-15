import React, { useState } from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import ResumeViewer from './ResumeViewer';

const ResumeViewerTab = ({ candidate }) => {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <Box sx={{ width: '100%', mt: 3 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Analysis" />
          <Tab label="Interactive Resume" />
        </Tabs>
      </Box>

      {/* Analysis Tab */}
      <Box hidden={activeTab !== 0} sx={{ p: 3 }}>
        {/* Your existing analysis content goes here */}
        <p>Analysis content (keep your existing component here)</p>
      </Box>

      {/* Resume Viewer Tab */}
      <Box hidden={activeTab !== 1} sx={{ p: 3 }}>
        <ResumeViewer 
          candidateId={candidate.candidate_id}
          candidateName={candidate.candidate_name}
        />
      </Box>
    </Box>
  );
};

export default ResumeViewerTab;
