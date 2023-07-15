import React from "react";
import { CaretDownFilled } from "@ant-design/icons";
import "./MoveBottom.css";

class MoveBottom extends React.Component {
    handleScrollToBottom = () => {
        document.documentElement.scrollTo({ top: document.documentElement.scrollHeight -10, behavior: "smooth" });
    };
    
    render() {
        return (
                <CaretDownFilled className="bottom-arrow" onClick={this.handleScrollToBottom}/>
        );
    }
}

export default MoveBottom;