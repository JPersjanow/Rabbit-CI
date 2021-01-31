import React, { useEffect, useState } from "react";
//import SingleTables from './SingleTables';
import '../componentsStyle/KanbanTables.css'
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";
import { v4 as uuidv4 } from 'uuid';

const onDragEnd = (result, columns, setColumns) => {
    if (!result.destination) return;
    const { source, destination } = result;

    if (source.droppableId !== destination.droppableId) {
        const sourceColumn = columns[source.droppableId];
        const destColumn = columns[destination.droppableId];
        const sourceItems = [...sourceColumn.items];
        const destItems = [...destColumn.items];
        const [removed] = sourceItems.splice(source.index, 1);
        destItems.splice(destination.index, 0, removed);
        setColumns({
            ...columns,
            [source.droppableId]: {
                ...sourceColumn,
                items: sourceItems
            },
            [destination.droppableId]: {
                ...destColumn,
                items: destItems
            }
        });
    } else {
        const column = columns[source.droppableId];
        const copiedItems = [...column.items];
        const [removed] = copiedItems.splice(source.index, 1);
        copiedItems.splice(destination.index, 0, removed);
        setColumns({
            ...columns,
            [source.droppableId]: {
                ...column,
                items: copiedItems
            }
        });
    }
};

const KanbanTables = (props) => {
    const singleKanbanName = props.singleKanbanName;
    const [kanbanTablesContent, setKanbanTablesContent] = useState(props.kanbanTablesContent);

    const [addedStatus, setAddedStatus] = useState(false);
    const [newIssueName, setNewIssueName] = useState('');
    let value;
    // const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    //let kanbanTablesContent = props.kanbanTablesContent;
    const kanbanID = props.kanbanID;
    const toDoTable = kanbanTablesContent.filter(item => item.issue.stage === "todo");
    const doingTable = kanbanTablesContent.filter(item => item.issue.stage === "doing");
    const doneTable = kanbanTablesContent.filter(item => item.issue.stage === "done");

    const taskColumns = {
        [uuidv4()]: {
            name: 'TO DO',
            items: toDoTable,
        },
        [uuidv4()]: {
            name: 'DOING',
            items: doingTable,
        },
        [uuidv4()]: {
            name: 'DONE',
            items: doneTable
        }
    }
    const [columns, setColumns] = useState(taskColumns);


    function refreshIssue(kanbanID) {
        console.log('ref');
        const query = `http://localhost:5000/api/v1/resources/kanbans/${kanbanID}/issues`; // http instead of https
        fetch(query).then(response => {
            if (response.ok) {
                console.log(response);
                return response // need this to clear data and take array
            }
            throw Error(response.status)
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                setKanbanTablesContent(data);
            })
            .catch(error => console.log(error))
    }


    function updateStage(kanban_id, issue_id, stageName) {
        let changedStage = {
            "stage": stageName
        }
        fetch(`http://localhost:5000/api/v1/resources/kanbans//${kanban_id}/issues/${issue_id}/stage`, {
            method: 'PUT',
            headers: { "Content-Type": "application/json", 'Accept': 'application/json', },
            body: JSON.stringify(changedStage),
            // mode: 'no-cors' update working without this

        })
            .catch(err => console.log(err));
    }

    function checkIssueID(array, stageName) {
        if (array !== []) {
            for (let j in array) {
                if (array[j].issue.stage !== stageName) {
                    updateStage(array[j].issue.kanban_id, array[j].issue.issue_id, stageName)
                }
            }
        }
    }

    useEffect(() => {
        let toDoTableAfter;
        let doingTableAfter;
        let doneTableAfter;
        for (let i in columns) {
            if (columns[i].name === 'TO DO') {
                toDoTableAfter = columns[i].items;
            }
            if (columns[i].name === 'DOING') {
                doingTableAfter = columns[i].items;
            }
            if (columns[i].name === 'DONE') {
                doneTableAfter = columns[i].items;
            }
        }
        checkIssueID(toDoTableAfter, 'todo');
        checkIssueID(doingTableAfter, 'doing');
        checkIssueID(doneTableAfter, 'done');
    })

    function handleRemoveIssueButton(kanban_id, issue_id) {
        console.log(issue_id);
        fetch(`http://localhost:5000/api/v1/resources/kanbans/${kanban_id}/issues/${issue_id}`, {
            method: 'DELETE',
            headers: { "Content-Type": "application/json", 'Accept': 'application/json', },
            body: null,
            //mode: 'no-cors', delete working without this

        })
            .catch(err => console.log(err));

    }

    function handleAddIssu(columnId) {
        console.log(columnId);
        setAddedStatus(true);
    }

    function handleIssueNameChange(e) {
        let inputValue = e.target.value;
        setNewIssueName(inputValue);
    }

    function submitNewIssue(kanbanID) {
        if (newIssueName === "") {
            return alert("need to write new issue name!");
        }
        else {
            let newIssue = {
                "name": newIssueName,
                "description": "string",
                "creator": "string"
            }
            setAddedStatus(false);
            fetch(`http://localhost:5000/api/v1/resources/kanbans/${kanbanID}/issues`, {
                method: 'POST',
                headers: { "Content-Type": "application/json", 'Accept': 'application/json', },
                body: JSON.stringify(newIssue),
                mode: 'no-cors'

            })
                .catch(err => console.log(err));
            // refreshIssue(kanbanID);
        }

    }

    function cancelButtonHandler() {
        setNewIssueName('');
        setAddedStatus(false);
    }

    return (
        <div className="kanbanTablesStyle">
            <div className="contentTitle">
                <span>{singleKanbanName}</span>
            </div>
            <div className="kanbanTablesContainer">
                <div style={{ display: "flex", justifyContent: "center", height: "100%" }}>
                    <DragDropContext
                        onDragEnd={result => onDragEnd(result, columns, setColumns)}>
                        {Object.entries(columns).map(([columnId, column], index) => {
                            return (
                                <div
                                    style={{
                                        display: "flex",
                                        flexDirection: "column",
                                        alignItems: "center"
                                    }}
                                    key={columnId}
                                >
                                    <div className='tableTitle'>
                                        <h2>{column.name}</h2>
                                        {column.name === 'TO DO' ? <button onClick={() => handleAddIssu(columnId)}>+</button> : null}
                                    </div>
                                    <div style={{ margin: 8 }}>
                                        <Droppable droppableId={columnId} key={columnId}>
                                            {(provided, snapshot) => {
                                                return (
                                                    <div
                                                        {...provided.droppableProps}
                                                        ref={provided.innerRef}
                                                        style={{
                                                            background: snapshot.isDraggingOver
                                                                ? "#E2E2E2"
                                                                : "lightgrey",
                                                            padding: 4,
                                                            width: 250,
                                                            minHeight: 500
                                                        }}
                                                    >
                                                        {addedStatus && column.name === 'TO DO' ?
                                                            <div className='addedIssueBox'>
                                                                <input
                                                                    type='text'
                                                                    value={value}
                                                                    onChange={handleIssueNameChange}
                                                                    placeholder="Write new issue name..."></input>
                                                                <button onClick={() => cancelButtonHandler()}
                                                                    style={{ fontSize: '16px', fontFamily: 'fontawesome' }}>
                                                                    <i className="fas fa-times"></i>
                                                                </button>
                                                                <button onClick={() => submitNewIssue(kanbanID)}
                                                                    style={{ fontSize: '16px', fontFamily: 'fontawesome' }}>
                                                                    <i className="fas fa-check"></i>
                                                                </button>

                                                            </div>
                                                            : null}
                                                        {column.items.map((item, index) => {
                                                            return (
                                                                <Draggable
                                                                    key={item.issue.issue_id}
                                                                    draggableId={item.issue.issue_id}
                                                                    index={index}>
                                                                    {(provided, snapshot) => {

                                                                        return (
                                                                            <div
                                                                                ref={provided.innerRef}
                                                                                {...provided.draggableProps}
                                                                                {...provided.dragHandleProps}
                                                                                style={{
                                                                                    display: 'grid',
                                                                                    userSelect: "none",
                                                                                    padding: 16,
                                                                                    margin: "0 0 8px 0",
                                                                                    minHeight: "50px",
                                                                                    backgroundColor: snapshot.isDragging
                                                                                        ? '#FFDC6A'
                                                                                        : '#FFA887',
                                                                                    color: "white",
                                                                                    ...provided.draggableProps.style
                                                                                }}
                                                                            >
                                                                                <div style={{ position: 'relative' }}>
                                                                                    <span>{item.issue.name}</span>
                                                                                    <button onClick={() =>
                                                                                        handleRemoveIssueButton(item.issue.kanban_id, item.issue.issue_id)}
                                                                                        className='deleteIssue'>
                                                                                        <i className="fas fa-times"></i></button>
                                                                                </div>
                                                                                <span>{item.issue.creation_date}</span>
                                                                            </div>
                                                                        );
                                                                    }}
                                                                </Draggable>
                                                            );
                                                        })}
                                                        {provided.placeholder}
                                                    </div>
                                                );
                                            }}
                                        </Droppable>
                                    </div>
                                </div>
                            );
                        })}
                    </DragDropContext>
                </div>
            </div>
        </div>
    )
}

export default KanbanTables;