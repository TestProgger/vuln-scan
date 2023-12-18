import { FC } from "react";
import styled from "styled-components";
import { ApplicationView } from "./ApplicationView";
import { ScannerView } from "./ScannerView";
import { ExploitView } from "./ExploitView";


interface ITriggerMessageValue{
    type: string
    name: string
    result: object | string 
}

interface ITriggerMessage{
    id: string
    value: ITriggerMessageValue
    created_at: string
}

interface IReportItem{
    info: any[]
    exploit: any[]
}

export interface IReportViewItem{
    application: IReportItem
    network: IReportItem
    scanner: IReportItem
    web: IReportItem
    exploit: IReportItem
}

export interface IReportView{
    items: IReportViewItem
}

export const ReportView: FC<IReportView> = ({items}) => {
    console.log(items)
    return (
        <ReportViewContainer>
            <ScannerView scanner={items.scanner} />
            <ApplicationView application={items.application}/>
            <ExploitView exploit={items.exploit} />
        </ReportViewContainer>
    )
}


const ReportViewContainer = styled.div`
    display: flex;
    flex-direction: column;
`