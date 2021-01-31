import React from 'react';
import '../mainComponentsStyle/MainContent.css'
import KanbanList from '../components/KanbanList'
import KanbanTables from '../components/KanbanTables'


const AssignedKanbanTable = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler
    const addNewKanbanVariable = props.addNewKanbanVariable;
    const sumbmitState = props.sumbmitState;
    const inputChangeHandler = props.inputChangeHandler;
    const submitNewKanbanHandler = props.submitNewKanbanHandler;
    const cancelButtonHandler = props.cancelButtonHandler;
    return (
        <div>
            <div className="contentTitle">
                <span>Your Kanbans</span>
            </div>
            <div className="assignedKanbanContainer">
                <div>
                    <span>Assigned kanban</span>
                </div>
                <div>
                    <KanbanList
                        userKanbans={userKanbans}
                        userKanbanListButton={userKanbanListButton}
                        addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                        addNewKanbanVariable={addNewKanbanVariable}
                        inputChangeHandler={inputChangeHandler}
                        sumbmitState={sumbmitState}
                        submitNewKanbanHandler={submitNewKanbanHandler}
                        cancelButtonHandler={cancelButtonHandler} />
                </div>
            </div>
        </div>
    )
}


const MainContent = (props) => {
    const addNewKanbanVariable = props.addNewKanbanVariable;
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler;
    const userKanbans = props.userKanbans;
    const singleKanbanName = props.singleKanbanName;
    const userKanbanListButton = props.userKanbanListButton;
    const kanbanTablesContent = props.kanbanTablesContent;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const sumbmitState = props.sumbmitState;
    const isUserKanbansPage = props.isUserKanbansPage;
    const isuserKanbansTablePage = props.isuserKanbansTablePage;
    const inputChangeHandler = props.inputChangeHandler;
    const submitNewKanbanHandler = props.submitNewKanbanHandler;
    const cancelButtonHandler = props.cancelButtonHandler;
    const kanbanID = props.currentKanbanID;
    return (
        <div className="mainContentStyle">
            { isuserKanbansTablePage && !isUserKanbansPage ?
                <KanbanTables
                    singleKanbanName={singleKanbanName}
                    userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                    kanbanTablesContent={kanbanTablesContent}
                    kanbanID={kanbanID} />


                : <AssignedKanbanTable
                    userKanbans={userKanbans}
                    userKanbanListButton={userKanbanListButton}
                    addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                    addNewKanbanVariable={addNewKanbanVariable}
                    sumbmitState={sumbmitState}
                    inputChangeHandler={inputChangeHandler}
                    submitNewKanbanHandler={submitNewKanbanHandler}
                    cancelButtonHandler={cancelButtonHandler}
                />
            }
        </div>
    )

}


export default MainContent;