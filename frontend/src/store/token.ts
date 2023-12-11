import { Instance, types } from 'mobx-state-tree'
import { IToken } from '@/types/store'


export const TokenStore = types.model("Token", {
    access: types.string,
    refresh: types.string,
    is_authenticated: types.optional(types.boolean, false)
})
.actions(self => ({
    setToken(data: IToken){
        self.access = data.access,
        self.refresh = data.refresh
        self.is_authenticated = true
    },
    removeToken(){
        self.access = ''
        self.refresh = ''
        self.is_authenticated = false
    }
}))


export type ITokenStore = Instance<typeof TokenStore>