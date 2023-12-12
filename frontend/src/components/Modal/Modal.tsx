import React, { FC } from "react";


export interface IModal{
    isActive: boolean
    setIsActive: (val: boolean) => void
    children: React.ReactChild
}
export const Modal: FC<IModal> = ({isActive, setIsActive, children}) => {
    return (
        <div className={isActive ? "modal-window active" : "modal-window"}>
            <div className="modal-window-body">
                { children }
            </div>
        </div>
    )
}