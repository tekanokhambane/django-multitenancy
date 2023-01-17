import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import CreateService from './pages/CreateService';


const App = () => {
  return (
    <div className=''>
      <BrowserRouter>
        <Routes>
          <Route  path="/dashboard/subscriptions/create/" element={<CreateService/>}/>
        </Routes>
      </BrowserRouter>
      
    </div>
  )
}

export default App