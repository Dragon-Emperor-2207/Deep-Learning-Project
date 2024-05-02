import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter
import Main from './Pages/Main';
import Summary from './Pages/Summary';

function App() {
  	return (
		<Router>
			<Routes>
				<Route path='/main' element={<Main />} />
				<Route path='/summary/*' element={<Summary />} />
			</Routes>
		</Router>
  	);
}

export default App;
