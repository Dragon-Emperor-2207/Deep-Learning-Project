import React from 'react'

export const Card = ({key ,imageUrl, id, seriesName}) => {
  console.log("Series Name:", seriesName);
    return (
        <div className="card">
          <img className="image" src={imageUrl} alt = {id}></img>
          <div className="card-content">
            <p>{seriesName}</p>
          </div>
        </div>
      );
}
