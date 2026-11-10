import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router";

import { AppRoutes } from "./app/AppRoutes";
import { createStore } from "./app/store";
import { ROOT_ELEMENT_ID } from "./shared/constants/app";

const rootElement = document.getElementById(ROOT_ELEMENT_ID);
if (rootElement === null) {
  throw new Error(`Element #${ROOT_ELEMENT_ID} was not found in index.html`);
}

createRoot(rootElement).render(
  <StrictMode>
    <Provider store={createStore()}>
      <ThemeProvider theme={createTheme()}>
        <CssBaseline />
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </ThemeProvider>
    </Provider>
  </StrictMode>,
);
