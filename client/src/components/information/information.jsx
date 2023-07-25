import React, { useState } from 'react';
import { CloseCircleFilled, BulbOutlined } from '@ant-design/icons';
import './information.css';
 
const MyComponent = () => {
  const [visible, setVisible] = useState(true);

  const handleToggle = () => {
    setVisible(!visible);
  };

  return (
    <div>
      {visible && (
        <div className="popup-container">
          <CloseCircleFilled className='popup-close'onClick={handleToggle} />
          <h2 className='popup-text'><BulbOutlined className='bulb' />코디를 클릭해,</h2>
          <h2 className='popup-text'><BulbOutlined className='bulb' />유사한 코디를 확인하세요!</h2>
        </div>
      )}
    </div>
  );
};

export default MyComponent;
