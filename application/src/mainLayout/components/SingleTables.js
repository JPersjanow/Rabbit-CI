import React, { useState } from 'react';
import '../componentsStyle/SingleTables.css'
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

const Tasks = (props) => {
    // map?

    console.log(props.kanbanTablesContent);

    const task = props.kanbanTablesContent.map((item, index) => (
        <div className="taskContainer" key={index}>
            <div>
                <span>{item.issue.name}</span>
            </div>
            <div>
                date: {item.issue.creation_date}
            </div>
        </div>

    ))

    return task;
}

const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

function SingleTables(props) {
    const [kanbanTablesContent, updatekanbanTablesContent] = useState(props.kanbanTablesContent);
    const title = useState(props.title);


    function handleOnDragEnd(result) {
        if (!result.destination) return;

        const items = kanbanTablesContent;
        const [reorderedItem] = items.splice(result.source.index, 1);
        items.splice(result.destination.index, 0, reorderedItem);

        updatekanbanTablesContent(items);
    }



    return (
        <div className="singleTableStyle">
            <div className="tableTitle">
                <span>{title}</span>
            </div>
            <div className="tableContent">
                {kanbanTablesContent === null || kanbanTablesContent === [] || kanbanTablesContent === undefined ?
                    <span>nothing to show...</span>
                    :
                    <DragDropContext onDragEnd={handleOnDragEnd}>
                        <Droppable droppableId={kanbanTablesContent}>
                            {(provided) => (
                                <div {...provided.droppableProps} ref={provided.innerRef}>
                                    {kanbanTablesContent.map((item, index) => {
                                        return (
                                            <Draggable key={item.issue.kanban_id} draggableId={item.issue.kanban_id} index={index}>
                                                {(provided) => (
                                                    <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                                                        <div className="taskContainer" key={index}>
                                                            <div>
                                                                <span>{item.issue.name}</span>
                                                            </div>
                                                            <div>
                                                                date: {item.issue.creation_date}
                                                            </div>
                                                        </div>
                                                    </div>

                                                )}
                                            </Draggable>

                                        )
                                    })}
                                    {provided.placeholder}
                                </div>
                            )}
                        </Droppable>
                    </DragDropContext>
                }
            </div>
        </div>
    )

};

export default SingleTables;