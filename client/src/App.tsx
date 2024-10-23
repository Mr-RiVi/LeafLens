import { BrowserRouter } from "react-router-dom";
import IndexRoutes from "./routes/IndexRoutesWithAuth";
import { Box, ThemeProvider } from "@mui/material";
import { AppTheme } from "./assets/styles/Themes/CustomAppTheme";

function App() {
  return (
    <ThemeProvider theme={AppTheme}>
      <Box
        className="App"
      >
        <BrowserRouter>
          <IndexRoutes />
        </BrowserRouter>
      </Box>
    </ThemeProvider>
  );
}

export default App;