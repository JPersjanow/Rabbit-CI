import React from 'react';


const ListElement = (props) => {
    const elements = props.userKanbans.map((item, index) => (
        <div key={index}>
            <span>{item.kanbanName}</span>
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