import React from 'react';
import '../mainComponentsStyle/LeftMenu.css'


const LeftMenu = (props) => {
    const userKanbansTablePage = props.userKanbansTablePage;
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    return (
        <div className="leftMenuStyle">
            {userKanbansTablePage ?
                <div className="kanbanButtonsContianer">
                    <button
                        onClick={() => userKanbanListButtonBackHandler()}
                        className="mainButtonStyle">
                        <span>Kanban list</span>
                    </button>
                    <button className="mainButtonStyle"><span>Add issue </span></button>
                </div>
                : <div className="kanbanButtonsContianer">
                    <button
                        onClick={() => addNewKanbanButtonHandler()}
                        className="addKanbanButton"> <span>
                            Add Kanban </span></button>
                </div>}

            <div className="automationAndConfiguration">
                <div className="buttonsMenuContainer">
                    <button className="automationBtn mainButtonStyle">
                        <span>Automation Module </span></button>
                    <button className="configurationBtn mainButtonStyle">
                        <span> Configuration </span></button>
                </div>

            </div>
        </div>
    )
}


export default LeftMenu;