import React, { Component } from 'react';
import { Table } from 'antd';

const columns = [
    {
        title: 'Участник',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'Красота',
        dataIndex: 'beauty',
        key: 'beauty',
    },
    {
        title: 'Цвет',
        dataIndex: 'color',
        key: 'color',
    },
    {
        title: 'Форма',
        dataIndex: 'shape',
        key: 'shape',
    },
    {
        title: 'Итог',
        dataIndex: 'total',
        key: 'total',
    }
];

class ParticipantsTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            participants: []
        };
    }

    async get_participants() {
        const participants_response = await fetch('http://localhost/api/participants');
        const participants = await participants_response.json();

        return participants;
    }

    compare_participants(a, b) {
        if (a.total > b.total) return -1;
        if (a.total == b.total) return 0;
        if (a.total < b.total) return 1;
    }

    async componentDidMount() {
        const participants = await this.get_participants();

        const participants_rows = participants.map((participant) => ({
            key: participant.id,
            name: `${participant.first_name} ${participant.last_name}`,
            beauty: participant.average_marks.beauty,
            color: participant.average_marks.color,
            shape: participant.average_marks.shape,
            total: participant.average_marks.beauty + participant.average_marks.color + participant.average_marks.shape
        }));

        participants_rows.sort(this.compare_participants);

        this.setState({
            participants: participants_rows,
        });
    }

    render() {
        return (
            <Table dataSource={this.state.participants} columns={columns}/>
        );
    }
}

export default ParticipantsTable;