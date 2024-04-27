import React from 'react'
import {FaSearch} from 'react-icons/fa'

export const SearchBar = ({setResults, setInput, input}) => {

    const fetchData = (value) => {
      fetch(`http://127.0.0.1:8000/search/?data=${value}`, {
    	method: 'GET',
    	headers: {
        	'Content-Type': 'application/json',
    	}
		})
		.then((response) => response.json())
		.then((json) => {
			setResults(json);
			console.log(json);
		})
		.catch((error) => {
			console.error('Error:', error);
		});

    }
    const handleChange = (value) => {
		if (value != null) {
			setInput(value);
			fetchData(value);
		}
  	};

	const handleKeyPress = (event, value) => {
		if (event.key === "Enter") {
			handleChange(value);
		}
	}

  return (
    <div className='input-wrapper'>
        <FaSearch id='search-icon'/>
        <input className='search-bar' placeholder='Type to Search' value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => handleKeyPress(e, e.target.value)}></input>
    </div>
  )
}
