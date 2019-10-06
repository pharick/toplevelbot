import React, {Component} from 'react';
import styled from 'styled-components';

const Participants = styled.ol`
  list-style: none;
  padding: 0;
  
  li {
    border-bottom: 1px solid lightgrey;
    padding: 1em 0;
  }
`;

const ParticipantArticle = styled.article`
  display: flex;
  align-items: center;
  
  .participant_photo {
    margin-right: 2em;
  }
  
  .participant_name {
    width: 400px;
    font-size: 1.7em;
    font-weight: bold;
    margin: 0;
  }
`;

const ParticipantMarks = styled.div`
  flex: 1;
  display: flex;
  justify-content: space-between;
`;

const ParticipantMark = styled.div`
  text-align: center;
  width: 150px;
  
  .mark_value {
    font-size: 2.5em;
    font-weight: ${props => props.total ? "bold" : "normal"};;
    margin: 0 0 0.1em 0;
  }
  
  .mark_label {
    color: gray;
    margin: 0;
  }
`;

const Participant = ({ participant }) => (
    <li>
        <ParticipantArticle>
            <img className="participant_photo" width="100" src={participant.photo} alt={`${participant.first_name} ${participant.last_name}`}/>
            <p className="participant_name">{participant.first_name} {participant.last_name}</p>

            <ParticipantMarks>
                <ParticipantMark>
                    <p className="mark_value">{participant.average_marks.beauty}</p>
                    <p className="mark_label">Красота</p>
                </ParticipantMark>

                <ParticipantMark>
                    <p className="mark_value">{participant.average_marks.color}</p>
                    <p className="mark_label">Цвет</p>
                </ParticipantMark>

                <ParticipantMark>
                    <p className="mark_value">{participant.average_marks.shape}</p>
                    <p className="mark_label">Форма</p>
                </ParticipantMark>

                <ParticipantMark total>
                    <p className="mark_value">
                        {participant.total}
                    </p>
                    <p className="mark_label">Итого</p>
                </ParticipantMark>
            </ParticipantMarks>
        </ParticipantArticle>
    </li>
);

class ParticipantsTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            participants: []
        };
    }

    async get_participants() {
        const participants_response = await fetch('http://157.230.105.46/api/participants/');
        let participants = await participants_response.json();

        participants = participants.map(participant => {
            participant.total = Object.values(participant.average_marks).reduce((sum, n) => (sum + n));
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
        this.timer = setInterval(() => this.get_participants(), 1000)
    }

    render() {
        return (
            <Participants>
                {this.state.participants.map(participant => (
                    <Participant key={participant.id} participant={participant}/>
                ))}
            </Participants>
        );
    }
}

export default ParticipantsTable;