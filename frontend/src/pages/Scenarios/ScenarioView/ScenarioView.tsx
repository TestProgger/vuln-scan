import { SwitchButton } from "@components/Button";
import { observer } from "mobx-react-lite";
import { FC, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { ScenarioEditor, ScenarioManagement } from "./components";
import { ScenariosService } from "@services/scenarios";
import { usePersistentStore } from "@store";
import './ScenarioView.scss'
import { IReadScenarioResponse } from "@services/types/scenarios";
import { ProcessesService } from "@services/processes";

enum ScenarioView{
    EDITOR = "EDITOR",
    MANAGEMENT = "MANAGEMENT"
}

const ScenarioViewPage: FC = () => {
    const params = useParams()
    const {token} = usePersistentStore()
    const [scenarioInfo, setScenarioInfo] = useState<IReadScenarioResponse>();
    const [activeView, setActiveView] = useState<string>(ScenarioView.MANAGEMENT)
    const scenarioService = new ScenariosService(token.access, token.refresh)
    const processesService = new ProcessesService(token.access, token.refresh)

    const loadScenario = async () => {
        const response = await scenarioService.read(params.scenarioId)
        if(response.success){
            setScenarioInfo(response.body)
        }
    }

    useEffect(() => {
        loadScenario().catch()
    }, [])

    return (
        <div className="scenario-view-page">
            <Container>
                <ScenarioInfoContainer>
                    <ScenarioName> {`Наименование сценария: ${scenarioInfo?.name}`} </ScenarioName>
                    <ScenarioId> {`ID сценария: ${scenarioInfo?.id}`} </ScenarioId>
                </ScenarioInfoContainer>
                <ViewContainer>
                    <SwitchMenuContainer>
                        <SwitchButton onClick={() => setActiveView(ScenarioView.EDITOR)}> Редактор </SwitchButton>
                        <SwitchButton onClick={() => setActiveView(ScenarioView.MANAGEMENT)}> Управение сценарием </SwitchButton>
                    </SwitchMenuContainer>
                    <MenuContainer>
                        {activeView == ScenarioView.EDITOR ? 
                            <ScenarioEditor 
                                scenarioService={scenarioService} 
                                initialCode=""
                                scenarioId={params?.scenarioId}
                            />
                            :
                            null
                        }
                        {
                            activeView == ScenarioView.MANAGEMENT ?
                                <ScenarioManagement
                                    scenarioId={params.scenarioId}
                                    scenariosService={scenarioService}
                                    processesService={processesService}
                                />
                            :null
                        }
                    </MenuContainer>
                </ViewContainer>
            </Container>
        </div>
    )
}   

const Container = styled.div`
    display: flex;
    justify-content: center;
    flex-direction: column;
    gap: 20px;
    width: 1200px;
    padding: 20px;
`

const SwitchMenuContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
`

const MenuContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
    /* border: 1px solid rgba(0,0,0,0.1);
    border-radius: 10px; */
    padding: 5px;
`

const ScenarioInfoContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 10px 0px;

    /* border: 1px solid rgba(0,0,0,0.4); */
    border-radius: 10px;
    margin-bottom: 20px;
`

const ScenarioName = styled.div`
    display: flex;
    font-size: 18px;
`

const ScenarioId = styled.div`
    display: flex;
    font-size: 18px;
`

const ViewContainer = styled.div`
    display: flex;
    justify-content: center;
    gap: 20px;
    width: 1200px;
    padding: 20px;
`

export default observer(ScenarioViewPage)