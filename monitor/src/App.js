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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
                 "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue",
                 sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: black;
    padding: 1em;
    color: white;
    
    @media(min-width: 840px) {
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
