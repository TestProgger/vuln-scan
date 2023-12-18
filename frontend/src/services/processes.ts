import BaseService from "./base";
import { IListResponse } from "./types/base";
import { ILastProcessMessagesResponse, IListProcessesItem, IReportViewResponse, IRunProcessResponse } from "./types/processes";


export class ProcessesService extends BaseService{
    constructor(aceess: string, refresh: string){
        super(aceess, refresh)
    }

    public async listLastProcessMessages(scenario_id: string){
        return await this.get<IReportViewResponse>('/processes/list-last-process-messages/', {scenario_id})
    }

    public async runProcess(scenario_id: string){
        return await this.post<IRunProcessResponse>('/processes/run-process/', {scenario_id})
    }

    public async listProcesses(page: number = 1, page_size:number = 20){
        return await this.get<IListResponse<IListProcessesItem>>('/processes/list/', {page, page_size})
    }

    public async getProcess(id: string){
        return await this.get<IReportViewResponse>('/processes/get/', {id})
    }
}