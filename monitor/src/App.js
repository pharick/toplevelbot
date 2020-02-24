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
    background: black url(${bg}) no-repeat;
    background-size: cover;
    padding: 2em;
    color: white;
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
