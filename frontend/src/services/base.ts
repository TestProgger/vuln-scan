import axios, { AxiosInstance, AxiosError } from "axios";
import { BaseURL, REFRESH_TOKEN_URL } from "./consts";
import throttle from "lodash/throttle";
type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

export interface IRefreshTokenBody {
    access: string,
    refresh: string
}


export interface IResponse<T> {
    success: boolean
    body: T,
    status: {
        message: string,
        code: number
    }
}

interface ITokenError {
    detail: string,
    code: string,
    messages: any[]
}

enum TokenResponseMessage {
    TOKEN_INVALID_OR_EXPIRED = "Токен недействителен или просрочен",
    GIVEN_TOKEN_INVALID_OR_EXPIRED = "Данный токен недействителен для любого типа токена"
}

class BaseService {
    protected session: AxiosInstance
    public access: string
    public refresh: string
    protected refreshAttemts: number = 0;
    protected throttledRefreshToken: Function;

    constructor(access: string = '', refresh: string = '') {
        this.access = access;
        this.refresh = refresh;
        this.session = axios.create(
            {
                baseURL: BaseURL,
                timeout: 30000,
                headers: !!access ? { "Authorization": `Bearer ${access}` } : {},
                withCredentials: false
            }
        )

        this.throttledRefreshToken = throttle(this.refreshToken, 150).bind(this)
    }

    public updateToken(access: string, refresh: string){
        this.access = access;
        this.refresh = refresh;
        this.session = axios.create(
            {
                baseURL: BaseURL,
                timeout: 30000,
                headers: !!access ? { "Authorization": `Bearer ${access}` } : {},
                withCredentials: false
            }
        )
    }

    protected async post<T>(url: string, data: object = {}, is_retry: boolean = false): Promise<IResponse<T>> {
        return await this.request('POST', url, data, {} ,is_retry) as IResponse<T>
    }

    protected async get<T>(url: string, params: object = {}, is_retry: boolean = false): Promise<IResponse<T>> {
        return await this.request('GET', url, {} ,params, is_retry) as IResponse<T>
    }

    protected async delete<T>(url: string, is_retry: boolean = false): Promise<IResponse<T>> {
        return await this.request('DELETE', url, {}, {}, is_retry) as IResponse<T>
    }

    protected async put<T>(url: string, data = {}, is_retry: boolean = false): Promise<IResponse<T>> {
        return await this.request('PUT', url, data, {}, is_retry) as IResponse<T>
    }

    protected async request<T>(method: RequestMethod, url: string, data: object = {}, params: object = {}, is_retry: boolean =false): Promise<IResponse<T>> {
        try {
            console.log(method, url, data, params)
            const response = await this.session.request({ method, url, data, params })
            console.log("--------------@#@!#")
            return this.formatResponse<T>(response.data)
        }
        catch (e) {
            console.log("====================@#@!#")
            const axiosError = e as AxiosError;
            const setTokenEvent = new CustomEvent('set-token', { detail: { access: this.access, refresh: this.refresh } });
            const LogOutEvent = new Event('logout');
            document.dispatchEvent(setTokenEvent)


            if (axiosError.response?.status === 401) {
                const data = axiosError.response.data as ITokenError;
                if(is_retry){
                    document.dispatchEvent(LogOutEvent);
                    return { body: null, status: { message: "", code: 401 } } as IResponse<T>;
                }
                if (data.detail == TokenResponseMessage.TOKEN_INVALID_OR_EXPIRED) {
                    document.dispatchEvent(LogOutEvent);
                    return { body: null, status: { message: "", code: 401 } } as IResponse<T>;
                }

                if (data.detail == TokenResponseMessage.GIVEN_TOKEN_INVALID_OR_EXPIRED) {
                    await this.throttledRefreshToken();
                    const setTokenEvent = new CustomEvent('set-token', { detail: { access: this.access, refresh: this.refresh } });
                    document.dispatchEvent(setTokenEvent)
                    return await this.request<T>(method, url, data, {}, is_retry=true);
                }
            }
            console.log("@#@!#", axiosError)
            if(axiosError.response?.status === 400){
                const errorEvent = new CustomEvent('error-response', { detail: { message: (axiosError.response?.data as {status: {message: string}})?.status?.message} });
                document.dispatchEvent(errorEvent)
            }

            return { body: null, status: { message: "Ошибка при запросе", code: 404 } } as IResponse<T>
        }
    }

    private async refreshToken() {
        this.session = axios.create(
            {
                baseURL: BaseURL,
                timeout: 3000,
                headers: {},
                withCredentials: false
            }
        )
        const refreshData = await this.post<IRefreshTokenBody>(REFRESH_TOKEN_URL, { refresh: this.refresh })
        this.access = refreshData.body.access;
        this.session = axios.create(
            {
                baseURL: BaseURL,
                timeout: 3000,
                headers: this.access ? { "Authorization": `Bearer ${this.access}` } : {},
                withCredentials: false
            }
        )
    }

    private formatResponse<T>(data: object): IResponse<T> {
        try{
            console.log("1")
            if ("detail" in data) {
                const errorEvent = new CustomEvent('error-response', { detail: { message: data['detail']} });
                document.dispatchEvent(errorEvent)
                return { 
                    success: false,
                    body: null, 
                    status: {
                        message: data['detail'],
                        code: 400
                    }
                } as IResponse<T>
            }
            console.log("2")
            if (!("body" in data)) {
                return { 
                    success: true,
                    body: data, 
                    status: {
                        message: "",
                        code: 0
                    }
                } as IResponse<T>
            }
            console.log("3")
            if ("status" in data){
                console.log("STATUS")
                if("code" in (data["status"] as object) && data["status"]["code"] > 210){
                    console.log("DISPATCH")
                    const errorEvent = new CustomEvent('error-response', { detail: { message: data["status"]["message"]} });
                    document.dispatchEvent(errorEvent)
                    return { ...data, success: false, } as IResponse<T>
                }
                return { ...data, success: true, } as IResponse<T>
            }

            return { ...data, success: true, } as IResponse<T>
        }
        catch(e)
        {
            const errorEvent = new CustomEvent('error-response', { detail: data['detail'] });
            document.dispatchEvent(errorEvent)
        }
    }

}

export default BaseService;
