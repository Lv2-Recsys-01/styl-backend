import { Layout, Space } from "antd";
import "./index.css";
import { ArrowLeftOutlined, CloseOutlined, ShareAltOutlined } from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import axios from "axios";
import { useEffect, useState } from "react";

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
    const { outfit_id } = useParams();
    const [singleOutfit, setSingleOutfit] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/items/journey/${outfit_id}`);
                const singleOutfitData = response.data.outfit;
                setSingleOutfit(singleOutfitData);
            } catch (error) {
                console.error("Failed to fetch data:", error);
            }
        };
        fetchData();
    }, [outfit_id]);

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
            {singleOutfit && (
                <>
                    <img className="codi" src={singleOutfit.img_url} alt="NoImg" />
                    <p className="options">
                        <a href={singleOutfit.origin_url}>
                            <img className="musinsa" src="https://www.musinsa.com/favicon.ico" alt="NoImg" />
                        </a>
                        <ShareAltOutlined className="share" onClick={handleShareClick} />
                        <HeartButton outfitId={singleOutfit.outfit_id} likeState={singleOutfit.is_liked} />
                    </p>
                </>
            )}
        </div>
    );
}

function SimilarItems() {
    const { outfit_id } = useParams();
    const navigate = useNavigate();
    const [similarOutfitsList, setSimilarOutfitsList] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/items/journey/${outfit_id}`);
                const fetchedSimilarOutfitsList = response.data.similar_outfits_list;
                setSimilarOutfitsList(fetchedSimilarOutfitsList);
            } catch (error) {
                console.error("Failed to fetch data:", error);
            }
        };
        fetchData();
    }, [outfit_id]);

    const goToDetailPage = (similarOutfitId) => {
        navigate(`/detail/${similarOutfitId}`);
    };

    // SimilarItems 컴포넌트가 렌더링될 때 similarOutfitsList가 존재할 경우에만 실행되도록 조건문 추가
    if (similarOutfitsList.length > 0) {
        const sim1 = similarOutfitsList[0].outfit_id;
        const sim1_url = similarOutfitsList[0].img_url;
        const sim2 = similarOutfitsList[1].outfit_id;
        const sim2_url = similarOutfitsList[1].img_url;
        const sim3 = similarOutfitsList[2].outfit_id;
        const sim3_url = similarOutfitsList[2].img_url;
        console.log("sim1", sim1, typeof sim1);
        return (
            <div>
                <p className="description">Similar Style</p>
                <Space direction="horizontal" className="similar">
                    <img
                        src={sim1_url}
                        alt="NoImg"
                        onClick={() => {
                            axios.post(`http://localhost:8000/items/journey/${sim1}/click`);
                            goToDetailPage(sim1);
                        }}
                    />
                    <img
                        src={sim2_url}
                        alt="NoImg"
                        onClick={() => {
                            axios.post(`http://localhost:8000/items/journey/${sim2}/click`);
                            goToDetailPage(sim2);
                        }}
                    />
                    <img
                        src={sim3_url}
                        alt="NoImg"
                        onClick={() => {
                            axios.post(`http://localhost:8000/items/journey/${sim3}/click`);
                            goToDetailPage(sim3);
                        }}
                    />
                </Space>
            </div>
        );
    }

    return null;
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
