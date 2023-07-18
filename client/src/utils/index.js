import axios from "axios";

const delayPromise = (n, expectedData) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(expectedData);
        }, n * 1000);
    });
};

const styleAxios = axios.create({
    baseURL: process.env.REACT_APP_ENV === "production" ? "https://localhost/api:8000" : "http://localhost:8000",
    timeout: 2500,
    withCredentials: true,
});

export { delayPromise, styleAxios };
