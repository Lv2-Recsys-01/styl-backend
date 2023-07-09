import { useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function withRouter(Component) {
    function ComponentWithRouterProp(props) {
        let location = useLocation();
        let navigate = useNavigate();
        let params = useParams();

        useEffect(() => {
            console.log("changed!");

            const checkAuth = async () => {
                const res = await axios.get("http://localhost:8000/");

                console.log(res);
            };

            checkAuth();
            // user info should save in context api
        }, [location.pathname]);

        return <Component {...props} location={location} params={params} navigate={navigate} />;
    }

    return ComponentWithRouterProp;
}

export default withRouter;
