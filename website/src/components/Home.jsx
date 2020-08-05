import React , {useEffect, useState} from 'react';
import { Button } from 'react-bootstrap';

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
    <div className="App">
      <header className="App-header">

        ... no changes in this part ...

        <p>The current time is {currentTime}.</p>
        <div className="mb-2">
        <Button variant="primary">Primary</Button>{' '}
      </div>
      </header>
    </div>
  );
}

export default Home;