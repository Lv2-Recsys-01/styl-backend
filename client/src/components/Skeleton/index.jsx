import React, { useState, useEffect } from "react";
import "./skeleton.css";

function SkeletonCodi() {
    return (
        <div className="skeleton-wrapper">
            <div className="skeleton-rectangle">
                <span className="loading-text">Loading...</span>
            </div>
            <div className="skeleton-rectangle">
                <span className="loading-text">Loading...</span>
            </div>
        </div>
    );
}

export default SkeletonCodi;
