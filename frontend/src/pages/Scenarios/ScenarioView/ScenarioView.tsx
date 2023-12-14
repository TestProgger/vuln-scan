import { SwitchButton } from "@components/Button";
import { observer } from "mobx-react-lite";
import { FC } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";

const ScenarioViewPage: FC = () => {
    const params = useParams()

    return (
        <Container>
            <SwitchMenuContainer>
                <SwitchButton> Редактор </SwitchButton>
                <SwitchButton> Управение сценарием </SwitchButton>
            </SwitchMenuContainer>

        </Container>
    )
}   

const Container = styled.div`
    display: flex;
    gap: 20px;
    width: 1200px;
    padding: 20px;
`

const SwitchMenuContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
`

const SwitchMenuItem = styled.div`
    padding: 10px 20px;
    font-size: 20px;

`

const MenuContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
`


export default observer(ScenarioViewPage)