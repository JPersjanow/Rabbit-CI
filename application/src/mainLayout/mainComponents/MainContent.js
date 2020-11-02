import React from 'react';
import '../mainComponentsStyle/MainContent.css'
import KanbanList from '../components/KanbanList'

const MainContent = (props) => {
    const userKanbans = props.userKanbans;
    return (
        <div className="mainContentStyle">
            <div className="contentTitle">
                <span>Your Kanbans</span>
            </div>
            <div className="assignedKanbanContainer">
                <div>
                    <span>Assigned kanban</span>
                </div>
                <div>
                    <KanbanList userKanbans={userKanbans} />
                </div>
            </div>
        </div>
    )
}


export default MainContent;