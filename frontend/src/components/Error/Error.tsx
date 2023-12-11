import { observer } from "mobx-react-lite";
import { FC, useEffect } from "react";
import './Error.scss';
import { usePersistentStore } from "@store";



const Error: FC = () => {
    const { error } = usePersistentStore()

    useEffect(() => {
        if(error.is_visible){
            setTimeout(() => {
                error.setIsVisible(false)
            }, error.timeout)
        }
    }, [error.is_visible])

    return (
        <div className={ !error.is_visible ? "block-error" : "block-error visible"}>
            <div className="block-error-content">
                {error.message ? <div> {error.message} </div> : null}
                {error.message_list ? error.message_list.map(m => <div>{m}</div>): null}
            </div>
        </div>
    )
}


export default observer(Error)