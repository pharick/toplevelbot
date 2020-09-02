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
    font-family: "Drunk Medium Desktop", sans-serif;
    font-size: 2em;
    color: white;
    opacity: 0.2;
    margin: 0 0.2em;
    padding: 0.2em;
    
    &:hover {
      background-color: rgba(100, 100, 100, 0.4);
      opacity: 1;
    }
  }
`;

const ParticipantList = styled.ol`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const ParticipantArticle = styled.article`
  display: flex;
  font-size: 1.5em;
  margin: 0.2em 0;
  
  @media(max-width: 1200px) {
    flex-direction: column;
    margin: 0.5em 0;
  }
`;

const ParticipantInfo = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 500px;
  flex: none;
  margin: 0;
  margin-right: 0.5em;
  font-family: "Drunk Medium Desktop", sans-serif;
  font-size: 2em;  
  
  @media(max-width: 1200px) {
    margin: 0.2em 0 0.2em 0;
    width: auto;
    justify-content: space-between;
    width: 90%;
  }
`;

const ParticipantNumber = styled.p`
  width: 80px;
  flex: none;
  text-align: right;
  margin: 0 0.3em 0 0;
  
  @media(max-width: 1200px) {
    width: auto;
  }
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
  
  @media(max-width: 1200px) {
    font-size: 0.7em;
  }
`;

const MarksWrapper = styled.div`
  flex: 1;
  display: flex;
  align-items: flex-start;
  
  & > * {
    flex: 1;
  }
  
  @media(max-width: 1200px) {
    margin: 0.5em auto;
    flex-direction: column;
    width: 70%;
    align-items: stretch;
  }
`;

const Mark = styled.div`
  text-align: center;
  font-weight: ${props => props.total ? "bold" : "normal"};
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%;
  width: 100%;
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
  font-family: "Drunk Medium Desktop", sans-serif;
  font-size: 2.5em;
  margin: 0;
  
  @media(max-width: 1200px) {
    flex: 1;
    text-align: left;
    font-size: 1.2em;
   }
`;

const MarkLabel = styled.p`
  margin: 0;
  font-size: 1em;
  color: darkgray;
  
  @media(max-width: 1200px) {
    flex: 3;
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

const CaptionMark = styled.p`
  margin: 0;
  margin-left: 0.5em;
`;

const Categories = ({ categories }) => (
  <nav>
    <CategoriesList>
      {Object.values(categories).map((category, i) => (
        <CategoryItem key={i}>
          <NavLink to={`/${category.url}`} activeStyle={{ opacity: 1 }}>{category.title}</NavLink>
        </CategoryItem>
      ))}

      <CategoryItem>
        <NavLink to="/grand-prix" activeStyle={{ opacity: 1 }}>Гран-при</NavLink>
      </CategoryItem>
    </CategoriesList>
  </nav>
);

class Participants extends Component {
  get_comparator = (category) => {
    if (category === 0) {
      return (a, b) => {
        if (a.marks.total > b.marks.total) return -1;
        if (a.marks.total === b.marks.total) return 0;
        if (a.marks.total < b.marks.total) return 1;
      };
    }

    return (a, b) => {
      if (a.marks.categories[category].total_category > b.marks.categories[category].total_category) return -1;
      if (a.marks.categories[category].total_category === b.marks.categories[category].total_category) return 0;
      if (a.marks.categories[category].total_category < b.marks.categories[category].total_category) return 1;
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
      <ToggleCaption key={i} display={true} title={
        <ParticipantInfo>
          <ParticipantNumber>{i}</ParticipantNumber>

          <ParticipantPhoto src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
          <ParticipantName>{participant.first_name} {participant.last_name}</ParticipantName>

          <MobileContent>
            <CaptionMark>
              {category === 0 ?
                participant.marks.total :
                participant.marks.categories[category].total_category
              }
            </CaptionMark>
          </MobileContent>
        </ParticipantInfo>
      }>
        {category === 0 ?
          <TotalMarks categories={categories} marks={participant.marks}/> :
          <Marks category={categories[category]} marks={participant.marks.categories[category]}/>
        }

        <MobileContent>
          <ToggleCaption title="Фотографии">
            <ParticipantPhotos participant={participant} category={category}/>
          </ToggleCaption>
        </MobileContent>
      </ToggleCaption>
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
        <CriteriaMarks
          criteria={category.criteria}
          marks={marks.judges[judge].criteria}
          message={marks.judges[judge].message}
        />
      </ToggleCaption>
    ))}

    <Mark>
      <MarkValue>{marks.doctor}</MarkValue>
      <MarkLabel>Оценка доктора</MarkLabel>
    </Mark>

    <Mark total>
      <MarkValue>
        {marks.total_category}
      </MarkValue>
      <MarkLabel>Итого</MarkLabel>
    </Mark>
  </MarksWrapper>
);

const TotalMarks = ({ categories, marks }) => (
  <MarksWrapper>
    {Object.keys(marks.categories).map((category, i) => (
      <Mark key={i}>
        <MarkValue>{marks.categories[category].total_category}</MarkValue>
        <MarkLabel>{categories[category].title}</MarkLabel>
      </Mark>
    ))}

    <Mark total>
      <MarkValue>
        {marks.total}
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

            <Route key={0} path={`/grand-prix`}>
              <Participants participants={this.props.participants} category={0}/>
            </Route>
          </Switch>
        </Router>
      </Container>
    );
  }
}

export default ParticipantsTable;