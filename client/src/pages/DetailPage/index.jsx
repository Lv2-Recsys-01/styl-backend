import { Layout, Space } from "antd";
import "./index.css";
import { ArrowLeftOutlined, CloseOutlined, ShareAltOutlined } from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import { useEffect, useState } from "react";
import { styleAxios } from "../../utils";
import NotFoundPage from "../NotFoundPage";

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
    const { front_outfit_id } = useParams();
    const [singleOutfit, setSingleOutfit] = useState(null);
    const [detailOutfitId, setDetailOutfitId] = useState(front_outfit_id);
    const [detailLikeState, setDetailLikeState] = useState(false);
    const [fetchError, setFetchError] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await styleAxios.get(`/items/journey/${front_outfit_id}`);
                const singleOutfitData = response.data.outfit;
                setSingleOutfit(singleOutfitData);
                setDetailOutfitId(singleOutfitData.outfit_id);
                setDetailLikeState(singleOutfitData.is_liked);
            } catch (error) {
                console.error("Failed to fetch data:", error);
                setFetchError(true);
                notification.error({
                message: "존재하지 않는 코디입니다.",
                description: "뒤로 돌아가 주세요!",
                duration: 2,
        });
      }
    };
    fetchData();
  }, [front_outfit_id]);

  if (fetchError) {
    return <NotFoundPage />;
  }

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
                    <img className="codi" src={singleOutfit.img_url} 
                    alt="NoImg"
                    onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                      }} 
                    />
                    <div className="options">
                        <a href={singleOutfit.origin_url}>
                            <img className="musinsa" src="https://www.musinsa.com/favicon.ico" alt="NoImg"/>
                        </a>
                        <ShareAltOutlined className="share" onClick={handleShareClick} />
                        <HeartButton outfitId={detailOutfitId} likeState={detailLikeState} />
                    </div>
                </>
            )}
        </div>
    );
}

function SimilarItems() {
    const { front_outfit_id } = useParams();
    const navigate = useNavigate();
    const [similarOutfitsList, setSimilarOutfitsList] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await styleAxios.get(`/items/journey/${front_outfit_id}`);
                const fetchedSimilarOutfitsList = response.data.similar_outfits_list;
                setSimilarOutfitsList(fetchedSimilarOutfitsList);
            } catch (error) {

                console.error("Failed to fetch data:", error);
            }
        };
        fetchData();
    }, [front_outfit_id]);

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
        return (
            <div>
                <p className="description">Similar Style</p>
                <Space direction="horizontal" className="similar">
                    <img
                        src={sim1_url}
                        alt="NoImg"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                          }}
                        onClick={() => {
                            styleAxios.post(`/items/journey/${sim1}/click`);
                            goToDetailPage(sim1);
                        }}
                    />
                    <img
                        src={sim2_url}
                        alt="NoImg"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                          }}
                        onClick={() => {
                            styleAxios.post(`/items/journey/${sim2}/click`);
                            goToDetailPage(sim2);
                        }}
                    />
                    <img
                        src={sim3_url}
                        alt="NoImg"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                          }}
                        onClick={() => {
                            styleAxios.post(`/items/journey/${sim3}/click`);
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
