import React, { useState } from 'react';
import '../componentsStyle/SingleTables.css'
//import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";



function SingleTables(props) {
    const [kanbanTablesContent] = useState(props.kanbanTablesContent);
    const title = useState(props.title);





    return (
        <div className="singleTableStyle">
            <div className="tableTitle">
                <span>{title}</span>
            </div>
            <div className="tableContent">
                {kanbanTablesContent === null || kanbanTablesContent === [] || kanbanTablesContent === undefined ?
                    <span>nothing to show...</span>
                    :
                    <div>

                    </div>
                }
            </div>
        </div>
    )

};

export default SingleTables;