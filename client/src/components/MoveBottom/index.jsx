import React from "react";
import { SyncOutlined } from "@ant-design/icons";
import "./MoveBottom.css";

class MoveBottom extends React.Component {
    handleScrollToBottom = () => {
        document.documentElement.scrollTo({ top: document.documentElement.scrollHeight -10, behavior: "smooth" });
    };

    render() {
        return (
                <SyncOutlined spin className="bottom-arrow" onClick={this.handleScrollToBottom} />
        );
    }
}

export default MoveBottom;