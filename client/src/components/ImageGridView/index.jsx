import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { styled } from "styled-components";
import Skeleton from "../Skeleton";
import HeartButton from "../../components/HeartButton";
import "./imagegridview.css";

const PAGE_SIZE = 10;

const S = {
    GridWrapper: styled.div`
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 10px;
        margin: 10px;
    `,
    GridItem: styled.div`
        position: relative;
        width: 100%;
        padding-top: 162%; /* 황금비 1.618의 근사값. 가로 대비 세로의 높이 */
        overflow: hidden;
        border-radius: 12px;
        border: 2px solid var(--vivamagenta);

        img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 85%;
            object-fit: cover;
            border-bottom: 2px dashed var(--vivamagenta);
        }
    `,
};

function getRandomNumber() {
    const min = Math.ceil(300 / 100); // 3
    const max = Math.floor(600 / 100); // 6
    const randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
    return randomNumber * 100;
}

const GridItem = ({ children, index }) => {
    return <S.GridItem key={index}>{children}</S.GridItem>;
};

function ImageGridView() {
    const gridViewWrapperBottomDomRef = useRef(null);
    const currentPage = useRef(0);
    const totalPage = useRef(100);
    const [outfits, setOutfits] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useLayoutEffect(() => {
        totalPage.current = 100;
    });

    useEffect(() => {
        let observer;
        const gridViewWrapperBottomDom = gridViewWrapperBottomDomRef.current;

        if (gridViewWrapperBottomDom) {
            const options = {
                root: null,
                rootMargin: "0px 0px 20px 0px",
                threshold: 0,
            };
            observer = new IntersectionObserver((entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting && !isLoading && currentPage.current < totalPage.current) {
                        console.log("should fetch data");
                        setIsLoading(true);

                        // Simulating data fetching time
                        const startFetchTime = Date.now();

                        // Simulating data fetching
                        //TODO: backendapi get images
                        fetchData().then(() => {
                            const endFetchTime = Date.now();
                            const elapsedFetchTime = endFetchTime - startFetchTime;
                            const fetchTime = Math.max(0, 1000 - elapsedFetchTime); // Minimum fetchTime of 1 second
                            setTimeout(() => {
                                const newData = [...outfits];
                                for (let i = 0; i < PAGE_SIZE; i++) {
                                    const randomNumWidth = getRandomNumber();
                                    const randomNumHeight = getRandomNumber();
                                    newData.push(
                                        <GridItem key={currentPage.current * PAGE_SIZE + i}>
                                            {/* <img
                                                src={`https://placehold.co/${randomNumWidth}x${randomNumHeight}`}
                                                alt={currentPage.current * PAGE_SIZE + i}
                                            /> */}
                                            <img src="sample_codi.png" alt={currentPage.current * PAGE_SIZE + i} />
                                            <HeartButton classname="heart-button" />
                                        </GridItem>,
                                    );
                                }
                                setOutfits(newData);
                                currentPage.current += 1;
                                setIsLoading(false);
                            }, fetchTime);
                        });
                    }
                });
            }, options);

            observer.observe(gridViewWrapperBottomDom);
        }

        return () => {
            observer.disconnect();
        };
    }, [isLoading, outfits]);

    // Simulating data fetching
    function fetchData() {
        return new Promise((resolve) => {
            // Simulating server response time
            const responseTime = Math.random() * 1000 + 1000; // Random time between 0.5 and 2.5 seconds

            setTimeout(() => {
                resolve(responseTime);
            }, responseTime);
        });
    }

    return (
        <div className="custom-wrapper">
            <S.GridWrapper>{outfits}</S.GridWrapper>
            {currentPage.current > 0 && isLoading && <Skeleton />}
            <div ref={gridViewWrapperBottomDomRef} />
        </div>
    );
}

export default ImageGridView;
