import React, { useEffect, useState } from "react";
import "./layout.css";
import withRouter from "../../hoc/withRouter";
import { Space } from "antd";
import { NavLink, useNavigate } from "react-router-dom";
import MoveToTop from "../MoveToTop";
import MoveBottom from "../MoveBottom";
import axios from 'axios';
import { useCookies } from 'react-cookie';


export function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, SetUserName] = useState('guest');
    const navigate = useNavigate();

    const [cookies, setCookie] = useCookies('Cookies');

    useEffect(() => {
        if (cookies.user_id !==undefined) {
            setIsLoggedIn(true);
            SetUserName(cookies.user_name);
        }
    }, []);

    const handleLogin = () => {
        navigate("/");
    };

    const handleLogout = () => {
        axios.post("http://localhost:8000/users/logout")
                .then(response => {
                setIsLoggedIn(false);
                navigate(window.location.href);
                console.log(response.data);
            })
            .catch(error => {
            console.error(error);
            });
    };

    return (
        <div className="header">
            <div className="wrapper">
                <Space direction="horizontal" className="options">
                    <div className="user-name">{userName}</div>
                    <NavLink to="/" className="login" onClick={isLoggedIn ? handleLogout : handleLogin}>
                        {isLoggedIn ? "Logout" : "Login"}
                    </NavLink>
                </Space>
            </div>
        </div>
    );
}    

export function Footer() {
    return <div className={`footer-container`}>footer</div>;
}

function Layout({ children, location }) {
   const [isMainlPage, setIsMainPage] = useState(() => location.pathname === "/journey");
    useEffect(() => {
        setIsMainPage(location.pathname === "/journey" || location.pathname === "/collections");
    }, [location]);

    return (
        <div className="global-container">
            {!isMainlPage ? (
                <div>{children}</div>
            ) : (
                <>
                    <Header />
                    {children}
                    <MoveBottom />
                    <MoveToTop />
                </>
            )}
        </div>
    );
}

export default withRouter(Layout);
