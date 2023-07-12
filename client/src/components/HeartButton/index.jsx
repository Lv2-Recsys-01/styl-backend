import React, { useState } from "react";
import { HeartOutlined, HeartFilled } from "@ant-design/icons";
import axios from "axios";
import styled from "styled-components";

const HeartButtonWrapper = styled.div`
  display: flex;
  justify-content: right;
  margin-right: 10px;
  margin-bottom: 10px;
  font-size: 30px;
  color: var(--vivamagenta);
`;

function HeartButton({ likeState, outfitId }) {
    const [isLiked, setIsLiked] = useState(likeState);

    const handleToggleLike = () => {
        setIsLiked((prevIsLiked) => !prevIsLiked);
        sendLikeRequest(); // 버튼을 누를 때마다 API 호출
    };

    const sendLikeRequest = () => {
        axios
            .post(`http://localhost:8000/items/journey/${outfitId}/like`)
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
