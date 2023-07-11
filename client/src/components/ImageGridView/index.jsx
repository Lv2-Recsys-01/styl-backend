import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { styled } from "styled-components";
import Skeleton from "../Skeleton";
import HeartButton from "../../components/HeartButton";
import "./imagegridview.css";
import axios from "axios";

const PAGE_SIZE = 10;
const DELAY =1000;

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
    padding-top: 162%; /* 황금비 1.618의 근사값. 가로 대비 세로의 높이 */
    overflow: hidden;
    border-radius: 12px;
    border: 2px solid var(--vivamagenta);

    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 85%;
      object-fit: cover;
      border-bottom: 2px dashed var(--vivamagenta);
    }
  `,
};

const GridItem = ({ children, index }) => {
  return <S.GridItem key={index}>{children}</S.GridItem>;
};

function ImageGridView(props) {
  const gridViewWrapperBottomDomRef = useRef(null);
  const currentPage = useRef(0);
  const totalPage = useRef(100);
  const [outfits, setOutfits] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useLayoutEffect(() => {
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
          if (entry.isIntersecting && !isLoading && currentPage.current < totalPage.current) {
            console.log("should fetch data");
            fetchDataWithDelay(DELAY);
          }
        });
      }, options);

      observer.observe(gridViewWrapperBottomDom);
    }

    return () => {
      observer.disconnect();
    };
  }, [isLoading]);

  async function fetchDataWithDelay(delay) {
    setIsLoading(true);
    const startFetchTime = Date.now();
    const remainingDelay = Math.max(delay, 0);
    await new Promise((resolve) => setTimeout(resolve, remainingDelay));
  
    const fetchDataPromise = fetchData();
    await fetchDataPromise;
  
    setIsLoading(false);
  }  
  

  async function fetchData() {
    try {
      const viewUrl = props.view === "journey" ? "http://localhost:8000/journey" : "http://localhost:8000/collection";
      const viewParams = new URLSearchParams({
        pagesize: PAGE_SIZE.toString(),
        offset: currentPage.current.toString(),
      });

      const response = await axios.get(`${viewUrl}?${viewParams.toString()}`);
      const data = response.data;
      console.log(data);

      const newOutfits = response.data;

      const newData = [...outfits];
      for (let i = 0; i < PAGE_SIZE; i++) {
        newData.push(
          <GridItem key={currentPage.current * PAGE_SIZE + i}>
            <img src="sample_codi.png" alt={currentPage.current * PAGE_SIZE + i} />
            <HeartButton classname="heart-button" />
          </GridItem>
        );
      }

      setOutfits(newData);
      currentPage.current += 1;
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="custom-wrapper">
      <S.GridWrapper>{outfits}</S.GridWrapper>
      {currentPage.current > 0 && isLoading && <Skeleton />}
      <div ref={gridViewWrapperBottomDomRef} />
    </div>
  );
}

export default ImageGridView;