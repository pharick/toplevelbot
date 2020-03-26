import React from 'react';
import styled from 'styled-components';

const MarkList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0.5em 0;
`;

const MarkItem = styled.li`
  display: flex;
`;

const MarkLabel = styled.p`
  font-weight: bold;
  flex: 2;
  text-align: right;
  margin: 0 0.5em 0 0;
`;

const MarkValue = styled.p`
  flex: 1;
  margin: 0;
`;

const CriteriaMarks = ({ marks, criteria }) => {
  return marks.length ? (
    <MarkList>
      {marks.map((mark, i) => (
        <MarkItem key={i}>
          <MarkLabel>{criteria[i]}:</MarkLabel>
          <MarkValue>{mark}</MarkValue>
        </MarkItem>
      ))}
    </MarkList>
  ) : (
    <p>Судья еще не выставил оценку.</p>
  );
};

export default CriteriaMarks;