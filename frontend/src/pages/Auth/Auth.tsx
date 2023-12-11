import { observer } from "mobx-react-lite";
import { FC, useState } from "react";
import styled from "styled-components";
import UserService from "@services/user";
import './Auth.scss';
import { usePersistentStore } from "@store";
import { useNavigate } from "react-router-dom";



const AuthPage: FC = () => {

    const {token} = usePersistentStore()
    const userService = new UserService(token.access, token.refresh)
    const navigate = useNavigate()
    const [username, setUsername] = useState<string>('');
    const [password, setPasssword] = useState<string>('');

    const handleAuth = async () => {
        const response = await userService.login(username, password)
        console.log(response)
        if(response.success){
            token.setToken(response.body)
            navigate('/')
        }
    }


    return (
        <div className="auth-page">
            <AuthFormContainer>
                <AuthFormHeader> Авторизация </AuthFormHeader>
                <AuthInputContainer>
                    <AuthInputLabel> Имя пользователя </AuthInputLabel>
                    <AuthInput type="text" value={username} onChange={e => setUsername(e.target.value)}/>
                </AuthInputContainer>
                <AuthInputContainer>
                    <AuthInputLabel> Пароль </AuthInputLabel>
                    <AuthInput type="password" value={password} onChange={e => setPasssword(e.target.value)}/>
                </AuthInputContainer>
                <AuthButton onClick={handleAuth}> Войти </AuthButton>
            </AuthFormContainer>
        </div>
    )
}

const AuthFormContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border: 1px solid #5e5e5e;
    border-radius: 10px;
    box-shadow: 0 0 10px 5px rgba(0,0,0,0.1);
`

const AuthFormHeader = styled.div`
    width: 100%;
    text-align: center;
    font-size: 24px;
    font-weight: 500;
    margin-bottom: 20px;
    border-bottom: 1px solid #5e5e5e;
`

const AuthInputContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 5px;
    margin-top: 5px;
`

const AuthInput = styled.input`
    background: none;
    font-size: 20px;
    font-weight: 400;
    border: 1px solid #5e5e5e;
    border-radius: 10px;
    padding: 10px;
`

const AuthInputLabel = styled.span`
    font-size: 14px;
    font-weight: 400;
`

const AuthButton = styled.button`
    background: none;
    font-size: 20px;
    font-weight: 500;
    border: 1px solid #5e5e5e;
    padding: 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    margin-top: 10px;

    transition: all 0.2s;

    &:hover{
        box-shadow: 0 0 10px 5px rgba(0,0,0,0.1);
        transform: scale(1.1);
    }

`


export default observer(AuthPage)