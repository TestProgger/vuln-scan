export interface IProcessMessage{
    id: string
    value: object | string
    created_at: string
}

export interface ILastProcessMessagesResponse{
    list: IProcessMessage[]
    is_completed: boolean
    process_id: string
    process_code: string
}

export interface IRunProcessResponse{
    scenario_id: string
    process_id: string
    process_code: string
}

export interface ITriggerMessageValue{
    type: string
    name: string
    result: object | string 
}

export interface ITriggerMessage{
    id: string
    value: ITriggerMessageValue
    created_at: string
}

export interface IReportItem{
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

export interface IReportViewResponse{
    items: IReportViewItem,
    is_completed: boolean
    process_id: string
    process_code: string
}

export interface IListProcessesItem{
    id: string
    code: string
    started_at: string
    finished_at: string | null
    scenario: {
        id: string
        name: string
    }
    is_completed: boolean
}