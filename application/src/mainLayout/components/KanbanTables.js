import React from 'react';
import SingleTables from './SingleTables';
import '../componentsStyle/KanbanTables.css'

const KanbanTables = (props) => {
    const singleKanbanName = props.singleKanbanName;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const kanbanTablesContent = props.kanbanTablesContent;
    console.log(kanbanTablesContent);
    const toDoTable = kanbanTablesContent.toDo;
    const doing = kanbanTablesContent.doing;
    const done = kanbanTablesContent.done
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
                <SingleTables kanbanTablesContent={doing} title={doingTitle} />
                <SingleTables kanbanTablesContent={done} title={doneTitle} />
            </div>
        </div>
    )
}

export default KanbanTables;