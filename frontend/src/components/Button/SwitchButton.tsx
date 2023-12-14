import styled from "styled-components";


export const SwitchButton = styled.button`
    padding: 5px 10px;
    border: 1px solid rgba(0,0,0,0.4);
    border-radius: 10px;
    background: none;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 0 10px 5px rgba(0,0,0,0.1);
    
    transition: all 0.1s;
    width: 100%;
    text-align: center;
    user-select: none;

    &:disabled{
        background-color: rgba(0, 0, 0, 0.3);
        color: #fff;
    }

    &:hover{
        transform: scale(1.1);
    }

    &:disabled:hover{
        box-shadow: none;
        transform: none;
    }
`

