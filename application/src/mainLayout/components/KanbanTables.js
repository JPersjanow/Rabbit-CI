import React from 'react';
import SingleTables from './SingleTables';
import '../componentsStyle/KanbanTables.css'

const KanbanTables = (props) => {
    const singleKanbanName = props.singleKanbanName;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const kanbanTablesContent = props.kanbanTablesContent;


    const toDoTable = kanbanTablesContent.filter(item => item.issue.stage === "todo");
    const doingTable = kanbanTablesContent.filter(item => item.issue.stage === "doing");
    const doneTable = kanbanTablesContent.filter(item => item.issue.stage === "done");

    const doToTitle = "ToDO";
    const doingTitle = "Doing";
    const doneTitle = "Done";

    return (
        <div className="kanbanTablesStyle">
            <div className="backButtonContainer">
                <button onClick={() => userKanbanListButtonBackHandler()}
                    style={{ float: 'left' }}>
                    <i className="fa fa-arrow-left"></i>
                </button>
            </div>
            <div className="contentTitle">
                <span>{singleKanbanName}</span>
            </div>
            <div className="kanbanTablesContainer">
                <SingleTables kanbanTablesContent={toDoTable} title={doToTitle} />
                <SingleTables kanbanTablesContent={doingTable} title={doingTitle} />
                <SingleTables kanbanTablesContent={doneTable} title={doneTitle} />
            </div>
        </div>
    )
}

export default KanbanTables;