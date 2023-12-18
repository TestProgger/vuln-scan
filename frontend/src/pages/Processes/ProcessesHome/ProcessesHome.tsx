import { ProcessesService } from "@services/processes";
import { IListProcessesItem } from "@services/types/processes";
import { usePersistentStore } from "@store";
import { observer } from "mobx-react-lite";
import { FC, useEffect, useState } from "react";
import styled from "styled-components";
import './ProcessesHome.scss'
import { useNavigate } from "react-router-dom";


const ProcessesHome: FC = () => {
    const {token} = usePersistentStore()
    const [processesList, setProcessesList] = useState<IListProcessesItem[]>([])
    const processesService = new ProcessesService(token.access, token.refresh)

    const navigate = useNavigate()

    const listProcesses = async() => {
        const response = await processesService.listProcesses()
        if(response.success){
            setProcessesList(response.body.list)
        }
    }

    useEffect(() => {
        listProcesses().catch()
    }, [])

    return (
        <div className="processes-page">
            <Table>
                <Thead>
                    <tr>
                        <Th>#</Th>
                        <Th> Код процесса </Th>
                        <Th> Наименование сценария </Th>
                        <Th> Дата запуска </Th>
                        <Th> Дата завершения </Th>
                        <Th> Статус </Th>
                    </tr>
                </Thead>
                <Tbody>
                    {
                        processesList &&  processesList.length ?
                        processesList.map( (pr, index) => {
                            return (
                                <Tr 
                                    key={pr.id} 
                                    onClick={() => navigate(`/processes/${pr.id}`, {state: {scenario: pr.scenario}})}
                                >
                                    <Td> {index+1} </Td>
                                    <Td> {pr.code.slice(11,42)} </Td>
                                    <Td> {pr.scenario.name} </Td>
                                    <Td> {pr.started_at} </Td>
                                    <Td> {pr.finished_at} </Td>
                                    <ColoredTd $active={pr.is_completed}> {pr.is_completed ? "Завершен" : "В работе"} </ColoredTd>
                                </Tr>
                            )
                        })
                        :null
                    }
                </Tbody>
            </Table>
        </div>
    )
}

export default observer(ProcessesHome)


const Table = styled.table`
    border-collapse: collapse;
`

const Thead = styled.thead`
    
`

const Th = styled.th`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
    text-align: center;
`

const Tbody = styled.tbody`
    
`

const Td = styled.td`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
    text-align: center;
`

const Tr = styled.tr`
    font-size: 20px;
    cursor: pointer;
    &:hover{
        background-color: rgba(0,0,0,0.1);
    }
`

export const ColoredTd = styled.td<{$active: boolean}>`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
    color: #fff;
    background-color: ${ props => props.$active ? "rgba(22, 145, 22, 0.6)" : "rgba(222, 39, 39, 0.6)"};
`