import React from 'react';
import '../componentsStyle/KanbanList.css'

const ListElement = (props) => {
    //console.log(props.userKanbans[0].kanban.info);
    const elements = props.userKanbans.map((item) => (
        <div key={item.kanban.info.id} className="kanbansRow">
            <span>{item.kanban.info.name}</span>
            <button onClick={() => props.userKanbanListButton(item.kanban.info.id)}
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