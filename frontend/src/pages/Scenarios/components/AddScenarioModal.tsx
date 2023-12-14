import { IModal, Modal } from "@components/Modal/Modal";
import { ChangeEvent, FC, MutableRefObject, useRef, useState } from "react";
import Editor from "react-simple-code-editor";
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism.css';
import styled from "styled-components";
import { ScenariosService } from "@services/scenarios";

interface IAddScenarioModal extends Omit<IModal, 'children'|'headerText'>{
    scenariosService: ScenariosService
}

enum MenuItem{
    EDITOR = "EDITOR",
    UPLOADER = "UPLOADER"
}

export const AddScenarioModal: FC<IAddScenarioModal> = ({isActive, setIsActive, scenariosService}) => {
    const [code, setCode] = useState<string>('')
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [activeMenu, setActiveMenu] = useState<string>(MenuItem.UPLOADER)
    const [scenarioName, setScenarioName] = useState<string>('')
    const [isButtonBlocked, setIsButtonBlocked] = useState<boolean>(false)

    const onReadFile = async (event) =>{
        console.log(event)
        const response = await scenariosService.upload(
            scenarioName, 
            btoa(event.target.result)
        )
        if(response.success){
            setIsButtonBlocked(false)
            setIsActive(false)
            fileInputRef.current.value = null;
            setCode('')
        }
    } 

    const handleUpload = async () => {
        setIsButtonBlocked(true)
        setTimeout(() => setIsButtonBlocked(false), 800)
        if (fileInputRef.current && fileInputRef.current.files.length){
            const reader = new FileReader()
            reader.addEventListener('load', onReadFile);
            reader.readAsText(fileInputRef.current.files[0]);
            return
        }
        else if(code){
            const response = await scenariosService.upload(
                scenarioName, 
                btoa(code.replace(/\t/gmi, '  '))
            )
            if(response.success){
                setCode('')
                setIsButtonBlocked(false)
                setIsActive(false)
                fileInputRef.current.value = null;
            }   
        }
    }

    return(
        <Modal isActive={isActive} setIsActive={setIsActive} headerText="Добавить сценарий">
            <Container>
                <SwitchMenuCountainer>
                    <SwitchMenuItem 
                        onClick={() => setActiveMenu(MenuItem.EDITOR)}
                        disabled={activeMenu == MenuItem.EDITOR}
                    > 
                        Открыть редактор 
                    </SwitchMenuItem>
                    <SwitchMenuItem 
                        onClick={() => setActiveMenu(MenuItem.UPLOADER)}
                        disabled={activeMenu == MenuItem.UPLOADER}
                    > 
                        Загрузить файл 
                    </SwitchMenuItem>
                </SwitchMenuCountainer>
                <SwitchBodyContainer>
                    <ScenarioNameInput 
                        type="text" 
                        placeholder="Наименование сценария"
                        value={scenarioName}
                        onChange={e => setScenarioName(e.target.value)}
                    />
                    <SwitchBody>
                        { activeMenu == MenuItem.EDITOR ?  <ScenarioEditor value={code} setValue={setCode} /> : null}
                        { activeMenu == MenuItem.UPLOADER ?  <ScenarioUploader inputRef={fileInputRef}/> : null}
                    </SwitchBody>
                    <SwitchFooter>
                        <UploadButton disabled={isButtonBlocked} onClick={handleUpload}> Сохранить </UploadButton>
                    </SwitchFooter>
                </SwitchBodyContainer>
            </Container>
        </Modal>
    )
}

interface IScenarioEditor{
    value: string
    setValue: (val: string) => void
}
const ScenarioEditor: FC<IScenarioEditor> = ({value, setValue}) => {
    return (
        // <EditorContainer>
            <Editor
                value={value}
                onValueChange={code => setValue(code)}
                highlight={code => highlight(code, languages.js)}
                padding={10}
                style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    fontSize: 16,
                    width: "700px",
                    height: "600px"
                }}
            />
        /* </EditorContainer> */
    )
}

interface IScenarioUploader{
    inputRef: MutableRefObject<HTMLInputElement>
}
const ScenarioUploader: FC<IScenarioUploader> = ({inputRef}) => {

    return(
        <>
            <ScenarioUploadInput 
                type="file" 
                ref={inputRef}
            />
        </>
    )
}

const SwitchMenuCountainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
`

const SwitchMenuItem = styled.button`
    padding: 5px 10px;
    border: 1px solid rgba(0,0,0,0.4);
    border-radius: 10px;
    background: none;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 0 10px 5px rgba(0,0,0,0.1);
    
    transition: all 0.1s;
    width: 190px;
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

const Container = styled.div`
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin: 20px 0px;
`

const SwitchBodyContainer = styled.div`
    display: flex;
    justify-content: center;
    /* align-items: center; */
    flex-direction: column;
    overflow-y: scroll;
`

const SwitchBody = styled.div`
    margin-top: 20px;
    border: 1px solid rgba(0,0,0,0.3);
    border-radius: 10px;
    width: 700px;
`


const ScenarioNameInput = styled.input`
    border: 1px solid rgba(0,0,0,0.2);
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 18px;
    font-weight: 400;
`

const ScenarioUploadInput = styled.input`
    border: none;
    padding: 10px 15px;
    font-size: 18px;
    font-weight: 400;
`

const SwitchFooter = styled.div`
    display: flex;
    justify-content: flex-end;
    padding: 10px 0px;
`

const UploadButton = styled.button`
    border: none;
    border-radius: 10px;
    background-color: rgba(22, 145, 22, 0.6);
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
        box-shadow: 0 0  10px 5px rgba(22, 145, 22, 0.6);
        transform: scale(1.05);
    }
    &:disabled:hover{
        box-shadow: none;
        transform: none;
    }
`



// const EditorContainer = styled.div`
//     border: 1px solid rgba(0,0,0,0.3);
//     border-radius: 10px;
//     overflow-x: hidden;
// `