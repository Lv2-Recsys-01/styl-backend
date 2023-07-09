import React from "react";
import { ArrowDownOutlined } from "@ant-design/icons";
import "./MoveBottom.css";

class MoveBottom extends React.Component {
    render() {
        return (
            <div className="scroll-to-bottom-button">
                <ArrowDownOutlined className="bottom-arrow" />
            </div>
        );
    }
}

export default MoveBottom;
