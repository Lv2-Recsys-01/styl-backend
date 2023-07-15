import React from "react";
import { CaretUpFilled } from "@ant-design/icons";
import "./MoveToTop.css";

class MoveToTop extends React.Component {
    handleScrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    render() {
        return (
            <div className="scroll-to-top-button">
                <CaretUpFilled className="top-arrow" onClick={this.handleScrollToTop} />
            </div>
        );
    }
}

export default MoveToTop;
