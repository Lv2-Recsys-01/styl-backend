import React from "react";
import ToggleRouter from "../../components/ToggleRouter";
import ImageGridView from "../../components/ImageGridView";

function MyPage() {
    return (
        <div>
            <ToggleRouter />
            <ImageGridView view={'collections'}/>
        </div>
    );
}

export default MyPage;
