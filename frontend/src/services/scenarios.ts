import BaseService from "./base";
import { IListResponse } from "./types/base";
import { IListScenarioItemResponse, IUploadScenarioResponse } from "./types/scenarios";


export class ScenariosService extends BaseService{

    constructor(access: string, refresh: string){
        super(access, refresh)
    }

    public async list(){
        return await this.get<IListResponse<IListScenarioItemResponse>>('/scenarios/list/')
    }

    public async upload(name: string, file: string){
        return await this.post<IUploadScenarioResponse>('/scenarios/upload/', {name, file})
    }
}