import { FC, useEffect } from "react";
import { Bars } from "react-loader-spinner";
import "./Loading.scss";
import { observer } from "mobx-react-lite";
import { usePersistentStore } from "@store";
import { useLocation, useNavigate } from "react-router-dom";

const LoadingPage: FC<{to:string}> = ({to}) => {

    const rootStore = usePersistentStore()
    const navigate = useNavigate()

    useEffect(() => {
        setTimeout(() => {
            navigate(to)
        }, 1500)
    }, [])

    return(
        <div className="loading-page">
            <Bars
                height="160"
                width="160"
                color="#4fa94d"
                ariaLabel="bars-loading"
                wrapperStyle={{}}
                wrapperClass=""
                visible={true}
            />
        </div>
    )
}

export default observer(LoadingPage)