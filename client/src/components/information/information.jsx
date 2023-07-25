import React, { useState } from 'react';
import { CloseCircleFilled, BulbOutlined } from '@ant-design/icons';
import './information.css';
 
const MyComponent = (props) => {
  const [visible, setVisible] = useState(true);

  const handleToggle = () => {
    setVisible(!visible);
  };

  return (
    <div>
      {visible && (
        <div className="popup-container">
          <CloseCircleFilled className='popup-close'onClick={handleToggle} />
          <h2 className='popup-text'><BulbOutlined className='bulb' />하트를 눌러, 당신의 스타일을 찾아보세요!{props.text}</h2>
        </div>
      )}
    </div>
  );
};

export default MyComponent;
