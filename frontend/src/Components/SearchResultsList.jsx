import React from 'react'
import { SearchResult } from './SearchResult';

export const SearchResultsList = ({Results, setInput, setResults}) => {
    //console.log(Results);
    if (Results === undefined|| Results.length === 0) {
        return <div></div>
    }
  return (
    <div className='results-list'>
      {Object.entries(Results).map(([key, value]) => (
        <SearchResult keyName={key} value={value} setInput={setInput} setResults={setResults}/>
      ))}
    </div>
  )
}
