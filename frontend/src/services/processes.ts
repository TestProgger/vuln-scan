import BaseService from "./base";
import { ILastProcessMessagesResponse, IReportViewResponse, IRunProcessResponse } from "./types/processes";


export class ProcessesService extends BaseService{
    constructor(aceess: string, refresh: string){
        super(aceess, refresh)
    }

    public async listLastProcessMessages(scenario_id: string){
        return await this.get<IReportViewResponse>('processes/list-last-process-messages/', {scenario_id})
    }

    public async runProcess(scenario_id: string){
        return await this.post<IRunProcessResponse>('processes/run-process/', {scenario_id})
    }
}