import React, { useEffect, useState } from "react";
import "./layout.css";
import withRouter from "../../hoc/withRouter";
import { Space } from "antd";
import { NavLink, useNavigate } from "react-router-dom";
import { ArrowDownOutlined } from "@ant-design/icons";
import MoveToTop from "../MoveToTop";
import MoveBottom from "../MoveBottom";

export function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userId, setUserId] = useState("");
    const navigate = useNavigate();

    //로그인 여부를 확인해서 로그인 했으면
    //setIsLoggedIn('true')
    //setUserId('user123')

    const handleLogin = () => {
        // 로그인 버튼 클릭 시 처리할 이벤트
        navigate("/");
        // 추가적인 로직 및 리다이렉션 등을 수행할 수 있습니다.
    };

    const handleLogout = () => {
        // 로그아웃 버튼 클릭 시 처리할 이벤트
        // 추가적인 로직 및 리다이렉션 등을 수행할 수 있습니다.
    };

    const handleLoginLogout = () => {
        if (isLoggedIn) {
            handleLogout();
        } else {
            handleLogin();
        }
    };

    return (
        <div className="header">
            <div className="wrapper">
                <Space direction="horizontal" className="options">
                    <div className="user_id">{userId}</div>
                    <NavLink to="/" className="login" onClick={handleLoginLogout}>
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
