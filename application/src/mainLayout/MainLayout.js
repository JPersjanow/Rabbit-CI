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
    }

    componentDidMount() {
        const query = "http://localhost:5000/api/v1/resources/kanbans/all"; // http instead of https
        fetch(query).then(response => {
            if (response.ok) {
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
        console.log(kanbanId);

        const userTables = this.state.userKanbans;
        const chooseKanban = userTables.filter(item => item.kanban.info.id === kanbanId); //
        console.log(chooseKanban);
        const chooseKanbanIssue = chooseKanban[0].kanban.info.issues;
        console.log(chooseKanbanIssue);
        this.setState({
            kanbanTablesContent: chooseKanbanIssue,
            userKanbansPage: false,
            userKanbansTablePage: true,
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
                        kanbanTablesContent={kanbanTablesContent}
                        singleKanbanName={singleKanbanName}
                    />
                </div>
            </div>
        )
    }
}

export default MainLayout;