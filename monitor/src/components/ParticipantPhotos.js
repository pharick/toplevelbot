import React from "react";
import styled from 'styled-components';

const PhotoFigure = styled.figure`
  margin: 0.5em;
  border: 1px solid rgba(100, 100, 100, 0.4);
  padding: 0.5em;

  img {
    width: 100%;
    margin-bottom: 0.5em;
  }
`;

const PhotoCaption = styled.figcaption`
  font-size: 0.8em;
  color: darkgray;
  text-align: center;
`;

const ParticipantPhotos = ({participant, category}) => (
  <section>
    {participant.photo_lips_face_before && (!category || category == 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_face_before} alt="Лицо с губами до"/>
      <PhotoCaption>Лицо с губами до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_lips_before && (!category || category == 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_before} alt="Губы до"/>
      <PhotoCaption>Губы до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_lips_face_after && (!category || category == 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_face_after} alt="Лицо с губами после"/>
      <PhotoCaption>Лицо с губами после</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_lips_after && (!category || category == 1) &&
    <PhotoFigure>
      <img src={participant.photo_lips_after} alt="Губы после"/>
      <PhotoCaption>Губы после</PhotoCaption>
    </PhotoFigure>
    }


    {participant.photo_eyeline_face_before && (!category || category == 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyeline_face_before} alt="Лицо с веками до"/>
      <PhotoCaption>Лицо с веками до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyeline_before && (!category || category == 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyeline_before} alt="Веки до"/>
      <PhotoCaption>Веки до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyeline_face_after && (!category || category == 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyeline_face_after} alt="Лицо с веками после"/>
      <PhotoCaption>Лицо с веками после</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_eyeline_after && (!category || category == 2) &&
    <PhotoFigure>
      <img src={participant.photo_eyeline_after} alt="Веки после"/>
      <PhotoCaption>Веки после</PhotoCaption>
    </PhotoFigure>
    }


    {participant.photo_brows_face_before && (!category || category == 3) &&
    <PhotoFigure>
      <img src={participant.photo_brows_face_before} alt="Лицо с бровями до"/>
      <PhotoCaption>Лицо с бровями до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_brows_before && (!category || category == 3) &&
    <PhotoFigure>
      <img src={participant.photo_brows_before} alt="Брови до"/>
      <PhotoCaption>Брови до</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_brows_face_after && (!category || category == 3) &&
    <PhotoFigure>
      <img src={participant.photo_brows_face_after} alt="Лицо с бровями после"/>
      <PhotoCaption>Лицо с бровями после</PhotoCaption>
    </PhotoFigure>
    }

    {participant.photo_brows_after && (!category || category == 3) &&
    <PhotoFigure>
      <img src={participant.photo_brows_after} alt="Брови после"/>
      <PhotoCaption>Брови после</PhotoCaption>
    </PhotoFigure>
    }
  </section>
);

export default ParticipantPhotos;