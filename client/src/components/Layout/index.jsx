import React, { useEffect, useState } from "react";
import "./layout.css";
import withRouter from "../../hoc/withRouter";
import { Space } from "antd";
import { NavLink, useNavigate } from "react-router-dom";
import MoveToTop from "../MoveToTop";
import MoveBottom from "../MoveBottom";
import { useCookies } from "react-cookie";
import { styleAxios } from "../../utils";
import ToggleRouter from "../../components/ToggleRouter";
import MyComponent from "../../components/information/information";

export function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, SetUserName] = useState("guest");
    const navigate = useNavigate();

    const [cookies, _] = useCookies("Cookies");

    useEffect(() => {
        if (cookies.user_id !== undefined) {
            setIsLoggedIn(true);
            SetUserName(cookies.user_name);
        }
    }, [isLoggedIn, cookies]);

    const handleLogin = () => {
        setIsLoggedIn(false);
        navigate("/");
    };

    const handleLogout = () => {
        styleAxios
            .post("/users/logout")
            .then((response) => {
                setIsLoggedIn(false);
                navigate("/");
                console.log(response.data);
            })
            .catch((error) => {
                console.error(error);
            });
    };

    return (
        <div className="header">
            <div className="wrapper">
                <Space direction="horizontal" className="options">
                    <div className="user-name">"Hello, {userName}"</div>
                    <NavLink to="/" className="login" onClick={isLoggedIn ? handleLogout : handleLogin}>
                        {isLoggedIn ? "Logout" : "Login"}
                    </NavLink>
                </Space>
                <ToggleRouter />
            </div>
        </div>
    );
}

export function Footer() {
    return <div className={`footer-container`}>footer</div>;
}

function Layout({ children, location }) {
    const [isMainlPage, setIsMainPage] = useState(
        () => location.pathname === "/journey" || location.pathname === "/collections",
    );

    useEffect(() => {
        setIsMainPage(location.pathname === "/journey" || location.pathname === "/collections");
    }, [location.pathname]);

    return (
        <div className="global-container">
            <>
                {isMainlPage && <Header />}
                {children}
                {isMainlPage && (
                    <>
                        <MoveBottom />
                        <MoveToTop />
                        <MyComponent/>
                    </>
                )}
            </>
        </div>
    );
}

export default withRouter(Layout);
