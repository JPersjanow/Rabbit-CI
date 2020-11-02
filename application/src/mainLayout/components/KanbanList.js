import React from 'react';
import '../componentsStyle/KanbanList.css'

const ListElement = (props) => {
    const elements = props.userKanbans.map((item, index) => (
        <div key={index} className="kanbansRow">
            <span>{item.kanbanName}</span>
            <button style={{ float: 'right' }}><i class="fa fa-arrow-right"></i></button>
        </div>
    ))
    return elements;
}


const KanbanList = (props) => {
    const userKanbans = props.userKanbans;
    return (
        <div>
            <ListElement userKanbans={userKanbans} />
            <button>Add new kanban</button>
        </div>
    )
}

export default KanbanList;