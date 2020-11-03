import React from 'react';
import TopNav from './mainComponents/TopNav'
import LeftMenu from './mainComponents/LeftMenu'
import MainContent from './mainComponents/MainContent'
import './MainLayout.css'

class MainLayout extends React.Component {

    state = {
        userName: "user1",
        userKanbans: [
            {
                kanbanName: "Kanban1",
                tables: [
                    { toDo: "toDo1", }, { doing: " ", }, { done: "done1" }]
            },
            {
                kanbanName: "Kanban2", tables: [
                    { toDo: "" }, { doing: "doing2" }, { done: "done2" }]
            }, {
                kanbanName: "Kanban3", tables: [
                    { toDo: "toDo3" }, { doing: "doing3" }, { done: "done3" }]
            }, // each kanban has a few jobs
        ],                   // page from canva project
        userKanbansPage: true,        //page 1
        userKanbansTablePage: false, //page 2, 3
        automationPage: false,       //page 4
        singleJobPage: false,        // page 5
        kanbanTablesContent: [],
        singleKanbanName: "",
    }

    handleKanbanListButton = (kanbanName) => {
        const userTables = this.state.userKanbans;
        const chooseKanban = userTables.filter(tableName => tableName.kanbanName === kanbanName); //
        console.log(chooseKanban);
        const toDoTable = chooseKanban[0].tables[0];
        const doingTable = chooseKanban[0].tables[1];
        const doneTable = chooseKanban[0].tables[2];
        const kanbanTable = [toDoTable, doingTable, doneTable];
        this.setState({
            kanbanTablesContent: kanbanTable,
            userKanbansPage: false,
            userKanbansTablePage: true,
            singleKanbanName: kanbanName,
        })
    }

    handleKanbanListButtonBack = () => {
        this.setState({
            userKanbansPage: true,
            userKanbansTablePage: false,
            singleKanbanName: "",
        })
    }

    render() {
        const userKanbans = this.state.userKanbans;
        const userKanbansPage = this.state.userKanbansPage;
        const userKanbansTablePage = this.state.userKanbansTablePage;
        const automationPage = this.state.automationPage;
        const singleJobPage = this.state.singleJobPage;
        const userKanbanListButtonHandler = this.handleKanbanListButton;
        const userKanbanListButtonBackHandler = this.handleKanbanListButtonBack;
        const kanbanTablesContent = this.state.kanbanTablesContent;
        const singleKanbanName = this.state.singleKanbanName;
        return (
            <div className="mainLayout">
                <TopNav
                    userName={this.state.userName}
                />
                <div className="contentLayout">
                    <LeftMenu />
                    <MainContent
                        userKanbans={userKanbans}
                        isUserKanbansPage={userKanbansPage}
                        isuserKanbansTablePage={userKanbansTablePage}
                        isAutomationPage={automationPage}
                        isSingleJobPage={singleJobPage}
                        userKanbanListButton={userKanbanListButtonHandler}
                        userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                        kanbanTablesContent={kanbanTablesContent}
                        singleKanbanName={singleKanbanName}
                    />
                </div>
            </div>
        )
    }
}

export default MainLayout;