import React, {Component} from 'react';
import styled from 'styled-components';

const criteria = {
    0: [
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

    1: [
        'Выбор техники',
        'Гармоничность формы',
        'Симметрия',
        'Заполнение межресничного пространства',
        'Равномерность и четкость прокраса стрелок',
        'Качество прокраса внутреннего уголка глаза',
        'Качество прокраса внешнего уголка глаза',
        'Глубина введения пигмента',
        'Градиент',
        'Травматичность'
    ],

    2: [
        'Выбор техники',
        'Гармоничность формы',
        'Симметрия',
        'Заполнение головки брови',
        'Заполнение верха тела брови',
        'Заполнение нижней части тела брови',
        'Заполнение хвоста брови',
        'Равномерность прокраса брови',
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
  }
`;

const ParticipantInfo = styled.div`
  display: flex;
  align-items: center;
  width: 400px;
  flex: none;
  
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

const ParticipantName = styled.p`
  font-size: 0.8em;
  font-weight: bold;
  margin: 0 1em 0 0;
`;

const ParticipantMarks = styled.div`
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin: 0.2em 0;
  
  @media(max-width: 1700px) {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
  
  @media(max-width: 840px) {
    flex-direction: column;
  }
`;

const ParticipantMark = styled.div`
  text-align: center;
  flex: 1;
  font-weight: ${props => props.total ? "bold" : "normal"};
  min-width: 110px;
  
  @media(max-width: 1700px) {
    flex: none;
    margin: 0.2em;
  }
  
  @media(max-width: 840px) {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
    justify-content: right;
  }
`;

const MarkValue = styled.p`
  font-size: 1.3em;
  margin: 0;
`;

const CriterionLabel = styled.p`
  margin: 0;
  font-size: 0.5em;
  color: darkgray;
  
  @media(max-width: 840px) {
    font-size: 0.6em;
    margin-right: 1em;
  }
`;

const Participant = ({ i, participant, category }) => (
  <ParticipantArticle>
      <ParticipantInfo>
          <ParticipantNumber>{i}</ParticipantNumber>

          <ParticipantPhoto src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
          <ParticipantName>{participant.first_name} {participant.last_name}</ParticipantName>
      </ParticipantInfo>

      <ParticipantMarks>
          {participant.total_marks[category].map((mark, i) => (
            <ParticipantMark key={i}>
                <MarkValue>{mark}</MarkValue>
                <CriterionLabel>{criteria[0][i]}</CriterionLabel>
            </ParticipantMark>
          ))}

          <ParticipantMark total>
              <MarkValue>{participant.total_category[category]}</MarkValue>
              <CriterionLabel>Итого</CriterionLabel>
          </ParticipantMark>
      </ParticipantMarks>
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
        const participants_response = await fetch('http://localhost/api/participants/');
        let participants = await participants_response.json();

        participants = participants.map(participant => {
            participant.total_category = [];
            participant.total_category[0] = participant.total_marks[0].reduce((sum, n) => (sum + n));
            participant.total_category[1] = participant.total_marks[1].reduce((sum, n) => (sum + n));
            participant.total_category[2] = participant.total_marks[2].reduce((sum, n) => (sum + n));
            participant.total = participant.total_category[0] +
                                participant.total_category[1] +
                                participant.total_category[2];
            return participant;
        });


        participants.sort(this.compare_participants);
        this.setState({ participants });
    }

    compare_participants(a, b) {
        if (a.total > b.total) return -1;
        if (a.total === b.total) return 0;
        if (a.total < b.total) return 1;
    }

    componentDidMount() {
        this.get_participants();
        this.timer = setInterval(() => this.get_participants(), 10000)
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