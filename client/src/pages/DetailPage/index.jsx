import { Layout, Space } from "antd";
import "./index.css";
import { ArrowLeftOutlined, CloseOutlined, ShareAltOutlined, BulbFilled} from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import { useEffect, useState } from "react";
import { styleAxios } from "../../utils";
import NotFoundPage from "../NotFoundPage";
import Information from "../../components/information/information";

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

function DetailCodi({ singleOutfit, detailOutfitId, detailLikeState, handleShareClick }) {
    return (
        <div className="body">
            {singleOutfit && (
                <>
                    <img
                        className="codi"
                        src={singleOutfit.img_url}
                        alt="NoImg"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.src =
                                "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                        }}
                    />
                    <div className="options">
                        <a href={singleOutfit.origin_url}>
                            <img
                                className="musinsa"
                                src="https://www.musinsa.com/favicon.ico"
                                alt="NoImg"
                                onClick={() => {
                                    styleAxios.post(`/items/journey/${detailOutfitId}/musinsa-share/musinsa`);
                                }}
                            />
                        </a>
                        <ShareAltOutlined className="share" onClick={handleShareClick} />
                        <HeartButton outfitId={detailOutfitId} likeState={detailLikeState} likeType="detail" />
                    </div>
                </>
            )}
        </div>
    );
}

function SimilarItems({ similarOutfitsList, goToDetailPage }) {
    if (similarOutfitsList.length > 0) {
        const slicedSimilarOutfits = similarOutfitsList.slice(0, 3);
        return (
            <div>
                <p className="description">Similar Style</p>
                <Space direction="horizontal" className="similar">
                    {slicedSimilarOutfits.map((similarOutfit) => (
                        <img
                            key={similarOutfit.outfit_id}
                            src={similarOutfit.img_url}
                            alt="NoImg"
                            onError={(e) => {
                                e.target.onerror = null;
                                e.target.src =
                                    "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
                            }}
                            onClick={() => {
                                styleAxios.post(`/items/journey/${similarOutfit.outfit_id}/click/similar`);
                                goToDetailPage(similarOutfit.outfit_id);
                            }}
                        />
                    ))}
                </Space>
            </div>
        );
    }

    return null;
}

function DetailPage() {
    const { front_outfit_id } = useParams();
    const [singleOutfit, setSingleOutfit] = useState(null);
    const [detailOutfitId, setDetailOutfitId] = useState(front_outfit_id);
    const [detailLikeState, setDetailLikeState] = useState(false);
    const [fetchError, setFetchError] = useState(false);
    const [similarOutfitsList, setSimilarOutfitsList] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await styleAxios.get(`/items/journey/${front_outfit_id}`);
                const responseData = response.data;
                const singleOutfitData = responseData.outfit;
                const fetchedSimilarOutfitsList = responseData.similar_outfits_list;

                setSingleOutfit(singleOutfitData);
                setDetailOutfitId(singleOutfitData.outfit_id);
                setDetailLikeState(singleOutfitData.is_liked);
                setSimilarOutfitsList(fetchedSimilarOutfitsList);
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

    const handleShareClick = () => {
        const currentURL = window.location.href;

        try {
            navigator.clipboard.writeText(""); // clear
            navigator.clipboard.writeText(currentURL).then(() => {
                console.log("URL copied to clipboard");
                notification.success({
                    message: "URL이 복사되었습니다!",
                    description: "클립보드에 URL이 복사되었어요",
                    duration: 1,
                });
            });
            styleAxios.post(`/items/journey/${detailOutfitId}/musinsa-share/share`);
        } catch (error) {
            console.error("Failed to copy URL to clipboard:", error);
        }
    };

    const goToDetailPage = (similarOutfitId) => {
        navigate(`/detail/${similarOutfitId}`);
    };

    if (fetchError) {
        return <NotFoundPage />;
    }

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
                    <DetailCodi
                        singleOutfit={singleOutfit}
                        detailOutfitId={detailOutfitId}
                        detailLikeState={detailLikeState}
                        handleShareClick={handleShareClick}
                    />
                </Content>
                <Footer className="detail-footer">
                    <SimilarItems similarOutfitsList={similarOutfitsList} goToDetailPage={goToDetailPage} />
                </Footer>
                <Information text=     {     <>
                    <BulbFilled className="popnotice"/>유사한 코디를 클릭하면, 자세히 볼 수 있어요<BulbFilled className="popnotice"/>
                 </>}
                 position="special-position"
                />
            </Layout>
        </Space>
    );
}

export default DetailPage;
