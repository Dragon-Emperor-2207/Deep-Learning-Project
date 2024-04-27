import { useState } from 'react';
import './App.css';
import { SearchBar } from './Components/SearchBar';
import {SearchResultsCards} from './Components/SearchResultsCards';
import { Card } from './Components/Card';

function App() {
	const [Results, setResults] = useState([]);
	const [input, setInput] = useState("");
  	return (
		<div className='App'>
			<div className="search-bar-container">
				<SearchBar setResults={setResults} setInput={setInput} input={input}/>
			</div>
			<div className='card-area'>
    			<SearchResultsCards Results={Results} setResults={setResults}/>
			</div>
		</div>
  	);
}

export default App;
