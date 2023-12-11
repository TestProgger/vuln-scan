import { LoadingPage, HomePage, AuthPage } from '@pages';
import { Error } from '@components';
import { observer } from 'mobx-react-lite'
import './App.scss'
import { usePersistentStore } from '@store'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

function App() {

  const rootStore = usePersistentStore()

  document.addEventListener('logout', () => {
    rootStore.logout()
  })

  document.addEventListener('set-token', (e: CustomEventInit) => {
    rootStore.token.setToken(e.detail)
  })

  document.addEventListener('error-response', (e: CustomEventInit) => {
    console.log(e.detail)
    if("message" in e.detail && !!e["detail"]["message"]){
      rootStore.error.throw(e.detail?.message)
    }
  })

  if (!!rootStore.token.is_authenticated){
    return (
      <BrowserRouter>
        <Routes>
          <Route path='/loading' element={<LoadingPage to="/home"/>}/>
          <Route path='/home' element={<HomePage/>}/>
          <Route path='*' element={<Navigate to='/loading' />}/>
        </Routes>
        <Error/>
      </BrowserRouter>
    )
  }
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/loading' element={<LoadingPage to="/auth"/>} />
        <Route path='/auth' element={<AuthPage/>}/>
        <Route path='*' element={<Navigate to='/loading'/>}/>
      </Routes>
      <Error/>
    </BrowserRouter>
  )
}

export default observer(App)
