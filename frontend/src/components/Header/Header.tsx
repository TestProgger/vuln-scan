import { observer } from "mobx-react-lite";
import { FC } from "react";
import styled from "styled-components";
import { Route, Routes, useNavigate } from "react-router-dom";
import { usePersistentStore } from "@store";


const Header:FC = () => {
    const navigate = useNavigate()
    const rootStore = usePersistentStore()


    return(
        <HomePageHeader>
            <HomePageHeaderLeftCotainer>
                <NavButton onClick={() => navigate('/scenarios')}> Сценарии </NavButton>
            </HomePageHeaderLeftCotainer>
            <HomePageHeaderRightCotainer>
                <NavButton onClick={() => rootStore.logout()}> Выход </NavButton>
            </HomePageHeaderRightCotainer>
        </HomePageHeader>
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


export default observer(Header)