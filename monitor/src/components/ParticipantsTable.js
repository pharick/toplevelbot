import React, {Component} from 'react';
import styled from 'styled-components';

import { BrowserRouter as Router, Switch, Route, NavLink } from "react-router-dom";

import ToggleCaption from "./ToggleCaption";
import ParticipantPhotos from "./ParticipantPhotos";
import CriteriaMarks from "./CriteriaMarks";

import categories from "../categories";

const Container = styled.div`
  margin: 0 auto;

  @media(max-width: 1200px) {
    max-width: 540px;
  }
`;

const CategoriesList = styled.ul`
  list-style: none;
  padding: 0;
  justify-content: center;
  display: flex;
  flex-wrap: wrap;
`;

const CategoryItem = styled.li`
  a {
    display: block;
    font-family: 'Rubik Mono One', sans-serif;
    font-size: 1.5em;
    color: darkgray;
    margin: 0 0.2em;
    padding: 0.2em;
    
    &:hover {
      background-color: rgba(100, 100, 100, 0.4);
    }
  }
`;

const ParticipantList = styled.ol`
  list-style: none;
  padding: 0;
  margin: 0;
  
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
  justify-content: flex-start;
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
  width: 80px;
  flex: none;
  text-align: right;
  margin: 0 0.3em 0 0;
`;

const ParticipantPhoto = styled.img`
  display: block;
  margin-right: 0.5em;
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
  margin: 0 auto;
  
  & > * {
    flex: 1;
  }
  
  @media(max-width: 1200px) {
    flex-direction: column;
    max-width: 400px;
  }
`;

const Mark = styled.div`
  text-align: center;
  font-weight: ${props => props.total ? "bold" : "normal"};
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%;
  margin: 0 0.2em;
  
  @media(max-width: 1200px) {
    align-items: center;
    flex-direction: row-reverse;
    justify-content: center;
    flex: 1;
    margin: 0.2em 0;
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

const Categories = ({ categories }) => (
  <nav>
    <CategoriesList>
      {Object.values(categories).map((category, i) => (
        <CategoryItem key={i}>
          <NavLink to={category.url} activeStyle={{ color: "white" }}>{category.title}</NavLink>
        </CategoryItem>
      ))}

      <CategoryItem>
        <NavLink to="grand-prix" activeStyle={{ color: "white" }}>Гран-при</NavLink>
      </CategoryItem>
    </CategoriesList>
  </nav>
);

class Participants extends Component {
  get_comparator = (category) => {
    return (a, b) => {
      if (a.marks[category].total_category > b.marks[category].total_category) return -1;
      if (a.marks[category].total_category === b.marks[category].total_category) return 0;
      if (a.marks[category].total_category < b.marks[category].total_category) return 1;
    };
  };

  render() {
    return (
      <ParticipantList>
        {this.props.participants.sort(this.get_comparator(this.props.category)).map((participant, i) => (
          <li key={participant.id}>
            <Participant i={i + 1} participant={participant} category={this.props.category}/>
          </li>
        ))}
      </ParticipantList>
    );
  }
}

const Participant = ({ i, participant, category }) => (
  <ParticipantArticle>
    <ParticipantInfo>
      <ParticipantNumber>{i}</ParticipantNumber>

      <ParticipantPhoto src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
      <ParticipantName>{participant.first_name} {participant.last_name}</ParticipantName>
    </ParticipantInfo>

    <Marks category={categories[category]} marks={participant.marks[category]}/>

    <MobileContent>
      <ToggleCaption title="Фотографии">
        <ParticipantPhotos participant={participant} category={category}/>
      </ToggleCaption>
    </MobileContent>
  </ParticipantArticle>
);

const Marks = ({ category, marks }) => (
  <MarksWrapper>
    {Object.keys(marks.judges).map((judge, i) => (
      <ToggleCaption key={i} title={
        <Mark>
          <MarkValue>{marks.judges[judge].total_judge}</MarkValue>
          <MarkLabel>{judge}</MarkLabel>
        </Mark>
      }>
        <CriteriaMarks/>
      </ToggleCaption>
    ))}

    <Mark total>
      <MarkValue>
        {marks.total_category}
      </MarkValue>
      <MarkLabel>Итого</MarkLabel>
    </Mark>
  </MarksWrapper>
);

class ParticipantsTable extends Component {
  render() {
    return (
      <Container>
        <Router>
          <Categories categories={categories}/>

          <Switch>
            {Object.keys(categories).map((id) => (
              <Route key={id} path={`/${categories[id].url}`}>
                <Participants participants={this.props.participants} category={id}/>
              </Route>
            ))}
          </Switch>
        </Router>
      </Container>
    );
  }
}

export default ParticipantsTable;