import React from "react";
import "./collectionbutton.css";
import { NavLink} from "react-router-dom";
import { StarFilled } from "@ant-design/icons";

class CollectionButton extends React.Component {

    render() {
        return (
            <div className="collection-button-container" >
                <NavLink to="/collections" className="collection"><StarFilled className= "collection-star"/></NavLink>
            </div>
        );
    }
}

export default CollectionButton;