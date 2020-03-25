import React, {Component} from 'react';
import styled from 'styled-components';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Toggle from "./Toggle";
import ParticipantPhotos from "./ParticipantPhotos";
import categories from "../categories";

const Container = styled.div`
  margin: 0 auto;

  @media(max-width: 1200px) {
    max-width: 540px;
  }
`;

const Caption = styled.h1`
  font-family: 'Rubik Mono One', sans-serif;
  font-size: 1.5em;
  margin: 0;
  text-align: center;
`;

const ParticipantList = styled.ol`
  list-style: none;
  padding: 0;
  
  li:not(:last-child) {
    border-bottom: 1px solid rgba(100, 100, 100, 0.4);
  }
`;

const ParticipantArticle = styled.article`
  display: flex;
  font-size: 1.5em;
  margin: 0.2em 0;
  
  @media(max-width: 1200px) {
    flex-direction: column;
    padding: 0.5em 0;
  }
`;

const ParticipantInfo = styled.div`
  display: flex;
  align-items: center;
  width: 500px;
  flex: none;
  margin: 0;
  font-family: 'Rubik Mono One', sans-serif;
  font-size: 1.2em;  
  
  @media(max-width: 1200px) {
    margin-top: 0.2em;
    width: auto;
  }
`;

const ParticipantNumber = styled.p`
  width: 50px;
  text-align: right;
  margin: 0 0.5em 0 0;
  flex: none;
  
  @media(max-width: 1200px) {
    width: auto;
  }
`;

const ParticipantPhoto = styled.img`
  display: block;
  margin-right: 0.8em;
  width: 80px;
  flex: none;
  border-radius: 100%;
  
  @media(max-width: 1200px) {
    margin-right: 0.5em;
  }
`;

const ParticipantName = styled.h2`
  font-size: 1em;
  line-height: 1em;
  font-weight: bold;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const MarksWrapper = styled.div`
  flex: 1;
  display: flex;
  
  @media(max-width: 1200px) {
    flex-direction: column;
  }
`;

const Mark = styled.div`
  text-align: center;
  font-weight: ${props => props.total ? "bold" : "normal"};
  flex: 1;
  
  &:not(:last-child) {
    margin-right: 0.2em;
  }
  
  @media(max-width: 1200px) {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
    justify-content: center;
  }
`;

const MarkValue = styled.p`
  font-family: 'Rubik Mono One', sans-serif;
  font-size: 1.5em;
  margin: 0;
  
  @media(max-width: 1200px) {
    flex: 1;
    text-align: left;
    font-size: 1em;
   }
`;

const MarkLabel = styled.p`
  margin: 0;
  font-size: 0.7em;
  color: darkgray;
  
  @media(max-width: 1200px) {
    flex: 2;
    text-align: right;
    margin-right: 1em;
  }
`;

const MobileContent = styled.section`
  display: none;
  
  @media(max-width: 1200px) {
    display: block;
  }
`;

const Participants = ({ participants, category }) => (
  <ParticipantList>
    {participants.map((participant, i) => (
      <li key={participant.id}>
        <Participant i={i + 1} participant={participant} category={category}/>
      </li>
    ))}
  </ParticipantList>
);

const Participant = ({ i, participant, category }) => (
  <ParticipantArticle>
    <ParticipantInfo>
      <ParticipantNumber>{i}</ParticipantNumber>

      <ParticipantPhoto src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
      <ParticipantName>{participant.first_name} {participant.last_name}</ParticipantName>
    </ParticipantInfo>

    <Marks category={categories[category]} marks={participant.marks[category]}/>

    <MobileContent>
      <Toggle title="Фотографии">
        <ParticipantPhotos participant={participant} category={category}/>
      </Toggle>
    </MobileContent>
  </ParticipantArticle>
);

const Marks = ({ category, marks }) => (
  <MarksWrapper>
    {Object.keys(marks).map((judge, i) => (
      <Mark key={i}>
        <MarkValue>{marks[judge].reduce((sum, n) => sum + n, 0)}</MarkValue>
        <MarkLabel>{judge}</MarkLabel>
      </Mark>
    ))}

    <Mark total>
      <MarkValue>
        {Object.values(marks).map(judge => judge.reduce((sum, n) => sum + n, 0)).reduce((sum, n) => sum + n, 0)}
      </MarkValue>
      <MarkLabel>Итого</MarkLabel>
    </Mark>
  </MarksWrapper>
);

class ParticipantsTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      participants: []
    };
  }

  // compare_participants = (a, b) => {
  //   const { category } = this.props;
  //
  //   if (category) {
  //     if (a.total_categories[category] > b.total_categories[category]) return -1;
  //     if (a.total_categories[category] === b.total_categories[category]) return 0;
  //     if (a.total_categories[category] < b.total_categories[category]) return 1;
  //   }
  //
  //   if (a.total > b.total) return -1;
  //   if (a.total === b.total) return 0;
  //   if (a.total < b.total) return 1;
  // };

  render() {
    return (
      <Container>
        <Router>
          <Switch>
            <Route path="/lips">
              <Caption>{categories[1].title}</Caption>
              <Participants participants={this.props.participants} category={1}/>
            </Route>x
          </Switch>
        </Router>
      </Container>
    );
  }
}

export default ParticipantsTable;