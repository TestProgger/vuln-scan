import { ErrorButton, SuccessButton } from "@components/Button";
import { ProcessesService } from "@services/processes";
import { ScenariosService } from "@services/scenarios";
import { IProcessMessage, IReportViewResponse } from "@services/types/processes";
import { FC, useEffect, useState } from "react";
import styled from "styled-components";
import { ReportView } from "./ReportView";


export interface IScenarioManagement{
    scenarioId: string
    processesService: ProcessesService
    scenariosService: ScenariosService
}
export const ScenarioManagement: FC<IScenarioManagement> = ({scenarioId, processesService, scenariosService}) => {
    const [lastReport, setLastReport] = useState<IReportViewResponse>();

    const handleStartScenario = async () => {
        const response = await processesService.runProcess(scenarioId)
        if(response.success){
            console.log(response.body)
            setTimeout(() => loadLastProcessesMessages(), 1500)
        }
    }

    const loadLastProcessesMessages = async () => {
        const response = await processesService.listLastProcessMessages(scenarioId)
        if(response.success){
            console.log(response.body)
            if (!response.body.is_completed && response.body.process_code && response.body.process_id){
                setTimeout(() => loadLastProcessesMessages(), 1500)
            }else
            {
                setLastReport(response.body)
            }
        }
    }

    useEffect(() => {
        loadLastProcessesMessages().catch()
    },[])

    return (
        <ManagmentContainer>
            <ButtonContainer>
                <SuccessButton onClick={() => handleStartScenario()}> Запустить </SuccessButton>
                <ErrorButton> Остановить </ErrorButton>
            </ButtonContainer>
            <ReportContainer>
                {lastReport ? <ReportView items={lastReport?.items}/> : null}
            </ReportContainer>
        </ManagmentContainer>
    )
}


const ManagmentContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 800px;
    border: 1px solid rgba(0,0,0,0.4);
    border-radius: 10px;
    padding: 10px;
`

const ButtonContainer = styled.div`
    display: flex;
    justify-content: flex-end;
    gap: 10px;
`

const ReportContainer = styled.div`
    display: flex;
    width: 100%;
    /* height: 100%; */
    min-height: 500px;
`