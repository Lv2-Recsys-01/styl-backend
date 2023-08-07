import React from "react";
import { BrowserRouter, Outlet, Route, Routes, useParams } from "react-router-dom";
import JourneyMen from "./JourneyMen";
import JourneyWomen from "./JourneyWomen";
import EntryPage from "./EntryPage";
import MyPage from "./MyPage";
import DetailPage from "./DetailPage";
import Layout from "../components/Layout";
import NotFoundPage from "./NotFoundPage";

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
                    <Route path="/journey/men" element={<JourneyMen />} />
                    <Route path="/journey/women" element={<JourneyWomen />} />
                    <Route path="/collections" element={<MyPage />} />
                    <Route path="/detail/:front_outfit_id" element={<DetailPageWrapper />} />
                    {/* <Route path="*" element={<NotFoundPage />} /> */}
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

function DetailPageWrapper() {
    const { front_outfit_id } = useParams();

    const isNumeric = /^\d+$/.test(front_outfit_id);

    if (!isNumeric) {
        return <NotFoundPage />;
    }

    return <DetailPage outfitId={parseInt(front_outfit_id)} />;
}

export default App;
