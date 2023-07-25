import React, { useEffect } from "react";
import "./skeleton.css";

function SkeletonCodi(props) {
  useEffect(() => {
    document.documentElement.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: "smooth",
    });
  }, []);

  return (
    <div className="skeleton-wrapper">
      <div className="skeleton-rectangle">
        <span className="loading-text">{props.text}</span>
      </div>
      <div className="skeleton-rectangle">
        <span className="loading-text">{props.text}</span>
      </div>
    </div>
  );
}

export default SkeletonCodi;
