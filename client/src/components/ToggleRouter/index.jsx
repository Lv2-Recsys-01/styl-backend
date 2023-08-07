import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./togglerouter.css";

function ToggleRouter() {
  const navigate = useNavigate();
  const location = useLocation();

  const onRouteBtnClick = (route) => {
    navigate(`/${route}`);
  };

  const isActiveRoute = (route) => {
    return (
      location.pathname.toLowerCase() === `/${route.toLowerCase()}` ||
      (location.pathname === "/" && route === "journey/men")
    );
  };

  return (
    <div className="toggle_wrapper">
      <button
        className={`route-btn route-btn-men ${isActiveRoute("journey/men") ? "active" : ""}`}
        onClick={() => onRouteBtnClick("journey/men")}
      >
        MEN
      </button>
      <button
        className={`route-btn route-btn-women ${isActiveRoute("journey/women") ? "active" : ""}`}
        onClick={() => onRouteBtnClick("journey/women")}
      >
        WOMEN
      </button>
    </div>
  );
}

export default ToggleRouter;
