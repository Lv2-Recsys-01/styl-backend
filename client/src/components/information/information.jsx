import React, { useState } from 'react';
import { CloseCircleFilled } from '@ant-design/icons';
import './information.css';
 
const Information = (props) => {
  const [visible, setVisible] = useState(true);

  const handleToggle = () => {
    setVisible(!visible);
  };

  return (
    <div>
      {visible && (
        <div className="popup-container">
          <CloseCircleFilled className='popup-close'onClick={handleToggle} />
          <h2 className='popup-text'>{props.text}</h2>
        </div>
      )}
    </div>
  );
};

export default Information;
