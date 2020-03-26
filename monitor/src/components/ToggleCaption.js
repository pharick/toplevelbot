import React, {Component} from "react";
import styled from 'styled-components';

const CaptionButton = styled.button`
  width: 100%;
  font-size: 1em;
  background: none;
  border: none;
  color: white;
  padding: 0;
  display: flex;
  align-items: center;
  
  @media(max-width: 1200px) {
    border-bottom: 1px solid rgba(100, 100, 100, 0.4);
    padding: 0.2em;
    margin: 0;
    cursor: pointer;
    
    &:hover {
      background-color: rgba(100, 100, 100, 0.4);
    }
  }
`;

const MarkerWrapper = styled.span`
  font-size: 0.5em;
  margin-right: 0.5em;
  
  @media(min-width: 1200px) {
    display: none;
  }
`;

const Content = styled.div`
  display: none;
  font-size: 1rem;

  @media(max-width: 1200px) {
    display: ${props => props.visible ? 'block' : 'none'};
  }
`;

const Marker = ({ isOpen }) => (
  <MarkerWrapper>
    {isOpen ? '▼' : '▷'}
  </MarkerWrapper>
);

class ToggleCaption extends Component {
  state = {
    isOpen: false
  };

  toggleState = () => {
    this.setState((state) => ({
      isOpen: !state.isOpen
    }));
  };

  render() {
    return (
      <>
        <CaptionButton onClick={this.toggleState}>
          <Marker isOpen={this.state.isOpen}/>
          {this.props.title}
        </CaptionButton>

        <Content visible={this.state.isOpen}>
          {this.props.children}
        </Content>
      </>
    );
  }
}

export default ToggleCaption;