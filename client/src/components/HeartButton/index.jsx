import React, { useState } from "react";
import { HeartOutlined, HeartFilled } from "@ant-design/icons";
import axios from "axios";

function HeartButton(props) {
  const [isLiked, setIsLiked] = useState(props.likeState);

  const handleToggleLike = () => {
    setIsLiked((prevIsLiked) => !prevIsLiked);
    sendLikeRequest(); // 버튼을 누를 때마다 API 호출
  };

  const sendLikeRequest = () => {
    const outfitId = props.outfitId; // outfit_id 값을 가져와야 함

    axios
      .post(`http://localhost:8000/journey/${outfitId}/like`)
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
