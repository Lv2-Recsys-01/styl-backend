import React from "react";
import CollectionGridView from "../../components/Collection/collection";
import "./mypage.css"
import { Layout } from "antd";
import { HomeOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const { Header } = Layout;

function DetailHeader() {
    const navigate = useNavigate();

    const goHome = () => {
        navigate(-1);
    };

    return (
        <>
            <div className= "collection-title"> My Collections</div>
            <HomeOutlined className="home" onClick={goHome} />
        </>
    );
}

function MyPage() {
    return (
        <div className="mypage-wrapper">
            <Header className="mypage">
                {DetailHeader()}
            </Header>
            <div className="collection-header">
                <CollectionGridView/>
            </div>
        </div>
    );
}

export default MyPage;
