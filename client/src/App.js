import './App.css';
import React from 'react';
import ResultsBox from './ResultsBox'

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      word: "",
      results: {
        first: [],
        second: [],
        grade: 0
      }
    };
  }

  handleChange = event => {
    this.setState({
      word: event.target.value
    });
  }

  render(){
    return (
      <div className="app">
        <div className="app_container">
          <input onChange={this.handleChange} placeholder="Memorize a word."/>
          <ResultsBox results={this.state.results}></ResultsBox>
        </div>
      </div>
    );
  }
}

export default App;
