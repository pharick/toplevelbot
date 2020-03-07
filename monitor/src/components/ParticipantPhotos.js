import React from "react";
import styled from 'styled-components';

import Toggle from "./Toggle";

const ParticipantPhotosWrapper = styled.section`
  display: none;
  
  @media(max-width: 840px) {
    display: block;
  }
`;

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

const ParticipantPhotos = ({participant}) => (
  <ParticipantPhotosWrapper>
    <Toggle title="Фотографии">
      {participant.photo_lips_before &&
        <PhotoFigure>
          <img src={participant.photo_lips_before}/>
          <PhotoCaption>Губы до</PhotoCaption>
        </PhotoFigure>
      }

      {participant.photo_lips_after &&
        <PhotoFigure>
          <img src={participant.photo_lips_after}/>
          <PhotoCaption>Губы после</PhotoCaption>
        </PhotoFigure>
      }

      {participant.photo_eyelids_before &&
        <PhotoFigure>
          <img src={participant.photo_eyelids_before}/>
          <PhotoCaption>Веки до</PhotoCaption>
        </PhotoFigure>
      }

      {participant.photo_eyelids_after &&
        <PhotoFigure>
          <img src={participant.photo_eyelids_after}/>
          <PhotoCaption>Веки после</PhotoCaption>
        </PhotoFigure>
      }

      {participant.photo_eyebrows_before &&
        <PhotoFigure>
          <img src={participant.photo_eyebrows_before}/>
          <PhotoCaption>Брови до</PhotoCaption>
        </PhotoFigure>
      }

      {participant.photo_eyebrows_atfer &&
        <PhotoFigure>
          <img src={participant.photo_eyebrows_atfer}/>
          <PhotoCaption>Брови после</PhotoCaption>
        </PhotoFigure>
      }
    </Toggle>
  </ParticipantPhotosWrapper>
);

export default ParticipantPhotos;