import React from 'react';
import '../mainComponentsStyle/TopNav.css'
import logo from '../../images/logo.png';

const TopNav = (props) => {
    const userName = props.userName;
    return (
        <div className="mainTopNavStyle">
            <div className="logoContainer">
                <img src={logo} alt="Logo" className="logoStyle" />
            </div>
            <div className="userNameAndOptions">
                <span>{userName}</span>
                <button className="optionsButton">options</button>
            </div>
        </div>
    )
}


export default TopNav;