import React from "react";
import ToggleRouter from "../../components/ToggleRouter";
import ImageGridView from "../../components/ImageGridView";

function Journey() {
    return (
        <div>
            <ToggleRouter />
            <ImageGridView view={'journey'}/>
        </div>
    );
}

export default Journey;
