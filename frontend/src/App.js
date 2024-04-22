import { useState } from 'react';
import './App.css';
import { SearchBar } from './Components/SearchBar';
import { Card } from './Components/Card';

function App() {
	const [Results, setResults] = useState([]);
	const [input, setInput] = useState("");
  	return (
		<div className='App'>
			<div className="search-bar-container">
				<SearchBar setResults={setResults} setInput={setInput} input={input}/>
			</div>
			<div className='cards-container'>
				<Card />
				<Card />
				<Card />
				<Card />
				<Card />
			</div>
		</div>
  	);
}

export default App;
