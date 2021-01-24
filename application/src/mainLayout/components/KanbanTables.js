import React, { useState } from "react";
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
    const userKanbanListButtonBackHandler = props.userKanbanListButtonBackHandler;
    const kanbanTablesContent = props.kanbanTablesContent;

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

    function handleUpdateIssue(issue_id, name) {
        //  console.log(issue_id);
        console.log(issue_id);
    }
    function handleClickIssue(id, index) {
        //  console.log('click', id);
        // console.log('click +index', index);
    }

    function handleDivClick(name) {
        // console.log('div', name);
    }
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
                <div style={{ display: "flex", justifyContent: "center", height: "100%" }}>
                    <DragDropContext
                        onDragEnd={result => onDragEnd(result, columns, setColumns)}

                    >
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
                                    <h2>{column.name}</h2>
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
                                                        {column.items.map((item, index) => {
                                                            return (
                                                                <Draggable
                                                                    key={item.issue.issue_id}
                                                                    draggableId={item.issue.issue_id}
                                                                    index={index}
                                                                    onClick={handleClickIssue(item.issue.issue_id, index)}
                                                                // onDragEnd={handleUpdateIssue(item.issue.issue_id, column.name, draggableId)}

                                                                >
                                                                    {(provided, snapshot) => {
                                                                        //   console.log(snapshot);
                                                                        return (
                                                                            <div
                                                                                onClick={handleDivClick(item.issue.name)}
                                                                                //  onDragEndCapture={handleUpdateIssue(item.issue.issue_id, column.name)}
                                                                                // onDropCapture={handleUpdateIssue(item.issue.issue_id, column.name)}
                                                                                ref={provided.innerRef}
                                                                                {...provided.draggableProps}
                                                                                {...provided.dragHandleProps}
                                                                                style={{
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
                                                                                <span>{item.issue.name}</span>
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