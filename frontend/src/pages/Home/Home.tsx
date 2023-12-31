import { observer } from "mobx-react-lite";
import { FC } from "react";
import './Home.scss';
import styled from "styled-components";
import { Route, Routes, useNavigate } from "react-router-dom";


const HomePage:FC = () => {
    return(
        <div className="home-page">
            <HomePageBody>
                <Routes>
                    <Route path="/home">
                        <Route path="scenarios" element={<div>Scenarios</div>}/>

                    </Route>
                </Routes>
            </HomePageBody>
        </div>
    )
}

const HomePageHeader = styled.div`
    display: flex;
    justify-content: space-between;
    height: 80px;
    border: 1px solid #5e5e5e;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 10px 20px;
`

const HomePageHeaderLeftCotainer = styled.div`
    padding: 10px;
    
`

const HomePageHeaderRightCotainer = styled.div`
    padding: 10px;
    
`

const NavButton = styled.button`
    background: none;
    border-radius: 10px;
    border: 1px solid #5e5e5e;
    padding: 5px 20px;
    font-size: 18px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;

    &:hover{
        box-shadow: 0 0 10px 5px rgba(0,0,0,0.1);
        transform: scale(1.1);
    }
`

const HomePageBody = styled.div`
    display: flex;
    margin: 20px 40px;
    padding: 10px;
    border: 1px solid red;
`


export default observer(HomePage)