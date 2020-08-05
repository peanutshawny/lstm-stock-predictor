import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

export default class AppWrapper extends React.Component {
  render() {
    return (
      <div className='app-container'>
        <Navbar bg="dark" variant="dark">
          <Nav.Link href={'/'}>Home</Nav.Link>
          <Nav.Link href={'/about'}>About</Nav.Link>
          <Nav.Link href={'/about/subroute'}>Subcomponent</Nav.Link>
        </Navbar>
        {this.props.children}
      </div>
    )
  }
}