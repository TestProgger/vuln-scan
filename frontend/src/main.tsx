import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.scss'
import { PersistentStoreProvider } from '@store/index.ts'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <PersistentStoreProvider>
        <App />
    </PersistentStoreProvider>
)
