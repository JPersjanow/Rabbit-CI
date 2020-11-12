import React from 'react';
import '../componentsStyle/SingleTables.css'


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


const SingleTables = (props) => {
    const kanbanTablesContent = props.kanbanTablesContent
    console.log(kanbanTablesContent);
    const title = props.title
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