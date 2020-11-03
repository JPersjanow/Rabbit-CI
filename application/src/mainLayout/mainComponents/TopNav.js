import React from 'react';
import '../mainComponentsStyle/TopNav.css'

const TopNav = (props) => {
    const userName = props.userName;
    return (
        <div className="mainTopNavStyle">
            <div className="logoContainer">
                LOGO
            </div>
            <div className="userNameAndOptions">
                <span>{userName}</span>
                <button className="optionsButton">options</button>
            </div>
        </div>
    )
}


export default TopNav;