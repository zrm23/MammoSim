import { Navigate, Route, Routes } from 'react-router-dom'
import './App.css'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'
import CasesPage from './pages/CasesPage'
import HistorialPage from './pages/HistorialPage'
import GuidePage from './pages/GuidePage'
import SettingPage from './pages/SettingPage'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Navigate to="/login" replace />}/>
      <Route path='/login' element={<LoginPage/>}/>
      <Route path='/register' element={<RegisterPage/>}/>
      <Route path='/cases' element={<CasesPage/>}/>
      <Route path='/historial' element={<HistorialPage/>}/>
      <Route path='/guide' element={<GuidePage/>}/>
      <Route path='/setting' element={<SettingPage/>}/>
    </Routes>
  )
}

export default App
