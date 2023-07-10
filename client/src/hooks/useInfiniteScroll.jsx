import { useState, useEffect } from "react";

const defaultOptions = {
    root: null,
    rootMargin: "1px",
    threshold: "0.1",
};

export default function useInfiniteScroll(fetchCallback, targetElement, options = defaultOptions) {
    const [isFetching, setIsFetching] = useState(false);

    const intersectionCallbackFunc = (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setIsFetching(true);
            }
        });
        setIsFetching(false);
    };

    useEffect(() => {
        let observer;

        if (targetElement) {
            observer = new IntersectionObserver(intersectionCallbackFunc, options);
            observer.observe(targetElement);
        }

        return () => observer?.disconnect(targetElement);
    }, []);

    useEffect(() => {
        if (!isFetching) {
            return;
        }
        fetchCallback();
    }, [isFetching]);

    return [isFetching, setIsFetching];
}
