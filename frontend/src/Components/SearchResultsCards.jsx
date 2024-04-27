import React from 'react'
import { Card } from './Card';

export const SearchResultsCards = ({ Results, setResults }) => {
  //console.log(Results);
  if (Results === undefined || Results.length === 0) {
    return <div></div>;
  }
  const resultsArray = Object.entries(Results).slice(0, 5); // Convert object to array and limit to 5 items

  return (
    <div className='cards-container'>
  {resultsArray.map(([seriesName, value]) => (
    <Card key = {seriesName} seriesName={seriesName} imageUrl={value.imageUrl} id={value.id} />
  ))}
</div>

  );
};

