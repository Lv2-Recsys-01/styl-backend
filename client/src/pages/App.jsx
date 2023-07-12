import React from "react";
import { BrowserRouter, Outlet, Route, Routes, useParams } from "react-router-dom";
import Journey from "./Journey";
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
                    <Route path="/journey" element={<Journey />} />
                    <Route path="/collections" element={<MyPage />} />
                    <Route path="/detail/:outfit_id" element={<DetailPageWrapper />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

function DetailPageWrapper() {
    const { outfit_id } = useParams();

    const isNumeric = /^\d+$/.test(outfit_id);

    if (!isNumeric) {

        return <NotFoundPage />;
    }

    return <DetailPage outfitId={parseInt(outfit_id)} />;
}

export default App;
