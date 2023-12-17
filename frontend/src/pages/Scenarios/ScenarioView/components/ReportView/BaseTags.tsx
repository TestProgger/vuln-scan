import styled from "styled-components"

export const Table = styled.table`
    border-collapse: collapse;
    margin-top: 30px;
`

export const Th = styled.th`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
`

export const ColoredTd = styled.td<{$active: boolean}>`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
    color: #fff;
    background-color: ${ props => props.$active ? "rgba(22, 145, 22, 0.6)" : "rgba(222, 39, 39, 0.6)"};
`

export const Td = styled.td`
    padding: 5px 10px;
    margin: 0;
    border: 1px solid black;
`

export const SubContainer = styled.div`
    display: flex;
    flex-direction: column;
    padding: 5px 10px;
`

export const SubContainerHeader = styled.div`
    font-size: 20px;
    padding: 5px 10px;
    border-bottom: 1px solid rgba(0,0,0,0.5);
`


export const MainViewContainer = styled.div`
    display: flex;
    width: 100%;
    flex-direction: column;
    overflow: auto;
`

export const MainViewHeader = styled.div`
    display: flex;
    font-size: 22px;

    padding: 20px;
`

export const MainViewBody = styled.div`
    padding: 20px;
`