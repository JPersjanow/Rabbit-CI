import React from 'react';
import '../mainComponentsStyle/MainContent.css'
import KanbanList from '../components/KanbanList'
import KanbanTables from '../components/KanbanTables'


const AssignedKanbanTable = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton
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
                        userKanbanListButton={userKanbanListButton} />
                </div>
            </div>
        </div>
    )
}


const MainContent = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton
    const kanbanTablesContent = props.kanbanTablesContent;
    const userKanbansPage = props.isUserKanbansPage;
    const userKanbansTablePage = props.isuserKanbansTablePage;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    return (
        <div className="mainContentStyle">
            { kanbanTablesContent !== [] && userKanbansTablePage ?
                <KanbanTables
                    userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                    kanbanTablesContent={kanbanTablesContent} />
                : <AssignedKanbanTable
                    userKanbans={userKanbans}
                    userKanbanListButton={userKanbanListButton} />

            }


        </div>
    )
}


export default MainContent;