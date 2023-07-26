import React from "react";
import "./MoveToTop.css";

class MoveToTop extends React.Component {
    handleScrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    render() {
        return (
                <div className="top-arrow" onClick={this.handleScrollToTop} >back to top</div>
        );
    }
}

export default MoveToTop;
