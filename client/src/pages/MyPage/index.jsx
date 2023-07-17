import React from "react";
import ImageGridView from "../../components/ImageGridView";
import "./mypage.css"

function MyPage() {
    return (
        <div className="collection-header">
            <ImageGridView view={'collections'}/>
        </div>
    );
}

export default MyPage;
