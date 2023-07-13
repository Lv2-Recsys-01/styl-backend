import axios from "axios";

const delayPromise = (n, expectedData) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(expectedData);
        }, n * 1000);
    });
};

const styleAxios = axios.create({
    baseURL: process.env.REACT_ENV === "production" ? "http://localhost:8000" : "http:http://43.202.97.64:8000",
    timeout: 2500,
    withCredentials: true,
});

export { delayPromise, styleAxios };
