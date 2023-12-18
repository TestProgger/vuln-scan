import { FC, useEffect, useState } from "react";
import './ProcessesView.scss'
import { observer } from "mobx-react-lite";
import { usePersistentStore } from "@store";
import { ProcessesService } from "@services/processes";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { IReportViewResponse } from "@services/types/processes";
import { ReportView } from "@pages/Scenarios/ScenarioView/components/ReportView";
import styled from "styled-components";


const ProcessesViewPage:FC = () => {
    const {token} = usePersistentStore()
    const processesSerivice = new ProcessesService(token.access, token.refresh)
    const params = useParams()
    const location = useLocation()
    const navigate = useNavigate()
    const [report, setReport] = useState<IReportViewResponse>(null);

    const loadReport = async() => {
        const response = await processesSerivice.getProcess(params.processId)
        if(response.success){
            setReport(response.body)
            if(!response.body.is_completed){
                setTimeout(() =>  loadReport(), 1500)
            }
        }
    }

    useEffect(() => {
        loadReport().catch(console.log)
    }, [])

    return(
        <div className="processes-view-page">
            <ProcessViewHeader>
                <ScenarioInfoContainer>
                    <NameText> Сценарий: 
                        <ScenarioLinkText 
                            onClick={() => navigate(`/scenarios/${location.state.scenario.id}`)}
                        >{location.state.scenario.name}</ScenarioLinkText> </NameText>
                    <NameText> Код процесса: {report?.process_code} </NameText>
                </ScenarioInfoContainer>
            </ProcessViewHeader>
            <ProcessViewBody>
                {report ?  <ReportView items={report.items} /> : null }
            </ProcessViewBody>
        </div>
    )
}


export default observer(ProcessesViewPage)

const ProcessViewBody = styled.div`
    width: 1000px;
    border: 1px solid black;
    border-radius: 10px;
    padding: 10px;
`

const ProcessViewHeader = styled.div`
    display: flex;
    flex-direction: column;
    margin-top: 10px;
    width: 1000px;
`

const ScenarioInfoContainer = styled.div`
    display: flex;
    flex-direction: column;
    font-size: 20px;
    border: 1px solid black;
    border-radius: 10px;
`

const NameText = styled.div`
    padding: 10px;
    display: flex;
`

const ScenarioLinkText = styled.div`
    cursor: pointer;
    border-bottom: 2px solid rgba(17, 38, 234, 0.5);
    color: rgba(17, 38, 234, 0.5);
    &:hover{
        border-bottom: 2px solid rgba(17, 38, 234, 0.9);
        color: rgba(17, 38, 234, 0.9);
    }
`