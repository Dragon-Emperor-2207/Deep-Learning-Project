import React, {useState, useEffect} from 'react'
import { useLocation } from 'react-router-dom';
import { trio } from 'ldrs'

trio.register()

const Summary = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const location = useLocation();
  const searchParams = new URLSearchParams(location.search);

  const imageUrl = searchParams.get('image');
  const id = searchParams.get('id');

  useEffect(() => {
    const fetchData = (id) => {
        console.log("Hi");
      fetch(`http://127.0.0.1:8000/search/summary/?data=${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
      })
      .then((response) => response.json())
      .then((json) => {
        setLoading(false);
        setData(json);
      })
      .catch((error) => {
          console.error('Error:', error);
      });
    };
    fetchData(id);

  }, []);
    
  if (loading) {
    return (
        <div className='LoadingScreen'>
            <l-trio
                size="60"
                speed="1.3" 
                color="rgb(0, 0, 0)" 
            ></l-trio>
        </div>

    )
    }
    else {
        return (
            <div className='summary-page'>
                <img src={imageUrl} alt='Poster of Movie' className='summary-image'></img>
                <div className='summaries'>
                    <div className='summary-good-block'>
                        <h3>{data.summaries.title_good}</h3>
                        <text className='summary-good'>{data.summaries.good_summary}</text>
                    </div>
                    <div className='summary-bad-block'>
                        <h3>{data.summaries.title_bad}</h3>
                        <text className='summary-bad'>{data.summaries.bad_summary}</text>
                    </div>
                </div>
                <div className='summary-adj'>
                    {/* <text>3 Most Frequent Words</text>
                    <div className="ol-container">
                        <ol>weefdfbg</ol>
                        <ol>2. JNONKINJ</ol>
                        <ol>3. hi</ol>
                    </div> */}
                </div>
            </div>
        )
    }
    }

export default Summary