import { IMessageListObject } from "@services/types/error";
import { REPLACE_ITEMS } from "./consts";


export function formatMessage(message_list: IMessageListObject){
    const result = []
    for( const [key, value] of Object.entries(message_list)){
        result.push(`${REPLACE_ITEMS[key]}: ${value[0]}`)
    }
    return result
}