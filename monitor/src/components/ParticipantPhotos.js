import React from "react";
import styled from 'styled-components';

const PhotoFigure = styled.figure`
  margin: 0.5em;

  img {
    width: 100%;
  }
`;

const PhotoCaption = styled.figcaption`
  font-size: 0.6em;
  color: darkgray;
`;

const ParticipantPhotos = ({participant, category}) => (
  <section>
    {participant.photo_lips_before && (!category || category === 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_before} alt="Губы до"/>
      <PhotoCaption>Губы до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_lips_after && (!category || category === 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_after} alt="Губы после"/>
      <PhotoCaption>Губы после</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyelids_before && (!category || category === 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyelids_before} alt="Веки до"/>
      <PhotoCaption>Веки до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyelids_after && (!category || category === 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyelids_after} alt="Веки после"/>
      <PhotoCaption>Веки после</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyebrows_before && (!category || category === 3) &&
    <PhotoFigure>
      <img src={participant.photo_eyebrows_before} alt="Брови до"/>
      <PhotoCaption>Брови до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyebrows_after && (!category || category === 3) &&
    <PhotoFigure>
      <img src={participant.photo_eyebrows_after} alt="Брови после"/>
      <PhotoCaption>Брови после</PhotoCaption>
    </PhotoFigure>
    }
  </section>
);

export default ParticipantPhotos;