import React, {useState, useEffect} from 'react'
import { useLocation } from 'react-router-dom';

const Summary = () => {
    const [data, setData] = useState(null);
    const location = useLocation();
  const searchParams = new URLSearchParams(location.search);

  const imageUrl = searchParams.get('image');
  const id = searchParams.get('id');

  useEffect(() => {
    const fetchData = (id) => {
      fetch(`http://127.0.0.1:8000/search/summary/?data=${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
      })
      .then((response) => response.json())
      .then((json) => {
          setData(json); // Assuming you want to store the fetched data
      })
      .catch((error) => {
          console.error('Error:', error);
      });
    };

    // Call fetchData only once at the first render
    fetchData(id);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
    
  if (data == null) {
    return (
        <div className='summary-page'>
            <img src={imageUrl} alt='Poster of Movie' className='summary-image'></img>
            <div className='summaries'>
                <text className='summary-good'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eius consequatur maiores autem quod temporibus dignissimos quo libero velit, ipsam quae laboriosam natus quos, facere magni placeat tempora! Suscipit, pariatur aliquid.</text>
                <text className='summary-bad'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Recusandae qui error placeat, sed vel vero, commodi veritatis sit assumenda expedita blanditiis aperiam facere! Itaque error quos vel corrupti eius maiores.</text>
            </div>
            <div className='summary-adj'>
                <text>3 Most Frequent Words</text>
                <div className="ol-container">
                    <ol>1. HBJH KJS</ol>
                    <ol>2. JNONKINJ</ol>
                    <ol>3. hi</ol>
                </div>
            </div>
        </div>
    )
    }
    else {
        return (
            <div className='summary-page'>
                <img src={imageUrl} alt='Poster of Movie' className='summary-image'></img>
                <div className='summaries'>
                    <text className='summary-good'>{data.summaries.good_summary}</text>
                    <text className='summary-bad'>{data.summaries.bad_summary}</text>
                </div>
                <div className='summary-adj'>
                    <text>3 Most Frequent Words</text>
                    <div className="ol-container">
                        <ol>1. HBJH KJS</ol>
                        <ol>2. JNONKINJ</ol>
                        <ol>3. hi</ol>
                    </div>
                </div>
            </div>
        )
    }
    }

export default Summary