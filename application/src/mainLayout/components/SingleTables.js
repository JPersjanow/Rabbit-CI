import React from 'react';
import '../componentsStyle/SingleTables.css'


const SingleTables = (props) => {
    const kanbanTablesContent = props.kanbanTablesContent

    const tables = kanbanTablesContent.map((item, index) => (
        <div key={index} className="singleTableStyle">
            <div className="tableTitle">
                <span>{item.toDo}</span>
            </div>
            <div className="tableContent">
                <spna>{item.toDo}</spna>
            </div>

        </div>
    ))


    return tables;
}

export default SingleTables;