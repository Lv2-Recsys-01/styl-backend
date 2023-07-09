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
                        src="https://image.msscdn.net/mfile_s01/_street_images/21754/list.street_list_56399249891e5.jpg.250?20200818233041"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://image.msscdn.net/mfile_s01/_street_images/62145/list.street_list_5efaaa72a09ed.jpg.250?20200819103705"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://image.msscdn.net/mfile_s01/_street_images/53328/list.street_list_5d196dd580985.jpg.250?20200819075906"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://image.msscdn.net/mfile_s01/_street_images/53082/list.street_list_5d105346caee9.jpg.250?20200819075435"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://image.msscdn.net/mfile_s01/_street_images/45508/list.street_list_5b48490710aaa.jpg.250?20200819054633"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://image.msscdn.net/mfile_s01/_street_images/80432/list.street_list_624baf2c355f6.jpg.250?20220406173002"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="up"
                        src="https://image.msscdn.net/mfile_s01/_street_images/72539/list.street_list_60e2962eefcb1.jpg.250?20210721141020"
                        alt="NoImg"
                    />
                </Col>
                <Col span={12}>
                    <img
                        className="down"
                        src="https://image.msscdn.net/mfile_s01/_street_images/54972/list.street_list_5d7750d45ebc5.jpg.250?20200819082909"
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
