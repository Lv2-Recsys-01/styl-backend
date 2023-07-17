import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/reset.css";
import "antd/dist/reset.css";
import GlobalStyle from "./styles/globalStyle";
import { ThemeProvider } from "styled-components";
import theme from "./styles/theme";
import App from "./pages/App";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
    <>
        <ThemeProvider theme={theme}>
            <GlobalStyle />
            <App />
        </ThemeProvider>
    </>,
);
