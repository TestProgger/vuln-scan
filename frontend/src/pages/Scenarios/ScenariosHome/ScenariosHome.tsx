import { observer } from "mobx-react-lite";
import { FC, useEffect, useState } from "react";
import { AddScenarioButton, AddScenarioModal, ScenarioItem } from "../components";
import './ScenariosHome.scss'
import { ScenariosService } from "@services/scenarios";
import { usePersistentStore } from "@store";
import { IListScenarioItemResponse } from "@services/types/scenarios";
import { Oval } from "react-loader-spinner";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";


const ScenariosPage: FC = () => {
    const [modalIsActive, setModalIsActive] = useState<boolean>(false)
    const {token} = usePersistentStore()
    const [scenariosList, setScenariosList] = useState<IListScenarioItemResponse[]>([])
    const [totalScenariosCount, setTotalScenariosCount] = useState<number>(0)
    const [isScenariosLoading, setIsScenariosLoading] = useState<boolean>(true)
    const navigate = useNavigate()
    const scenariosService = new ScenariosService(token.access, token.refresh)

    const loadScenarios = async() => {
        setIsScenariosLoading(true)
        const response = await scenariosService.list()
        if(response.success){
            setScenariosList(response.body.list)
            setTotalScenariosCount(response.body.total)
        }
        setIsScenariosLoading(false)
    }

    const handleModalActivation = async (val: boolean) => {
        if(!val){
            await loadScenarios()
        }
        setModalIsActive(val)
    }

    useEffect(() =>{
        loadScenarios().catch(console.log)
    }, [])
    return (
        <div className="scenarios-page">
            
            <AddScenarioButton onClick={() => setModalIsActive(true)} />
            {
                scenariosList.length && !isScenariosLoading ? 
                scenariosList.map( 
                    (sc, index) =>  <ScenarioItem 
                                        key={sc.id} 
                                        index={index+1} 
                                        id={sc.id} 
                                        name={sc.name} 
                                        created_at={sc.created_at} 
                                        onClick={() => navigate(`/scenarios/${sc.id}`)}
                                    /> 
                )
                :
                <NotFound> Вы не загрузили ни одного сценария </NotFound>
            }
            {isScenariosLoading ? <Oval width={40} height={40} /> : null}
            <AddScenarioModal 
                scenariosService={scenariosService}
                isActive={modalIsActive} 
                setIsActive={handleModalActivation}
            />
        </div>
    )
}


const NotFound = styled.div`
    font-size: 20px;
    font-weight: 500;
`

export default observer(ScenariosPage)