import React from 'react';
import { createGlobalStyle } from 'styled-components';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

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

function App() {
  return (
    <div className="App">
      <GlobalStyle/>

      <Router>
        <Switch>
          <Route path="/lips">
            <ParticipantsTable category={1}/>
          </Route>

          <Route path="/eyelids">
            <ParticipantsTable category={2}/>
          </Route>

          <Route path="/eyebrows">
            <ParticipantsTable category={3}/>
          </Route>

          <Route path="/">
            <ParticipantsTable />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
