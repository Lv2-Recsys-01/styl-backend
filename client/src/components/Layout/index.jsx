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

    const [cookieUserId] = useCookies(['user_id']);
    const [cookieUserName] = useCookies(['user_name']);

    useEffect(() => {

        if (cookieUserId.name !=='1') {
            setIsLoggedIn(true);
            SetUserName(cookieUserName.name);
        }
    }, []);

    const handleLogin = () => {
        navigate("/");
    };

    const handleLogout = () => {
        axios.post("http://localhost:8000/logout")
                .then(response => {
                setIsLoggedIn(false);
                navigate(window.location.pathname, { replace: true });
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
    const [isDetailPage, setIsDetailPage] = useState(() => location.pathname === "/detail");
    useEffect(() => {
        setIsDetailPage(location.pathname === "/detail" || location.pathname === "/");
    }, [location]);

    return (
        <div className="global-container">
            {isDetailPage ? (
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
