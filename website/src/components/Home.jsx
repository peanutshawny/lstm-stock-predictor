import React , {useEffect, useState} from 'react';
import { Button } from 'react-bootstrap';
import ApexChart from './Chart.jsx';

function Home() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    console.log(process.env.MOO);
    fetch(process.env.TEST, {
      headers : { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
       }

    })
    .then(res => res.json())
    .then(data => {
      setCurrentTime(data[0].time)
    });
  }, []);

  return (
    <div className="m-4">
      <div className="App">
        <header className="App-header">
          <p>The current time is {currentTime}.</p>
          <div className="mb-2">
          <Button variant="primary" onClick={() => { alert("Button Clicked");}}>Test Button</Button>{' '}
          <div className="mt-5 col-md-12">
            <ApexChart></ApexChart>
          </div>
        </div>
        </header>
      </div>
    </div>
  );
}

export default Home;