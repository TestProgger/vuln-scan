import {Instance, types} from 'mobx-state-tree'
import { IUser } from '@/types/store'

export const UserStore = types.model("User", {
    id: types.string,
    first_name: types.string,
    last_name: types.string,
    middle_name: types.maybeNull(types.string)
})
.actions(self => ({

    setUser(data: IUser){
        self.id = data.id
        self.first_name = data.first_name
        self.last_name = data.last_name
        self.middle_name = data.middle_name
    },

    removeUser(){
        self.id = ''
        self.first_name = ''
        self.last_name = ''
        self.middle_name = ''
    }

}))


export type IUserStore = Instance<typeof UserStore>