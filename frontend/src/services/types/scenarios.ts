
export interface IListScenarioItemResponse{
    id: string
    name: string
    created_at: string
}


export interface IUploadScenarioResponse {
    id: string
    name: string
    created_at: string
}

export interface IReadScenarioResponse extends IUploadScenarioResponse{
    text: string
}