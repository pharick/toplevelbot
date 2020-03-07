import React, {Component} from "react";
import styled from 'styled-components';

const CaptionButton = styled.button`
  font-size: 1em;
  background: none;
  border: none;
  color: white;
  padding: 0;
  display: flex;
  align-items: center;
`;

const MarkerWrapper = styled.span`
  font-size: 0.5em;
  margin-right: 0.5em;
`;

const Content = styled.div`
  display: ${props => props.visible ? 'block' : 'none'};
`;

const Marker = ({isOpen}) => (
  <MarkerWrapper>
    {isOpen ? '▼' : '▷'}
  </MarkerWrapper>
);

class Toggle extends Component {
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
        <CaptionButton onClick={this.toggleState}><Marker isOpen={this.state.isOpen}/> {this.props.title}</CaptionButton>

        <Content visible={this.state.isOpen}>
          {this.props.children}
        </Content>
      </>
    );
  }
};

export default Toggle;