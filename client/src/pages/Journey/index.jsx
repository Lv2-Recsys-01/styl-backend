import React from "react";
import ImageGridView from "../../components/ImageGridView";
import "./journey.css"

function Journey() {
    return (
        <div className="journey-header">
            <ImageGridView view={'journey'}/>
        </div>
    );
}

export default Journey;
