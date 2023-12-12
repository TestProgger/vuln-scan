import { observer } from "mobx-react-lite";
import { FC } from "react";
import { AddScenarioButton, ScenarioItem } from "./components";
import './Scenarios.scss'


const ScenariosPage: FC = () => {
    return (
        <div className="scenarios-page">
            <AddScenarioButton onClick={() => console.log("HELLO")} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
            <ScenarioItem index={1} id={'123213'} name="Какойто-сценарий" created_at={new Date()} />
        </div>
    )
}


export default observer(ScenariosPage)