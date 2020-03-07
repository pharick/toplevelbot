import React from 'react';
import { createGlobalStyle } from 'styled-components';

import ParticipantsTable from './components/ParticipantsTable';
import bg from './bg.jpg';

const GlobalStyle = createGlobalStyle`
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

function App() {
  return (
    <div className="App">
      <GlobalStyle/>
      <ParticipantsTable/>
    </div>
  );
}

export default App;
