import React from 'react';
import '../mainComponentsStyle/MainContent.css'
import KanbanList from '../components/KanbanList'
import KanbanTables from '../components/KanbanTables'


const AssignedKanbanTable = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler
    const addNewKanbanVariable = props.addNewKanbanVariable;
    const handleSubmit = props.handleSubmit;
    const submit = props.submit;
    const handleChange = props.handleChange;
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
                        handleSubmit={handleSubmit}
                        handleChange={handleChange}
                        submit={submit} />
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
    // const userKanbansTablePage = props.userKanbansTablePage;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const submit = props.submit;
    const isUserKanbansPage = props.isUserKanbansPage;
    const isuserKanbansTablePage = props.isuserKanbansTablePage;

    console.log(isUserKanbansPage);
    console.log(isuserKanbansTablePage);
    return (
        <div className="mainContentStyle">
            { isuserKanbansTablePage && !isUserKanbansPage ?
                <KanbanTables
                    singleKanbanName={singleKanbanName}
                    userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                    kanbanTablesContent={kanbanTablesContent} />
                : <AssignedKanbanTable
                    userKanbans={userKanbans}
                    userKanbanListButton={userKanbanListButton}
                    addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                    addNewKanbanVariable={addNewKanbanVariable}
                    submit={submit}
                />
            }
        </div>
    )

}


export default MainContent;