import React from 'react';
import '../componentsStyle/LeftMenu.css'


const LeftMenu = (props) => {
    return (
        <div className="leftMenuStyle">
            <div className="kanbanButtonsContianer">
                <button>Add Kanban</button>
            </div>
            <div className="automationAndConfiguration">
                <div className="buttonsMenuContainer">
                    <button className="automationBtn">Automation Module</button>
                    <button className="configurationBtn"> Configuration</button>
                </div>

            </div>
        </div>
    )
}


export default LeftMenu;