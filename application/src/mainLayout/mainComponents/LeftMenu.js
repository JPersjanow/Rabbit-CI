import React from 'react';
import '../mainComponentsStyle/LeftMenu.css'


const LeftMenu = (props) => {
    const userKanbansTablePage = props.userKanbansTablePage;
    return (
        <div className="leftMenuStyle">
            {userKanbansTablePage ?
                <div className="kanbanButtonsContianer">
                    <button className="btnColor">Kanban list</button>
                    <button className="btnColor">Add issue</button>
                </div>
                : <div className="kanbanButtonsContianer">
                    <button className="btnColor">Add Kanban</button>
                </div>}

            <div className="automationAndConfiguration">
                <div className="buttonsMenuContainer">
                    <button className="automationBtn btnColor">Automation Module</button>
                    <button className="configurationBtn btnColor"> Configuration</button>
                </div>

            </div>
        </div>
    )
}


export default LeftMenu;