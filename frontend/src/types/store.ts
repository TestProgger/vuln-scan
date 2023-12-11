export interface IUser{
    id: string
    first_name: string
    last_name: string
    middle_name: string
}

export interface IToken{
    access: string
    refresh: string
}