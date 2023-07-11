import React from "react";
import ReactDOM from "react-dom/client";
import App from "./pages/App";
import "./styles/reset.css";
import "antd/dist/reset.css";
import GlobalStyle from "./styles/globalStyle";
import { ThemeProvider } from "styled-components";
import theme from "./styles/theme";
import axios from "axios";

const root = ReactDOM.createRoot(document.getElementById("root"));

axios.defaults.withCredentials = true;

root.render(
    <>
        <ThemeProvider theme={theme}>
            <GlobalStyle />
            <App />
        </ThemeProvider>
    </>,
);
