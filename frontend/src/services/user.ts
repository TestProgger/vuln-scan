import BaseService from "./base";
import { LoginResponse } from "./types/user";


class UserService extends BaseService{
    
    constructor(access: string, refresh:string){
        super(access, refresh)
    }

    public async login(username: string, password: string){
        return await this.post<LoginResponse>('/user/auth/login/', {username, password})
    } 

}


export default UserService