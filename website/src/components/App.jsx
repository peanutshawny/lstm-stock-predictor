import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

export default class AppWrapper extends React.Component {
  render() {
    return (
      <div className='app-container'>
        <Navbar bg="light" variant="light">
        <Navbar.Brand href="#home">
          <img
            alt=""
            src="/logo.svg"
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{' '}
          LSTM Stock Predictor
        </Navbar.Brand>
        <Nav.Link href={'/'}>Home</Nav.Link>
        <Nav.Link href={'/about'}>About</Nav.Link>
        <Nav.Link href={'/about/subroute'}>Subcomponent</Nav.Link>
        </Navbar>
        {this.props.children}
      </div>
    )
  }
}