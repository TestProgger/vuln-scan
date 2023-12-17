import styled from "styled-components";

export const ErrorButton = styled.button`
    border: none;
    border-radius: 10px;
    background-color: rgba(222, 39, 39, 0.6);
    color: #fff;
    font-size: 18px;
    font-weight: 400;

    padding: 10px 15px;
    cursor: pointer;

    transition: all 0.2s;

    &:disabled{
        background-color: rgba(0, 0, 0, 0.3);
    }

    &:hover{
        box-shadow: 0 0  10px 5px rgba(222, 39, 39, 0.6);
        transform: scale(1.05);
    }
    &:disabled:hover{
        box-shadow: none;
        transform: none;
    }
`