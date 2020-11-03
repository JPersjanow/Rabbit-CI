import React from 'react';
import '../componentsStyle/KanbanList.css'

const ListElement = (props) => {
    const elements = props.userKanbans.map((item, index) => (
        <div key={index} className="kanbansRow">
            <span>{item.kanbanName}</span>
            <button onClick={() => props.userKanbanListButton(item.kanbanName)}
                style={{ float: 'right' }}>
                <i className="fa fa-arrow-right"></i>
            </button>
        </div>
    ))
    return elements;
}


const KanbanList = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton;
    return (
        <div>
            <ListElement
                userKanbans={userKanbans}
                userKanbanListButton={userKanbanListButton} />
            <button>Add new kanban</button>
        </div>
    )
}

export default KanbanList;