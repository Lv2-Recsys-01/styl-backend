import React from "react";
import JourneyGridView from "../../components/Journey/journey";
import "./journeywomen.css";

function JourneyWomen() {
    return (
        <div className="journey-women-header">
            <JourneyGridView view={"women"} />
        </div>
    );
}

export default JourneyWomen;
