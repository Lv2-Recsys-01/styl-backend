import React, { useState, useEffect } from "react";
import { HeartOutlined, HeartFilled } from "@ant-design/icons";
import styled from "styled-components";
import { styleAxios } from "../../utils";

const HeartButtonWrapper = styled.div`
    display: flex;
    justify-content: right;
    margin-right: 10px;
    margin-bottom: 10px;
    font-size: 30px;
    color: var(--vivamagenta);
`;

function HeartButton({ likeState, outfitId, likeType }) {
    const [isLiked, setIsLiked] = useState(likeState);

    useEffect(() => {
        setIsLiked(likeState);
    }, [outfitId, likeState]);

    const handleToggleLike = () => {
        setIsLiked((prevIsLiked) => !prevIsLiked);
        sendLikeRequest();
    };

    const sendLikeRequest = () => {
        styleAxios
            .post(`/items/journey/${outfitId}/like/${likeType}`)
            .then((response) => {
                console.log(response.data); // API 응답 데이터 처리
            })
            .catch((error) => {
                console.error(error); // 오류 처리
            });
    };

    return (
        <HeartButtonWrapper>
            {isLiked ? (
                <HeartFilled className="heart" onClick={handleToggleLike} />
            ) : (
                <HeartOutlined className="heart" onClick={handleToggleLike} />
            )}
        </HeartButtonWrapper>
    );
}

export default HeartButton;
