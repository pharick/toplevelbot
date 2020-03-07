import React, {Component} from 'react';
import styled from 'styled-components';

import Toggle from "./Toggle";
import ParticipantPhotos from "./ParticipantPhotos";

const categories = ['Акварельные губы', 'Веки с растушевкой', 'Пудровые брови'];

const criteria = {
  1: [
    'Впечатление',
    'Форма',
    'Симметрия',
    'Цвет',
    'Насыщенность',
    'Контур',
    'Равномерность покраса',
    'Оформление уголков',
    'Глубина пигмента',
    'Травматичность'
  ],

  2: [
    'Техника',
    'Форма',
    'Симметрия',
    'Межресничное пространство',
    'Прокрас стрелок',
    'Внутренний уголок глаза',
    'Внешний уголок глаза',
    'Глубина пигмента',
    'Градиент',
    'Травматичность'
  ],

  3: [
    'Техника',
    'Форма',
    'Симметрия',
    'Головка брови',
    'Верх тела брови',
    'Низ тела брови',
    'Хвост брови',
    'Равномерность прокраса',
    'Градиент',
    'Травматичность'
  ]
};

const Participants = styled.ol`
  list-style: none;
  padding: 0;
  
  li:not(:last-child) {
    border-bottom: 1px solid lightgrey;
  }
`;

const ParticipantArticle = styled.article`
  display: flex;
  font-size: 2em;
  
  @media(max-width: 840px) {
    flex-direction: column;
    padding-bottom: 0.5em;
  }
`;

const ParticipantInfo = styled.div`
  display: flex;
  align-items: center;
  max-width: 400px;
  flex: none;
  margin: 0.2em 0;
  
  @media(max-width: 840px) {
    margin-top: 0.2em;
  }
`;

const ParticipantNumber = styled.p`
  width: 50px;
  text-align: right;
  margin: 0 0.5em 0 0;
  flex: none;
`;

const ParticipantPhoto = styled.img`
  display: block;
  margin-right: 1em;
  width: 80px;
  flex: none;
`;

const ParticipantName = styled.h2`
  font-size: 0.8em;
  font-weight: bold;
  margin: 0 1em 0 0;
`;

const ParticipantMarksWrapper = styled.div`
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin: 0.2em 0;
  flex-wrap: wrap;
  
  @media(max-width: 840px) {
    flex-direction: column;
  }
`;

const ParticipantMark = styled.div`
  text-align: center;
  flex: 1;
  font-weight: ${props => props.total ? "bold" : "normal"};
  min-width: 110px;
  
  @media(max-width: 840px) {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
    justify-content: center;
  }
`;

const MarkValue = styled.p`
  font-size: 1.3em;
  margin: 0;
  
  @media(max-width: 840px) {
    flex: 1;
    text-align: left;
   }
`;

const CriterionLabel = styled.p`
  margin: 0;
  font-size: 0.5em;
  color: darkgray;
  
  @media(max-width: 840px) {
    flex: 2;
    text-align: right;
    font-size: 0.6em;
    margin-right: 1em;
  }
`;

const MobileContent = styled.section`
  display: none;
  
  @media(max-width: 840px) {
    display: block;
  }
`;

const ParticipantMarks = ({criteria, marks, total}) => (
  <ParticipantMarksWrapper>
    {marks.map((mark, i) => (
      <ParticipantMark key={i}>
        <MarkValue>{mark}</MarkValue>
        <CriterionLabel>{criteria[i]}</CriterionLabel>
      </ParticipantMark>
    ))}

    <ParticipantMark total>
      <MarkValue>{total}</MarkValue>
      <CriterionLabel>Итого</CriterionLabel>
    </ParticipantMark>
  </ParticipantMarksWrapper>
);

const Participant = ({ i, participant, category }) => (
  <ParticipantArticle>
    <ParticipantInfo>
      <ParticipantNumber>{i}</ParticipantNumber>

      <ParticipantPhoto src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
      <ParticipantName>{participant.first_name} {participant.last_name}</ParticipantName>
    </ParticipantInfo>

    {category ?
      <ParticipantMarks
        criteria={criteria[category]}
        marks={participant.criteria_marks[category]}
        total={participant.total_categories[category]}
      />
      :
      <ParticipantMarks
        criteria={categories}
        marks={[participant.total_categories[1], participant.total_categories[2], participant.total_categories[3]]}
        total={participant.total}
      />
    }

    <MobileContent>
      <Toggle title="Фотографии">
        <ParticipantPhotos participant={participant} category={category}/>
      </Toggle>
    </MobileContent>
  </ParticipantArticle>
);

class ParticipantsTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      participants: []
    };
  }

  async get_participants() {
    const participants_response = await fetch('http://192.168.1.50/api/participants/');
    let participants = await participants_response.json();

    participants.sort(this.compare_participants);
    this.setState({ participants });
  }

  compare_participants = (a, b) => {
    const { category } = this.props;

    if (category) {
      if (a.total_categories[category] > b.total_categories[category]) return -1;
      if (a.total_categories[category] === b.total_categories[category]) return 0;
      if (a.total_categories[category] < b.total_categories[category]) return 1;
    }

    if (a.total > b.total) return -1;
    if (a.total === b.total) return 0;
    if (a.total < b.total) return 1;
  };

  componentDidMount() {
    this.get_participants();
    this.timer = setInterval(() => this.get_participants(), 10000);
  }

  render() {
    return (
      <Participants>
        {this.state.participants.map((participant, i) => (
          <li key={participant.id}>
            <Participant i={i + 1} participant={participant} category={this.props.category} />
          </li>
        ))}
      </Participants>
    );
  }
}

export default ParticipantsTable;