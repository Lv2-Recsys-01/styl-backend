import React, { useState } from "react";
import { HeartOutlined, HeartFilled } from "@ant-design/icons";

function HeartButton() {
    const [isLiked, setIsLiked] = useState(false);

    const handleToggleLike = () => {
        setIsLiked((prevIsLiked) => !prevIsLiked);
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
