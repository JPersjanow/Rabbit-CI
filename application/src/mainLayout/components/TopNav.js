import React from 'react';
import '../componentsStyle/TopNav.css'

const TopNav = () => {
    return (
        <div className="mainTopNavStyle">
            <div className="logoContainer">
                LOGO
            </div>
            <div className="userNameAndOptions">
                <span>userName</span>
                <button className="optionsButton">options</button>
            </div>
        </div>
    )
}


export default TopNav;