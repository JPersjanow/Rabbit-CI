import React from 'react';
import SingleTables from './SingleTables';
import '../componentsStyle/KanbanTables.css'

const KanbanTables = (props) => {
    const singleKanbanName = props.singleKanbanName;
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const kanbanTablesContent = props.kanbanTablesContent;
    console.log(kanbanTablesContent);
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
                <SingleTables kanbanTablesContent={kanbanTablesContent} />
            </div>
        </div>
    )
}

export default KanbanTables;