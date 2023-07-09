const delayPromise = (n, expectedData) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(expectedData);
        }, n * 1000);
    });
};

export { delayPromise };
