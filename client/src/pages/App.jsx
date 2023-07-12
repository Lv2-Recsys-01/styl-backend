import React from "react";
import { useNavigate, BrowserRouter, Outlet, Route, Routes, useParams } from "react-router-dom";
import Journey from "./Journey";
import EntryPage from "./EntryPage";
import MyPage from "./MyPage";
import DetailPage from "./DetailPage";
import Layout from "../components/Layout";

function LayoutOutlet() {
    return (
        <Layout>
            <Outlet />
        </Layout>
    );
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LayoutOutlet />}>
                    <Route path="/" element={<EntryPage />} />
                    <Route path="/journey" element={<Journey />} />
                    <Route path="/collections" element={<MyPage />} />
                    <Route path="/detail/:outfit_id" element={<DetailPageWrapper />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
//TODO: detail/ede같이 숫자가 아니거나 범위를 넘어갔을 때 처리
function DetailPageWrapper() {
    const { outfit_id } = useParams();

    return <DetailPage outfitId={outfit_id} />;
}

export default App;
