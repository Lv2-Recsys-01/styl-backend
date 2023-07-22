import React, { useEffect } from "react";
import "./skeleton.css";

function SkeletonCodi() {
  useEffect(() => {
    document.documentElement.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: "smooth",
    });
  }, []);

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
