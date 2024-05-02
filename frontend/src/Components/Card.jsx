import React from 'react'
import { useNavigate } from 'react-router-dom';

export const Card = ({key ,imageUrl, id, seriesName}) => {
  const navigate = useNavigate();

    return (
        <div className="card">
          <img className="image" src={imageUrl} alt = {id} onClick={() => {navigate(`/summary?image=${encodeURIComponent(imageUrl)}&id=${id}`)}}></img>
          <div className="card-content">
            <p>{seriesName}</p>
          </div>
        </div>
      );
}
