import React, { useState } from "react";
import { HeartOutlined, HeartFilled } from "@ant-design/icons";
import axios from "axios";

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
        <div>
            {isLiked ? (
                <HeartFilled className="heart" onClick={handleToggleLike} />
            ) : (
                <HeartOutlined className="heart" onClick={handleToggleLike} />
            )}
        </div>
    );
}

export default HeartButton;
