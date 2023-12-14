import React, { FC } from "react";
import './Modal.scss';
import styled from "styled-components";
import { CrossIcon } from "@icons";

export interface IModal{
    isActive: boolean
    setIsActive: (val: boolean) => void
    headerText: string
    children?: React.ReactChild
}
export const Modal: FC<IModal> = ({isActive, setIsActive, children, headerText}) => {
    return (
        <div className={isActive ? "modal-window active" : "modal-window"}>
            <div className={ isActive ? "modal-window__content active" : "modal-window__content"}>
                <ModalHeaderContainer>
                    <ModalHeaderLeft></ModalHeaderLeft>
                    <ModalHeaderMiddle>{headerText}</ModalHeaderMiddle>
                    <ModalHeaderRight onClick={() => setIsActive(false)}> 
                        <CrossIcon width="25" height="25" fill="#000"/> 
                    </ModalHeaderRight>
                </ModalHeaderContainer>
                <ModalBodyContainer>
                    { children }
                </ModalBodyContainer>
            </div>
        </div>
    )
}

const ModalBodyContainer = styled.div`
    padding: 5px 0px;
`

const ModalHeaderContainer = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 10px;
    border-bottom: 1px solid rgba(0,0,0,0.4);
`

const ModalHeaderLeft = styled.div``

const ModalHeaderMiddle = styled.div`
    font-size: 24px;
    font-weight: 500;
    text-align: center;
`

const ModalHeaderRight = styled.div`
    width: 25px;
    height: 25px;
    cursor: pointer;
`