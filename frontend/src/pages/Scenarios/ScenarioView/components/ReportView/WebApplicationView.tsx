import { IReportItem } from "@services/types/processes"
import { FC } from "react"
import { MainViewBody, MainViewContainer, MainViewHeader, SubContainer, SubContainerHeader } from "./BaseTags"
import styled from "styled-components"
import ReactJson from "react-json-view"

interface IWebApplicationView{
    web: IReportItem
}
export const WebApplicationView: FC<IWebApplicationView> = ({web}) => {
    if(!web || !web.info || !web.info.length){
        return(
            <></>
        )
    }


    return(
        <MainViewContainer>
            <MainViewHeader> Блок: WEB-приложений </MainViewHeader>
            <MainViewBody>
                {
                    web.info.length ? 
                    web.info.map( item => <WebApplicationViewItem item={item} /> )
                    :
                    null
                }
            </MainViewBody>
        </MainViewContainer>
    )
}


interface IWebApplicationViewItem{
    item: any
}

const WebApplicationViewItem:FC<IWebApplicationViewItem> = ({item}) => {
    return (
        <SubContainer>
            <SubContainerHeader> 
                <ItemViewHeader> {item.name} </ItemViewHeader>  
                <ItemViewHeader> {item.host} </ItemViewHeader>  
             </SubContainerHeader>
             <ItemViewBody>
                <ItemViewHeader> Извлеченный данные </ItemViewHeader>

                <ReactJson 
                    src={item}
                    displayDataTypes={false}
                    displayObjectSize={false}
                    style={{marginTop: "20px"}}
                />
             </ItemViewBody>
        </SubContainer>
    )
}

const ItemViewContainer = styled.div`
    display: flex;
    flex-direction: column;
`

const ItemViewBody = styled.div`
    padding: 20px;
`

const ItemViewHeader = styled.div`
    font-size: 20px;
`
