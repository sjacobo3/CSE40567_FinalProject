import Navigation from './Navigation/Navigation.jsx'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

function Components() {
    return (
        <Router>
          <Navigation />
          <Routes>
          </Routes>
        </Router>
      )
}

export default Components