import React from "react";
import "./skeleton.css";

function SkeletonCodi() {
    return (
        <div className="skeleton-wrapper">
            <div className="skeleton-rectangle">
                <span className="loading-text">AI가 당신을 위한 코디를 추천하고 있습니다..</span>
            </div>
            <div className="skeleton-rectangle">
                <span className="loading-text">AI가 당신을 위한 코디를 추천하고 있습니다..</span>
            </div>
        </div>
    );
}

export default SkeletonCodi;
