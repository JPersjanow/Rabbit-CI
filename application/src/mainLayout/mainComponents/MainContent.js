import React from 'react';
import '../mainComponentsStyle/MainContent.css'
import KanbanList from '../components/KanbanList'
import KanbanTables from '../components/KanbanTables'


const AssignedKanbanTable = (props) => {
    const userKanbans = props.userKanbans;
    const userKanbanListButton = props.userKanbanListButton
    const addNewKanbanButtonHandler = props.addNewKanbanButtonHandler
    const addNewKanbanVariable = props.addNewKanbanVariable;
    const handleSubmit = props.handleSubmit;
    const submit = props.submit;
    const handleChange = props.handleChange;
    return (
        <div>
            <div className="contentTitle">
                <span>Your Kanbans</span>
            </div>
            <div className="assignedKanbanContainer">
                <div>
                    <span>Assigned kanban</span>
                </div>
                <div>
                    <KanbanList
                        userKanbans={userKanbans}
                        userKanbanListButton={userKanbanListButton}
                        addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                        addNewKanbanVariable={addNewKanbanVariable}
                        handleSubmit={handleSubmit}
                        handleChange={handleChange}
                        submit={submit} />
                </div>
            </div>
        </div>
    )
}


class MainContent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            submit: props.submit,
            addNewKanbanVariable: props.addNewKanbanVariable,
            inputValue: "",
        }
    }

    handleChangeInputValue = (e) => {
        console.log(e.target.value);
        this.setState({
            inputValue: e.target.value,
        })
    }

    handleSubmit = () => {
        console.log("handle submit");
        if (this.state.inputValue === "") {
            return alert("need to write something")
        } else (
            this.setState({
                submit: true,
                addNewKanbanVariable: false,
            })
        )

    }


    render() {
        const {
            addNewKanbanVariable,
            addNewKanbanButtonHandler,
            userKanbans,
            singleKanbanName,
            userKanbanListButton,
            kanbanTablesContent,
            userKanbansTablePage,
            userKanbanListButtonBackHandler,
            submit } = this.props;
        const handleSubmit = this.handleSubmit;
        const handleInputValueChange = this.handleChangeInputValue;
        return (
            <div className="mainContentStyle">
                { kanbanTablesContent !== [] && userKanbansTablePage ?
                    <KanbanTables
                        singleKanbanName={singleKanbanName}
                        userKanbanListButtonBackHandler={userKanbanListButtonBackHandler}
                        kanbanTablesContent={kanbanTablesContent} />
                    : <AssignedKanbanTable
                        userKanbans={userKanbans}
                        userKanbanListButton={userKanbanListButton}
                        addNewKanbanButtonHandler={addNewKanbanButtonHandler}
                        addNewKanbanVariable={addNewKanbanVariable}
                        submit={submit}
                        handleSubmit={handleSubmit}
                        handleChange={handleInputValueChange} />
                }
            </div>
        )
    }

}


export default MainContent;