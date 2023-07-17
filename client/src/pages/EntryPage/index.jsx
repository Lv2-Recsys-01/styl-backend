import React from "react";
import Login from "../../components/Login/login";
import "./index.css";
import { Row, Col } from "antd";

function EntryBackground() {
    return (
        <div className="entry-background">
            <Row gutter={[16, 16]}>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2023female/91725.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2022male/85039.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2022male/82356.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2023female/92055.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2023female/92003.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2022male/85259.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2023female/92002.jpg"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/2022male/84832.jpg"
                        alt="NoImg"
                    />
                </Col>
            </Row>
            <Row gutter={[16, 16]}>
                <Col span={12} />
                <Col span={12} />
            </Row>
        </div>
    );
}

function EntryPage() {
    return (
        <div>
            <EntryBackground />
            <Login />
        </div>
    );
}

export default EntryPage;
