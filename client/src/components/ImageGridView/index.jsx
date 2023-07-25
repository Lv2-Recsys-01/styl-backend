import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { styled } from "styled-components";
import Skeleton from "../Skeleton";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import { ShareAltOutlined } from "@ant-design/icons";
import { styleAxios } from "../../utils";
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
        border: 1px solid var(--subcolor);
        cursor: pointer;
        img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 85%;
            object-fit: cover;
            border-bottom: 1px solid var(--subcolor);
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
    const [isFetchStopped, setIsFetchStopped] = useState(false);
    const navigate = useNavigate(); // useNavigate 훅 사용
    const loadingText = props.view === "journey" ? "AI가 당신을 위한 코디를 추천하고 있습니다.." : "Loading...";
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
                    if (
                        entry.isIntersecting &&
                        !isLoading &&
                        !isFetchStopped &&
                        currentPage.current < totalPage.current
                    ) {
                        fetchData();
                    }
                });
            }, options);
            observer.observe(gridViewWrapperBottomDom);
        }
        return () => {
            observer.disconnect();
        };
    }, [isLoading]);

    const handleShareClick = (outfit) => {
        const DetailUrl = 'stylesjourney.com/detail/';
        const newUrl = `${DetailUrl}${outfit}`;
        try {
            navigator.clipboard.writeText("");
            navigator.clipboard.writeText(newUrl).then(() => {
                console.log("URL copied to clipboard");
                notification.success({
                    message: "URL이 복사되었습니다!",
                    description: "클립보드에 URL이 복사되었어요",
                    duration: 1,
                });
            });
            styleAxios.post(`/items/journey/${outfit}/musinsa-share/share`);
        } catch (error) {
            console.error("Failed to copy URL to clipboard:", error);
        }
    };
    
    async function fetchData() {
        try {
            setIsLoading(true); 
            await new Promise((resolve) => setTimeout(resolve, 1000));
            const viewUrl = props.view === "journey" ? "/items/journey" : "/items/collection";
            const clickType = props.view === "journey" ? "journey" : "collection";
            const viewParams = new URLSearchParams({
                page_size: PAGE_SIZE.toString(),
                offset: (currentPage.current * PAGE_SIZE).toString(),
            });
            const response = await styleAxios.get(`${viewUrl}?${viewParams.toString()}`);

            const { outfits_list: outfitsList, is_last: isLast } = response.data;

            const newData = [...outfits];
            for (let i = 0; i < outfitsList.length; i++) {
                const single_outfit = outfitsList[i];
                newData.push(
                    <GridItem key={currentPage.current * PAGE_SIZE + i}>
                        <img
                            src={single_outfit.img_url}
                            alt={currentPage.current * PAGE_SIZE + i}
                            onError={(e) => {
                                e.target.onerror = null;
                                e.target.src =
                                    "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                            }}
                            onClick={() => {
                                goToDetailPage(single_outfit.outfit_id);
                                styleAxios.post(`/items/journey/${single_outfit.outfit_id}/click/${clickType}`).catch((error) => {
                                    console.error(error);
                                });
                            }}
                        />
                        <div 
                            className="journey-option"
                            style={{
                                display: "flex",
                                justifyContent: "flex-end", // Right-align the children
                                alignItems: "center", // Center the content vertically
                            }}
                            >
                            <ShareAltOutlined
                                className="journey-share"
                                style={{ fontSize: "25px", marginRight: "12px", marginBottom:"10px" }}
                                onClick={() => handleShareClick(single_outfit.outfit_id)}
                            />
                            <div style={{ display: "flex", alignItems: "center" }}>
                                <HeartButton
                                className="heart-button"
                                outfitId={single_outfit.outfit_id}
                                likeState={single_outfit.is_liked}
                                likeType="journey"
                                />
                            </div>

                        </div>

                    </GridItem>,
                );
            }
            setOutfits(newData);
            currentPage.current += 1;

            if (isLast) {
                setIsFetchStopped(true);
                return;
            }
        } catch (error) {
            console.log(error);
            if (error.response.request.status === 501) {
                navigate("/journey");
                notification.warning({
                    message: "JOURNEY 페이지로 이동합니다.",
                    description: "먼저, 마음에 드는 코디에 하트를 눌러보세요!",
                    duration: 3,
                });
            }
        } finally{
            setIsLoading(false);
        }
    }
    const goToDetailPage = (front_outfit_id) => {
        window.scrollTo({ top: 0, behavior: "instant" });
        navigate(`/detail/${front_outfit_id}`);
    };
    return (
        <div className="custom-wrapper">
            <S.GridWrapper>{outfits}</S.GridWrapper>
            {currentPage.current > 0 && isLoading && <Skeleton text = {loadingText} />}
            <div ref={gridViewWrapperBottomDomRef} />
        </div>
    );
}
export default ImageGridView;
