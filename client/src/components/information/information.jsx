import React, { useState } from 'react';
import { CloseCircleFilled } from '@ant-design/icons';
import './information.css';
// import { useCookies } from "react-cookie";

const Information = (props) => {
  const { text, position } = props;
  const [visible, setVisible] = useState(true);
  // const [cookies, _] = useCookies("Cookies");

  const handleToggle = () => {
    setVisible(!visible);
  };
  // const handleFormClick = () => {
  //   // Redirect to the Google Form URL using window.location.href
  //   window.location.href = `https://docs.google.com/forms/d/e/1FAIpQLSewgDy9AE8O8mZwJ-efjVc5boidEKW3G1WY0OeP72bj4O3FXg/viewform?entry.850289922=${cookies.session_id}`;
  // };

  return (
    <div>
      {visible && (
        <div className={`popup-container ${position}`}>
          <CloseCircleFilled className='popup-close' onClick={handleToggle} />
          <h2 className='popup-text'>{text}</h2>
          {/* <div className="google-form" onClick={handleFormClick}>
          <span className="click-here">👉🏻설문조사 링크👈🏻</span> 참여 부탁드립니다😂
          </div> */}
        </div>
      )}
    </div>
  );
};

export default Information;