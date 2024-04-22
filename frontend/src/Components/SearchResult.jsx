import React from 'react'

export const SearchResult = ({keyName, value, setInput, setResults}) => {
    console.log(value);
    function setInputandClear(keyName) {
        setInput(keyName);
        setResults([]);
    }

    function handleKeyPress(event) {
      if (event.key === "Enter") {
        setInputandClear()
      }
    }
  return (
    <div className='search-result' onkeypress={handleKeyPress}>{keyName}</div>
  )
}
