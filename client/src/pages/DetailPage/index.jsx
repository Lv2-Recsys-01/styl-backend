import { Layout, Space } from "antd";
import "./index.css";
import { ArrowLeftOutlined, CloseOutlined, ShareAltOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";

const { Header, Footer, Content } = Layout;

function DetailHeader() {
    const navigate = useNavigate();

    const goBack = () => {
        navigate(-1);
    };
    const goJourney = () => {
        navigate("/journey");
    };

    return (
        <>
            <ArrowLeftOutlined className="back" onClick={goBack} />
            <CloseOutlined className="close" onClick={goJourney} />
        </>
    );
}

function DetailCodi() {
    const navigate = useNavigate();
    const goMusinsa = () => {
        navigate("/musinsa");
    };
    const handleShareClick = () => {
        const currentURL = window.location.href;
        navigator.clipboard
            .writeText(currentURL)
            .then(() => {
                console.log("URL copied to clipboard");
                notification.success({
                    message: "URL Copied",
                    description: "The URL has been copied to the clipboard.",
                    duration: 1,
                });
            })
            .catch((error) => {
                console.error("Failed to copy URL to clipboard:", error);
            });
    };
    return (
        <div classname="body">
            <img className="codi" src="sample_codi.png" alt="NoImg" />
            <p className="options">
                <img className="musinsa" src="musinsa.png" alt="NoImg" onClick={goMusinsa} />
                <ShareAltOutlined className="share" onClick={handleShareClick} />
                <HeartButton />
            </p>
        </div>
    );
}

function SimilarItems() {
    const navigate = useNavigate();
    const goDetail = () => {
        navigate("/detail1");
    };
    return (
        <div>
            <p className="description">Similar Style</p>
            <Space direction="horizontal" className="similar">
                <img src="sample_codi.png" alt="NoImg" onClick={goDetail} />
                <img src="sample_codi.png" alt="NoImg" onClick={goDetail} />
                <img src="sample_codi.png" alt="NoImg" onClick={goDetail} />
            </Space>
        </div>
    );
}

function DetailPage() {
    return (
        <Space
            direction="vertical"
            style={{
                width: "100%",
            }}
            size={[0, 48]}
        >
            <Layout className="detail">
                <Header className="detail-header">
                    <DetailHeader />
                </Header>
                <Content className="detail-content">
                    <DetailCodi />
                </Content>
                <Footer className="detail-footer">
                    <SimilarItems />
                </Footer>
            </Layout>
        </Space>
    );
}

export default DetailPage;
