import { types, cast } from "mobx-state-tree";
import { formatMessage } from "./utils";
import { IMessageListObject } from "@services/types/error";


export const ErrorStore = types.model('Error', {
    message: types.maybeNull(types.string),
    message_list: types.maybeNull(types.array(types.string)),
    status_code: types.optional(types.number, 200),
    is_visible: types.optional(types.boolean, false),
    timeout: types.optional(types.number, 10000)
})
.actions(self => ({
    setMessage(message: string){
        self.message_list = null
        self.message = message
        self.is_visible = true
    },
    setMessageList(message_list: IMessageListObject){
        self.message = null
        self.message_list = cast(formatMessage(message_list))
        self.is_visible = true
    },

    throw(message: string | IMessageListObject){
        console.log(typeof message, message)
        if(typeof message == 'object'){
            // @ts-ignore
            self.setMessageList(message)
        }else{
            // @ts-ignore
            self.setMessage(message)
        }
    },

    setTimeout(timeout: number){
        self.timeout = timeout
    },
    setIsVisible(is_visible: boolean){
        self.is_visible = is_visible
        if(!is_visible){
            self.message = null,
            self.message_list = null
        }
    }
}))