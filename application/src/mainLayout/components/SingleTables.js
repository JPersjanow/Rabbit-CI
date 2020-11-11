import React from 'react';
import '../componentsStyle/SingleTables.css'


const Tasks = (props) => {

    const task = <div>task</div>
    return task;
}


const SingleTables = (props) => {
    const kanbanTablesContent = props.kanbanTablesContent
    const title = props.title
    console.log(kanbanTablesContent);
    const tables = (
        <div className="singleTableStyle">
            <div className="tableTitle">
                <span>{title}</span>
            </div>
            <div className="tableContent">
                {kanbanTablesContent === null || kanbanTablesContent === [] || kanbanTablesContent === undefined ?
                    <span>nothing to show...</span>
                    : <Tasks kanbanTablesContent={kanbanTablesContent} />
                }
            </div>

        </div>
    )


    return tables;
}

export default SingleTables;