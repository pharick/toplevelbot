import React, {Component} from 'react';
import {createGlobalStyle} from 'styled-components';

import ParticipantsTable from './components/ParticipantsTable';

import bg from './bg.jpg';
import drunkMediumDesktopFont from './Druk-Medium-Desktop.otf';

const GlobalStyle = createGlobalStyle`
  @font-face {
     font-family: "Drunk Medium Desktop";
     src: url(${drunkMediumDesktopFont}) format("opentype");
  }
  
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
    const participants_response = await fetch('http://toplevel.space/api/participants/');
    const participants = await participants_response.json();
    this.setState({ participants });
  }

  async componentDidMount() {
    await this.get_participants();
    this.timer = setInterval(async () => await this.get_participants(), 60000);
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
