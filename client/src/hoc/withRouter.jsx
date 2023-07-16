import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useCookies } from "react-cookie";
import { notification } from "antd";
import { styleAxios } from "../utils";

function withRouter(Component) {
    function ComponentWithRouterProp(props) {
        const [isLoggedIn, setIsLoggedIn] = useState(false);
        const [cookies] = useCookies(["Cookies"]);
        const navigate = useNavigate();

        useEffect(() => {
            if (cookies.user_id !== undefined) {
                setIsLoggedIn(true);
            }
        }, [cookies]);

        let location = useLocation();
        let params = useParams();

        useEffect(() => {
            window.scrollTo({ top: 0, behavior: "instant" });
            const checkAuth = async () => {
                const res = await styleAxios.get("/healthz");
                console.log(res);
            };

            checkAuth();
            // user info should save in context api
        }, [location.pathname]);

        useEffect(() => {
            if (isLoggedIn && location.pathname === "/") {
                navigate("/journey", { replace: true });
                setIsLoggedIn(false);
                notification.warning({
                    message: "로그인되어 있습니다!",
                    description: "로그아웃을 먼저 해주세요.",
                    duration: 3,
                });
            }
        }, [isLoggedIn, location.pathname, navigate]);

        return <Component {...props} location={location} params={params} navigate={navigate} />;
    }

    return ComponentWithRouterProp;
}

export default withRouter;
