import React, { useState } from 'react';
import {CssBaseline, ThemeProvider, createTheme} from '@mui/material';
import ResponsiveAppBar from './AppBar';
import StudentForm from './StudentForm';
import AppTheme from './shared-theme/AppTheme';
import ResultGrid from './resultGrid';
const App = () => {
  // Manage theme state
  const [darkMode, setDarkMode] = useState(true);

  // Create theme based on current mode
  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  // Toggle theme function
  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    // <ThemeProvider theme={theme}>
    <AppTheme>
      <CssBaseline />
      <ResponsiveAppBar/>
      {/* <StudentForm/> */}
      {/* <ResultGrid/> */}
    </AppTheme>
    // </ThemeProvider>
  );
};

export default App;
