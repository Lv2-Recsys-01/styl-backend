import React from "react";
import JourneyGridView from "../../components/Journey/journey";
import "./journeymen.css";

function JourneyMen() {
    return (
        <div className="journey-men-header">
            <JourneyGridView view={"men"} />
        </div>
    );
}

export default JourneyMen;
