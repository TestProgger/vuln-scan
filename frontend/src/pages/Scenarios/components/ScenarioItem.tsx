import { FC } from "react"
import styled from "styled-components"

interface IScenarioItem{
    index: number
    id: string
    name: string
    created_at: string | Date
    onClick: () => void
}
export const ScenarioItem: FC<IScenarioItem>  = ({ index, id, name, created_at, onClick }) => {
    return(
        <ScenarioItemContainer onClick={() => onClick()}>
            <ScenarioTextContainer>
                <ScenarioItemIndex> {`${index}.`} </ScenarioItemIndex>
                <ScenarioItemName> {name} </ScenarioItemName>
            </ScenarioTextContainer>
            <ScenarioItemCreatedAt> {created_at.toLocaleString()} </ScenarioItemCreatedAt>
        </ScenarioItemContainer>
    )
}

const ScenarioItemContainer = styled.div`
    display: flex;
    width: 700px;
    align-items: center;
    justify-content: space-between;
    padding: 5px 20px;

    font-size: 18px;
    font-weight: 500;

    border: 1px solid rgba(0,0,0,0.5);
    border-radius: 10px;

    cursor: pointer;

    transition: all 0.2s;

    &:hover{
        box-shadow: 0 0  10px 5px rgba(0,0,0,0.1);
        transform: scale(1.05);
    }

`

const ScenarioTextContainer = styled.div`
    display: flex;
`

const ScenarioItemIndex = styled.div`
    padding: 5px;
`

const ScenarioItemName = styled.div`
    padding: 5px 10px 5px 5px;
`

const ScenarioItemCreatedAt = styled.div`
    color: rgba(0,0,0,0.3);
`