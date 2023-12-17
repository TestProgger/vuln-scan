import { ScenariosService } from "@services/scenarios";
import { FC, useEffect, useState } from "react";
import Editor from "react-simple-code-editor";
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism.css';
import styled from "styled-components";
import { SuccessButton } from "@pages/Scenarios/components/Button";
import { IReadScenarioResponse } from "@services/types/scenarios";


interface IScenarioEditor{
    scenarioService: ScenariosService
    initialCode: string
    scenarioId: string
}
const ScenarioEditor: FC<IScenarioEditor> = ({scenarioService, initialCode, scenarioId}) => {
    const [code, setCode] = useState<string>(initialCode);
    const [scenarioInfo, setScenarioInfo] = useState<IReadScenarioResponse>();
    const [isUploaded, setIsUploaded] = useState<boolean>(false)
    
    const loadScenario = async () => {
        const response = await scenarioService.read(scenarioId)
        if(response.success){
            setScenarioInfo(response.body)
            setCode(response.body.text)
        }
    }

    const updateScenario = async () => {
        const response = await scenarioService.update(
            scenarioId,
            btoa(code.replace(/\t/gmi, '  '))
        )
        if(response.success){
            setIsUploaded(true)
            setTimeout(() => {setIsUploaded(false)}, 1000)
        }
    }

    useEffect(() => {
        loadScenario().catch()
    }, [])

    return (
        <EditorContainer>
            <Editor
                value={code}
                onValueChange={code => setCode(code)}
                highlight={code => highlight(code, languages.js)}
                padding={10}
                style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    fontSize: 16,
                    width: "800px",
                    height: "700px",
                    border: "1px solid rgba(0,0,0,0.5)",
                    borderRadius: "10px"
                }}
            />
            <EditorFooter $isUploaded={isUploaded}>
                {isUploaded ?
                    <SuccessUploadContainer>
                        <SuccessUploadText> Сценарий успешно обновлен </SuccessUploadText>
                    </SuccessUploadContainer>
                    :
                    null
                }   
                <SuccessButton onClick={updateScenario}> Сохранить </SuccessButton>
            </EditorFooter>
        </EditorContainer>
        
    )
}

const SuccessUploadContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
`

const SuccessUploadText = styled.div`
    font-size: 24px;
    font-weight: 20px;
    padding: 5px 10px;
    background-color: rgba(22, 145, 22, 0.6);
    border-radius: 10px;
    color: #fff;
`

const EditorContainer = styled.div`
    display: flex;
    flex-direction: column;
`

const EditorFooter = styled.div<{ $isUploaded: boolean}>`
    margin-top: 20px;
    display: flex;
    justify-content: ${props => props.$isUploaded ? 'space-between' : 'flex-end'};
`

export { ScenarioEditor }