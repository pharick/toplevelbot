import React, {Component} from 'react';
import {createGlobalStyle} from 'styled-components';

import ParticipantsTable from './components/ParticipantsTable';

import bg from './bg.jpg';

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    font-family: "Open Sans", sans-serif;
    background-color: black;
    padding: 1em;
    color: white;
    
    @media(min-width: 1200px) {
      background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${bg});
      background-size: cover;
      background-attachment: fixed;
      background-position: center;
     }
  }
`;

class App extends Component {
  state = {
    participants: []
  };

  async get_participants() {
    const participants_response = await fetch('http://localhost/api/participants/');
    return await participants_response.json();
  }

  async componentDidMount() {
    const participants = await this.get_participants();
    this.setState({ participants });
    // this.timer = setInterval(() => this.get_participants(), 10000);
  }

  render() {
    return (
      <div className="App">
        <GlobalStyle/>
        <ParticipantsTable participants={this.state.participants}/>
      </div>
    );
  }
}

export default App;
