import React from "react";
import { CaretUpFilled } from "@ant-design/icons";
import "./MoveToTop.css";

class MoveToTop extends React.Component {
    handleScrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    render() {
        return (
                <CaretUpFilled className="top-arrow" onClick={this.handleScrollToTop} />
        );
    }
}

export default MoveToTop;
