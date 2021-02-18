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
        currentKanbanID: '',
    }


    handleRefreshKanbans = () => {
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

    componentDidMount() {
        this.handleRefreshKanbans();
    }

    handleKanbanListButton = (kanbanId) => {
        const userTables = this.state.userKanbans;
        const chooseKanban = userTables.filter(item => item.kanban.info.id === kanbanId); //
        const thiskanbanName = chooseKanban[0].kanban.info.name;
        const queryChoosenKanbanIssue = `http://localhost:5000/api/v1/resources/kanbans/${kanbanId}/issues`
        fetch(queryChoosenKanbanIssue).then(response => {
            if (response.ok) {
                return response
            }
            throw Error(response.status)
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                this.setState({
                    kanbanTablesContent: data,
                    userKanbansPage: false,
                    userKanbansTablePage: true,
                    singleKanbanName: thiskanbanName,
                    currentKanbanID: kanbanId,
                })
            })
            .catch(error => console.log(error))
    }

    handleKanbanListButtonBack = () => {
        this.setState({
            kanbanTablesContent: [],
            userKanbansPage: true,
            userKanbansTablePage: false,
            singleKanbanName: "",
            currentKanbanID: '',
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
        this.setState({
            addedKanbanName: inputValue,
        });
    }

    handleSubmitNewKanban = () => {
        const addedKanbanName = this.state.addedKanbanName
        if (addedKanbanName === "") {
            return alert("need to write new kanban name!");
        } else {
            let addedKanban = {
                "name": addedKanbanName,
                "description": "abc",
            }
            this.setState({
                sumbmitState: 1,
                addNewKanban: false,
                addedKanbanName: "",
            });

            fetch('http://localhost:5000/api/v1/resources/kanbans/', {
                method: 'POST',
                headers: { "Content-Type": "application/json", 'Accept': 'application/json', },
                body: JSON.stringify(addedKanban),
                mode: 'no-cors'

            })
                .catch(err => console.log(err));
        };
        this.handleRefreshKanbans();
    }

    handleCancelButton = () => {
        this.setState({
            sumbmitState: 1,
            addNewKanban: false,
            addedKanbanName: "",
        });
    }
    handleAutomationModuleButton = () => {
        this.setState({
            automationPage: !this.state.automationPage,
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
        const addNewKanbanButtonHandler = this.hanldeAddNewKanban;
        const addNewKanbanVariable = this.state.addNewKanban;
        const sumbmitState = this.state.sumbmitState;
        const inputChangeHandler = this.handleChange;
        const submitNewKanbanHandler = this.handleSubmitNewKanban;
        const cancelButtonHandler = this.handleCancelButton;
        const currentKanbanID = this.state.currentKanbanID;
        const handleAutomationModuleButton = this.handleAutomationModuleButton;
        return (
            <div className="mainLayout">
                <TopNav
                    userName={this.state.userName}
                />
                <div className="contentLayout">
                    <LeftMenu
                        userKanbansTablePage={userKanbansTablePage}
                        addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                        userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                        handleAutomationModuleButton={handleAutomationModuleButton} />
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
                        cancelButtonHandler={cancelButtonHandler}
                        currentKanbanID={currentKanbanID}
                    />
                </div>
            </div>
        )
    }
}

export default MainLayout;