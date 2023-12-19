import { IReportItem } from "@services/types/processes";
import { FC } from "react";
import styled from "styled-components";


interface IApplicationView{
    application: IReportItem
}
export const ApplicationView: FC<IApplicationView> = ({application}) => {
    if(!application || !application.info.length){
        return(<></>)
    }
    return (
        <ApplicationViewContainer>
            <ApplicationViewHeader> Блок: Приложений </ApplicationViewHeader>
            <ApplicationViewBody>
                <FindedHosts application={application} />
                <OpenPorts application={application}/>
                {/* {JSON.stringify(application)} */}
            </ApplicationViewBody>
        </ApplicationViewContainer>
    )
}


const FindedHosts: FC<Omit<IApplicationView, "web">> = ({application}) => {
    return( 
        <SubContainer>
            <SubContainerHeader> Обнаруженные устройства </SubContainerHeader>
            <Table>
                <thead>
                    <Th> # </Th>
                    <Th> IPv4-адрес </Th>
                    <Th> MAC-адрес </Th>
                    <Th> Семейство ОС </Th>
                    <Th> Статус хоста </Th>
                </thead>
                <tbody>
                    { application && application.info.length ?
                        application.info.map( (item,index) => {
                            return (
                                <tr key={`${item?.host}`}>
                                    <Td> {index+1} </Td>
                                    <Td> {item?.host} </Td>
                                    <Td> {item?.mac} </Td>
                                    <Td> {item?.os} </Td>
                                    <ColoredTd 
                                        $active={["up", "filtered"].includes(item?.status)}
                                    > { ["up", "filtered"].includes(item?.status) ? "Активен" : "Неактивен" } </ColoredTd>
                                </tr>
                            )
                        } )
                        :
                        null
                    }
                </tbody>
            </Table>
        </SubContainer>
    )
}


const OpenPorts: FC<Omit<IApplicationView, "web">> = ({application}) => {
    if(
        !application || !application.info.length ||
        "error" in application.info[0]
    ){
        return(<></>)
    }


    return(
        <SubContainer>
            <SubContainerHeader> Открытые порты </SubContainerHeader>
            <Table>
                <thead>
                    <Th> IPv4-адрес </Th>
                    <Th> MAC-адрес </Th>
                    <Th> Порт </Th>
                    <Th> Протокол </Th>
                    <Th> Сервис </Th>
                    <Th> Версия </Th>
                </thead>
                <tbody>
                    {
                        application && application.info.length ? 
                        application.info.map(item => <OpenPortRows ports={item.ports} />)
                        :null
                    }
                </tbody>
            </Table>
        </SubContainer>
    )
}

const OpenPortRows: FC<{ports: any[]}> = ({ports}) => {
    return(
        <>
            {
                ports.length ? 
                ports.map(p => {
                    return (
                        <tr key={`${p?.host}-${p?.port}`}>
                            <Td> {p?.host} </Td>
                            <Td> {p?.mac} </Td>
                            <Td> {p?.port} </Td>
                            <Td> {p?.protocol.toUpperCase()} </Td>
                            <Td> {p?.service?.name} </Td>
                            <Td> {p?.service?.version} </Td>
                        </tr>
                    )
                })
                :null
            }
        </>
    )
}



const ApplicationViewContainer = styled.div`
    display: flex;
    width: 100%;
    flex-direction: column;
    overflow: auto;
`

const ApplicationViewHeader = styled.div`
    display: flex;
    font-size: 24px;
    font-weight: bold;
    padding: 20px;
`

const ApplicationViewBody = styled.div`
    padding: 20px;
`

const Table = styled.table`
    border-collapse: collapse;
    margin-top: 30px;
`

const Th = styled.th`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
`

const ColoredTd = styled.td<{$active: boolean}>`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
    color: #fff;
    background-color: ${ props => props.$active ? "rgba(22, 145, 22, 0.6)" : "rgba(222, 39, 39, 0.6)"};
`

const Td = styled.td`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
`

const SubContainer = styled.div`
    display: flex;
    flex-direction: column;
    padding: 5px 10px;
`

const SubContainerHeader = styled.div`
    font-size: 20px;
    padding: 5px 10px;
    border-bottom: 1px solid rgba(0,0,0,0.5);
`