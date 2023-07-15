import React from "react";
import { CaretDownFilled } from "@ant-design/icons";
import "./MoveBottom.css";

class MoveBottom extends React.Component {
    handleScrollToBottom = () => {
        document.documentElement.scrollTo({ top: document.documentElement.scrollHeight -10, behavior: "smooth" });
    };
    
    render() {
        return (
            <div className="scroll-to-bottom-button">
                <CaretDownFilled className="bottom-arrow" onClick={this.handleScrollToBottom}/>
            </div>
        );
    }
}

export default MoveBottom;