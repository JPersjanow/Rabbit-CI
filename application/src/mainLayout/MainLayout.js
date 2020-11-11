import React from 'react';
import TopNav from './mainComponents/TopNav'
import LeftMenu from './mainComponents/LeftMenu'
import MainContent from './mainComponents/MainContent'
import './MainLayout.css'

class MainLayout extends React.Component {

    state = {
        userName: "user1",
        userKanbans: [],               // page from canva project
        userKanbansPage: true,        //page 1
        userKanbansTablePage: false, //page 2, 3
        automationPage: false,       //page 4
        singleJobPage: false,        // page 5
        kanbanTablesContent: [],
        singleKanbanName: "",
        addNewKanban: false,
        addedKanbanName: "",
        sumbmitState: 1,
    }

    componentDidMount() {
        const query = "http://localhost:5000/api/v1/resources/kanbans/"; // http instead of https
        fetch(query).then(response => {
            if (response.ok) {
                console.log(response);
                return response // need this to clear data and take array
            }
            throw Error(response.status)
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                this.setState({
                    userKanbans: data
                })
            })
            .catch(error => console.log(error))
    }

    handleKanbanListButton = (kanbanId) => {
        // console.log(kanbanId);
        const userTables = this.state.userKanbans;
        const chooseKanban = userTables.filter(item => item.kanban.info.id === kanbanId); //
        // console.log(chooseKanban);
        const thiskanbanName = chooseKanban[0].kanban.info.name;
        const todOTable = chooseKanban[0].kanban.todo;
        const doingTable = chooseKanban[0].kanban.doing;
        const doneTable = chooseKanban[0].kanban.done;
        const chooseKanbanIssue = { toDo: todOTable, doing: doingTable, done: doneTable };
        // console.log(chooseKanbanIssue);
        this.setState({
            kanbanTablesContent: chooseKanbanIssue,
            userKanbansPage: false,
            userKanbansTablePage: true,
            singleKanbanName: thiskanbanName,
        })

    }

    handleKanbanListButtonBack = () => {
        this.setState({
            userKanbansPage: true,
            userKanbansTablePage: false,
            singleKanbanName: "",
        })
    }

    hanldeAddNewKanban = () => {
        console.log("add new kanban");
        this.setState({
            addNewKanban: true,
            sumbmitState: 2,
        })
    }

    handleChange = (e) => {
        let inputValue = e.target.value;
        console.log(inputValue);
        this.setState({
            addedKanbanName: inputValue,
        });
    }

    handleSubmitNewKanban = () => {
        console.log("handleSubmitNewKanban");
        const addedKanbanName = this.state.addedKanbanName
        const actualKanbansList = this.state.userKanbans;
        const actualKanbansListLength = actualKanbansList.length;
        let addedKanbanId = actualKanbansListLength + 1;
        let addedKanban = {
            kanban:
            {
                doing: null,
                done: null, todo: null, info: {
                    description: "",
                    id: addedKanbanId,
                    name: addedKanbanName,
                }
            }
        };
        console.log(addedKanban);
        const userKanbansActual = this.state.userKanbans;
        console.log(userKanbansActual)
        const userKanbansupdate = this.state.userKanbans.concat(addedKanban);
        console.log(userKanbansupdate);
        this.setState({
            userKanbans: userKanbansupdate,
            sumbmitState: 1,
            addNewKanban: false,
        });
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
        const addNewKanbanButtonHandler = this.hanldeAddNewKanban;
        const addNewKanbanVariable = this.state.addNewKanban;
        const sumbmitState = this.state.sumbmitState;
        const inputChangeHandler = this.handleChange;
        const submitNewKanbanHandler = this.handleSubmitNewKanban;
        return (
            <div className="mainLayout">
                <TopNav
                    userName={this.state.userName}
                />
                <div className="contentLayout">
                    <LeftMenu
                        userKanbansTablePage={userKanbansTablePage} />
                    <MainContent
                        userKanbans={userKanbans}
                        isUserKanbansPage={userKanbansPage}
                        isuserKanbansTablePage={userKanbansTablePage}
                        isAutomationPage={automationPage}
                        isSingleJobPage={singleJobPage}
                        userKanbanListButton={userKanbanListButtonHandler}
                        userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                        addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                        kanbanTablesContent={kanbanTablesContent}
                        singleKanbanName={singleKanbanName}
                        addNewKanbanVariable={addNewKanbanVariable}
                        sumbmitState={sumbmitState}
                        inputChangeHandler={inputChangeHandler}
                        submitNewKanbanHandler={submitNewKanbanHandler}
                    />
                </div>
            </div>
        )
    }
}

export default MainLayout;