import React from "react";
import { ArrowDownOutlined} from "@ant-design/icons";
import "./MoveBottom.css";

class MoveBottom extends React.Component {
    handleScrollToBottom = () => {
        document.documentElement.scrollTo({ top: document.documentElement.scrollHeight -10, behavior: "smooth" });
    };

    render() {
        return (
            <div className="bottom-arrow-container">
                <span className="bottom-arrow-text">나만의 스타일 찾기</span>
                <ArrowDownOutlined className="bottom-arrow" onClick={this.handleScrollToBottom}/>
            </div>
        );
    }
}

export default MoveBottom;