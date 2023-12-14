import { ScenariosService } from "@services/scenarios";
import { FC, useState } from "react";
import Editor from "react-simple-code-editor";
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism.css';
import styled from "styled-components";
import { SuccessButton } from "@pages/Scenarios/components/Button";


interface IScenarioEditor{
    scenarioService: ScenariosService
    initialCode: string
}
const ScenarioEditor: FC<IScenarioEditor> = ({scenarioService, initialCode}) => {
    const [code, setCode] = useState<string>(initialCode);
    

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
                    height: "700px"
                }}
            />
            <EditorFooter>
                <SuccessButton> Сохранить </SuccessButton>
            </EditorFooter>
        </EditorContainer>
        
    )
}


const EditorContainer = styled.div`
    display: flex;
    flex-direction: column;
`

const EditorFooter = styled.div`
    display: flex;
    justify-content: flex-end;
`