import { PlusIcon } from "@icons/Plus"
import { FC } from "react"
import styled from "styled-components"


interface IScenarioAdd{
    onClick: () => void
}
export const AddScenarioButton: FC<IScenarioAdd> = ({onClick}) => {
    return(
        <Container>
            <IconContainer> <PlusIcon width="24" height="24" fill="#fff"/> </IconContainer>
            <TextContainer> Добавить сценарий </TextContainer>
        </Container>
    )
}


const Container = styled.div`
    display: flex;
    width: 700px;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;

    gap: 20px;

    font-size: 18px;
    font-weight: 500;
    background-color: rgba(22, 145, 22, 0.6);
    color: #fff;

    border: none;
    border-radius: 10px;

    cursor: pointer;

    transition: all 0.2s;

    &:hover{
        box-shadow: 0 0  10px 5px rgba(22, 145, 22, 0.6);
        transform: scale(1.05);
    }
`

const IconContainer = styled.div`
    width: 25px;
    height: 25px;
`

const TextContainer = styled.div`
    
`