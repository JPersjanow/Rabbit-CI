import React from 'react';
import TopNav from './components/TopNav'
import LeftMenu from './components/LeftMenu'
import MainContent from './components/MainContent'
import './MainLayout.css'

class MainLayout extends React.Component {

    state = {
        userName: "user1",              // page from canva project
        userKanbansPage: true,        //page 1
        userKanbansTablePage: false, //page 2, 3
        automationPage: false,       //page 4
        singleJobPage: false,        // page 5
    }

    render() {
        return (
            <div className="mainLayout">
                <TopNav />
                <div className="contentLayout">
                    <LeftMenu />
                    <MainContent />
                </div>
            </div>
        )
    }
}

export default MainLayout;