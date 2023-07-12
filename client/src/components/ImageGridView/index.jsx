import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { styled } from "styled-components";
import Skeleton from "../Skeleton";
import HeartButton from "../../components/HeartButton";
import "./imagegridview.css";
import axios from "axios";
import { notification } from "antd";
const PAGE_SIZE = 10;
const DELAY = 1000;
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
        border: 3px double var(--graylilac);
        img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 85%;
            object-fit: cover;
            border-bottom: 2px dashed var(--graylilac);
        }
    `,
};
const GridItem = ({ children, index }) => {
    return <S.GridItem key={index}>{children}</S.GridItem>;
};
function ImageGridView(props) {
    const gridViewWrapperBottomDomRef = useRef(null);
    const currentPage = useRef(0);
    const totalPage = useRef(100);
    const [outfits, setOutfits] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate(); // useNavigate 훅 사용
    useLayoutEffect(() => {
        totalPage.current = 100;
    }, []);
    useEffect(() => {
        let observer;
        const gridViewWrapperBottomDom = gridViewWrapperBottomDomRef.current;
        if (gridViewWrapperBottomDom) {
            const options = {
                root: null,
                rootMargin: "0px 0px 20px 0px",
                threshold: 0,
            };
            observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting && !isLoading && currentPage.current < totalPage.current) {
                        console.log("should fetch data");
                        fetchDataWithDelay(DELAY);
                    }
                });
            }, options);
            observer.observe(gridViewWrapperBottomDom);
        }
        return () => {
            observer.disconnect();
        };
    }, [isLoading, fetchDataWithDelay]);
    async function fetchDataWithDelay(delay) {
        setIsLoading(true);
        const remainingDelay = Math.max(delay, 0);
        await new Promise((resolve) => setTimeout(resolve, remainingDelay));
        await fetchData();
        setIsLoading(false);
    }
    async function fetchData() {
        try {
            const viewUrl =
                props.view === "journey"
                    ? "http://localhost:8000/items/journey"
                    : "http://localhost:8000/items/collection";
            const viewParams = new URLSearchParams({
                page_size: PAGE_SIZE.toString(),
                offset: (currentPage.current * PAGE_SIZE).toString(),
            });
            const response = await axios.get(`${viewUrl}?${viewParams.toString()}`);
            //TODO: collection/response api에서
            //outfits_list를 통해 아래 데이터 처리,
            // is_last를 통해 fetch끝 지점 나타내기
            const { outfits_list: outfitsList, page_size, offset, is_last: isLast } = response.data;
            console.log(outfitsList, isLast);

            // 응답 데이터 처리
            const outfit_id = 1;
            const newData = [...outfits];
            for (let i = 0; i < outfitsList.length; i++) {
                const single_outfit = outfitsList[i];
                newData.push(
                    <GridItem key={currentPage.current * PAGE_SIZE + i}>
                        {/* TODO: POST /items/journey/{outfit_id}/click
            이미지 클릭시,  */}
                        <img
                            src={single_outfit.image_url}
                            alt={currentPage.current * PAGE_SIZE + i}
                            onClick={() => goToDetailPage(outfit_id)}
                        />
                        {/* TODO: outfit_id, 좋아요 상태 전달 */}
                        <HeartButton
                            className="heart-button"
                            outfitId={single_outfit.outfit_id}
                            likeState={single_outfit.is_liked}
                        />
                    </GridItem>,
                );
            }
            setOutfits(newData);
            currentPage.current += 1;
        } catch (error) {
            if (error.response.status === 501) {
                navigate("/journey");
                notification.warning({
                    message: "JOURNEY 페이지로 이동합니다.",
                    description: "마음에 드는 코디에 하트를 눌러보세요!",
                    duration: 3,
                });
            }
        } finally {
            setIsLoading(false);
        }
    }
    const goToDetailPage = (outfit_id) => {
        navigate(`/detail/${outfit_id}`);
    };
    return (
        <div className="custom-wrapper">
            <S.GridWrapper>{outfits}</S.GridWrapper>
            {currentPage.current > 0 && isLoading && <Skeleton />}
            <div ref={gridViewWrapperBottomDomRef} />
        </div>
    );
}
export default ImageGridView;
