import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useCookies } from "react-cookie";
import { notification } from "antd";

function withRouter(Component) {
    function ComponentWithRouterProp(props) {
        const [isLoggedIn, setIsLoggedIn] = useState(false);
        const [cookies] = useCookies(["Cookies"]);
        const navigate = useNavigate();

        useEffect(() => {
            if (cookies.user_id !== undefined) {
                setIsLoggedIn(true);
            }
        }, [cookies.user_id, cookies.user_name]);

        let location = useLocation();
        let params = useParams();

        useEffect(() => {
            if (isLoggedIn && location.pathname === "/") {
                navigate("/journey/men", { replace: true });
                setIsLoggedIn(false);
                notification.warning({
                    message: "로그인되어 있습니다!",
                    description: "로그아웃을 먼저 해주세요.",
                    duration: 3,
                });
            }
        }, [isLoggedIn, location.pathname]);

        return <Component {...props} location={location} params={params} navigate={navigate} />;
    }

    return ComponentWithRouterProp;
}

export default withRouter;
