import { Layout, Space } from "antd";
import "./index.css";
import { ArrowLeftOutlined, CloseOutlined, ShareAltOutlined } from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import axios from "axios";
import { useEffect } from "react";

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

function DetailCodi(props) {
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
                    message: "URL이 복사되었습니다!",
                    description: "클립보드에 URL이 복사되었어요",
                    duration: 1,
                });
            })
            .catch((error) => {
                console.error("Failed to copy URL to clipboard:", error);
            });
    };
    return (
        <div className="body">
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
    const goToDetailPage = (outfit_id) => {
        navigate(`/detail/${outfit_id}`);
    };
    const outfit_id1 = 1;
    const outfit_id2 = 2;
    const outfit_id3 = 3;
    return (
        <div>
            <p className="description">Similar Style</p>
            <Space direction="horizontal" className="similar">
                {/* TODO: /items/journey/{outfit_id}/click */}
                <img src="sample_codi.png" alt="NoImg" onClick={goToDetailPage(outfit_id1)} />
                <img src="sample_codi.png" alt="NoImg" onClick={goToDetailPage(outfit_id2)} />
                <img src="sample_codi.png" alt="NoImg" onClick={goToDetailPage(outfit_id3)} />
            </Space>
        </div>
    );
}

function DetailPage() {
    //TODO: GET items/journey/{outfit_id}
    //유사 아이템, 메인 아이템 링크 걸기
    const { outfit_id } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/items/journey/${outfit_id}`);
                console.log(response.data); // 요청 결과 출력
            } catch (error) {
                console.error("Failed to fetch data:", error);
            }
        };
        fetchData();
    }, []);

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
                    <DetailCodi detail_outfitId={outfit_id} />
                </Content>
                <Footer className="detail-footer">
                    <SimilarItems />
                </Footer>
            </Layout>
        </Space>
    );
}

export default DetailPage;
