import { IReportItem } from "@services/types/processes";
import { FC } from "react";
import styled from "styled-components";
import { MainViewBody, MainViewContainer, MainViewHeader, SubContainer, SubContainerHeader, Table, Td, Th } from "./BaseTags";


interface IScannerView{
    scanner: IReportItem
}
export const ScannerView: FC<IScannerView> = ({scanner}) => {
    console.log("scanner", scanner)
    if(!scanner || !scanner.info.length){
        return(<></>)
    }
    return (
        <MainViewContainer>
            <MainViewHeader> Блок: Сканер </MainViewHeader>
            <MainViewBody>
                <FindedDevices scanner={scanner}/>
            </MainViewBody>
        </MainViewContainer>
    )
}


const FindedDevices: FC<IScannerView> = ({scanner}) => {
    console.log("scanner", scanner)
    if(!scanner || !scanner.info.length){
        return(<></>)
    }
    return (
        <ScannerViewSubContainer>
            {/* <SubContainerHeader>  </SubContainerHeader> */}
            {
                scanner && scanner?.info && scanner.info?.length ? 
                scanner.info.map(item => <DeviceInfo host={item}/>)
                :null
            }
        </ScannerViewSubContainer>
    )
} 

const ScannerViewSubContainer = styled.div`
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
`


const DeviceInfo: FC<{host: any}> = ({host}) => {
    console.log(host)
    if(!host){
        return(<></>)
    }

    return(
        <DeviceSubContainer>
            <DeviceHeader> Хост: {host?.host} </DeviceHeader>
            <Table>
                <thead>
                    <Th> # </Th>
                    <Th> Порт </Th>
                    <Th> Протокол </Th>
                    <Th> Сервис </Th>
                </thead>
                <tbody>
                    {
                        host && host?.ports && host?.ports?.length ?
                        host.ports.map( (p, index) => {
                            return (
                                <tr>
                                    <Td> {index+1} </Td>
                                    <Td> {p.port} </Td>
                                    <Td> {p.protocol.toUpperCase()} </Td>
                                    <Td> {p.service_name} </Td>
                                </tr>
                            )
                        } )
                        :null
                    }
                </tbody>
            </Table>
        </DeviceSubContainer>
    )
}

const DeviceSubContainer = styled.div`
    padding: 5px;
    margin-bottom: 10px;
`

const DeviceHeader = styled.div`
    display: flex;
    font-size: 18px;

    margin-top: 10px;
    /* padding: 20px; */
    border-bottom: 1px solid black;
`