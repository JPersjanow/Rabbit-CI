import React from 'react';
import SingleTables from './SingleTables';

const KanbanTables = (props) => {
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const kanbanTablesContent = props.kanbanTablesContent;
    console.log(kanbanTablesContent);
    return (
        <div>
            <div>
                <button onClick={() => userKanbanListButtonBackHandler()}
                    style={{ float: 'left' }}>
                    <i className="fa fa-arrow-left"></i>
                </button>
            </div>
            <div className="kanbanTablesContainer">
                <SingleTables kanbanTablesContent={kanbanTablesContent} />
            </div>
        </div>
    )
}

export default KanbanTables;