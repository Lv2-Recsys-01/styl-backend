import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { styled } from "styled-components";
import Skeleton from "../Skeleton";
import HeartButton from "../../components/HeartButton";
import { notification } from "antd";
import { ShareAltOutlined } from "@ant-design/icons";
import { styleAxios } from "../../utils";
import Information from "../information/information";

const PAGE_SIZE = 30;

const S = {
  GridWrapper: styled.div`
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 10px;
    margin: 10px;
  `,
  GridItem: styled.div`
    position: relative;
    width: 100%;
    padding-top: 162%;
    overflow: hidden;
    border-radius: 12px;
    border: 1px solid var(--subcolor);
    cursor: pointer;
    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 85%;
      object-fit: cover;
      border-bottom: 1px solid var(--subcolor);
    }
  `,
};

const CollectionGridView = () => {
  const gridViewWrapperBottomDomRef = useRef(null);
  const [currentPage, setCurrentPage] = useState(0);
  const totalPage = useRef(100);
  const [outfits, setOutfits] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchStopped, setIsFetchStopped] = useState(false);
  const navigate = useNavigate();
  const clickType = 'collection';

  const loadingText = "Loading...";

  const popuptext = (
    <>
       <p>코디 이미지를 클릭하면 상세페이지를 볼 수 있어요!</p>
    </>
  );

  useEffect(() => {
    totalPage.current = 100;
  }, []);

  useEffect(() => {
    let observer;
    const gridViewWrapperBottomDom = gridViewWrapperBottomDomRef.current;
    if (gridViewWrapperBottomDom) {
      const options = {
        root: null,
        rootMargin: "0px 0px 20px 0px",
        threshold: 0,
      };
      observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (
            entry.isIntersecting &&
            !isLoading &&
            !isFetchStopped &&
            currentPage < totalPage.current
          ) {
            fetchData();
          }
        });
      }, options);
      observer.observe(gridViewWrapperBottomDom);
    }
    return () => {
      observer.disconnect();
    };
  }, [isLoading, isFetchStopped, currentPage]);

  const handleShareClick = async (outfit) => {
    const DetailUrl = 'stylesjourney.com/detail/';
    const newUrl = `${DetailUrl}${outfit}`;
    try {
      await navigator.clipboard.writeText(newUrl);
      notification.success({
        message: "URL이 복사되었습니다!",
        description: "클립보드에 URL이 복사되었어요",
        duration: 1,
      });
      await styleAxios.post(`/items/journey/${outfit}/musinsa-share/share`);
    } catch (error) {
      console.error("Failed to copy URL to clipboard:", error);
    }
  };

  async function fetchData() {
    try {
      setIsLoading(true);
      const viewUrl = "/items/collection";
      const viewParams = new URLSearchParams({
        page_size: PAGE_SIZE.toString(),
        offset: (currentPage * PAGE_SIZE).toString(),
      });
      const response = await styleAxios.get(`${viewUrl}?${viewParams.toString()}`);

      const { outfits_list: outfitsList, is_last: isLast } = response.data;
      const newData = outfitsList
        .filter((single_outfit) =>
          outfits.every((outfit) => outfit.id !== single_outfit.outfit_id)
        )
        .map((single_outfit, i) => ({
          id: currentPage * PAGE_SIZE + i,
          img_url: single_outfit.img_url,
          is_liked: single_outfit.is_liked,
          outfit_id: single_outfit.outfit_id,
        }));


      setOutfits((prevOutfits) => [...prevOutfits, ...newData]);

      setCurrentPage((prevPage) => prevPage + 1);

      if (isLast) {
        setIsFetchStopped(true);
      }
    } catch (error) {
      console.log(error);
      if (error.response?.request?.status === 501) {
        navigate(-1);
        notification.warning({
          message: "JOURNEY 페이지로 이동합니다.",
          description: "먼저, 마음에 드는 코디에 하트를 눌러보세요!",
          duration: 3,
        });
      }
    } finally {
      setIsLoading(false);
    }
  }

  const goToDetailPage = (front_outfit_id) => {
    window.scrollTo({ top: 0, behavior: "instant" });
    navigate(`/detail/${front_outfit_id}`);
  };

  return (
    <div className="custom-wrapper">
      <S.GridWrapper>
        {outfits.map((outfit) => (
          <S.GridItem key={outfit.id}>
            <img
              src={outfit.img_url}
              alt={outfit.id}
              onError={(e) => {
                e.target.onerror = null;
                e.target.src =
                  "https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/subimage/loading.jpg";
              }}
              onClick={() => {
                goToDetailPage(outfit.outfit_id);
                styleAxios
                  .post(`/items/journey/${outfit.outfit_id}/click/${clickType}`)
                  .catch((error) => {
                    console.error(error);
                  });
              }}
            />
            <div
              className="journey-option"
              style={{
                display: "flex",
                justifyContent: "flex-end",
                alignItems: "center",
              }}
            >
              <ShareAltOutlined
                className="journey-share"
                style={{ fontSize: "25px", marginRight: "12px", marginBottom: "10px" }}
                onClick={() => handleShareClick(outfit.outfit_id)}
              />
              <div style={{ display: "flex", alignItems: "center" }}>
                <HeartButton
                  className="heart-button"
                  outfitId={outfit.outfit_id}
                  likeState={outfit.is_liked}
                  likeType="journey"
                />
              </div>
            </div>
          </S.GridItem>
        ))}
      </S.GridWrapper>
      {currentPage > 0 && isLoading && <Skeleton text={loadingText} />}
      <div ref={gridViewWrapperBottomDomRef} />
      <Information text={popuptext} position="collection-position"/>
    </div>
  );
};

export default CollectionGridView;

