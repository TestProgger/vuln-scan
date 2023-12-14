import { IMessageListObject } from "@services/types/error";
import { REPLACE_ITEMS } from "./consts";


export function formatMessage(message_list: IMessageListObject){
    const result = []
    if(typeof message_list === 'object' && message_list !== null){
        return Object.values(message_list)
    }
    for( const [key, value] of Object.entries(message_list)){
        result.push(`${REPLACE_ITEMS[key]}: ${value[0]}`)
    }
    return result
}