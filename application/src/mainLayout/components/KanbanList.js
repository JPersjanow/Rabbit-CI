import React from 'react';
import '../componentsStyle/KanbanList.css'

const ListElement = (props) => {
    const elements = props.userKanbans.map((item) => (
        <div key={item.kanban.info.id} className="kanbansRow">
            <span>{item.kanban.info.name}</span>
            <button onClick={() => props.userKanbanListButton(item.kanban.info.id)}
                style={{ float: 'right', fontSize: '16px', fontFamily: 'fontawesome !important' }}>
                <i className="fa fa-arrow-right"></i>
            </button>
        </div>
    ))
    return elements;
}

const NewListElement = (props) => {
    const handleValueChange = props.handleValueChange;
    const submitNewKanbanHandler = props.submitNewKanbanHandler;
    const cancelButtonHandler = props.cancelButtonHandler;
    let nameValue;
    return (
        <div className="kanbansRow">
            <input
                type="text"
                id="kanbanNameId"
                value={nameValue}
                onChange={handleValueChange}
                placeholder="Write new kanban name..."
                name="newKanbanName"
            />
            <button onClick={() => cancelButtonHandler()}
                style={{ fontSize: '16px', fontFamily: 'fontawesome' }}>
                <i className="fas fa-times"></i>
            </button>
            <button onClick={() => submitNewKanbanHandler()}
                style={{ float: 'right', fontSize: '16px', fontFamily: 'fontawesome' }}>
                <i className="fas fa-check"></i>
            </button>

        </div>

    )
}


const KanbanList = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton;
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler
    const addNewKanbanVariable = props.addNewKanbanVariable;
    const handleSubmit = props.handleSubmit;
    const sumbmitState = props.sumbmitState;
    const inputChangeHandler = props.inputChangeHandler;
    const submitNewKanbanHandler = props.submitNewKanbanHandler;
    const cancelButtonHandler = props.cancelButtonHandler;
    console.log(addNewKanbanVariable);
    return (
        <div>
            <ListElement
                userKanbans={userKanbans}
                userKanbanListButton={userKanbanListButton} />
            {addNewKanbanVariable === true && sumbmitState === 2 ?
                <NewListElement
                    submitNewKanbanHandler={submitNewKanbanHandler}
                    handleSubmit={handleSubmit}
                    handleValueChange={inputChangeHandler}
                    cancelButtonHandler={cancelButtonHandler} /> : null}
            <button onClick={() => addNewKanbanButtonHandler()}>Add new kanban</button>
        </div>
    )
}

export default KanbanList;