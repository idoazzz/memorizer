import './App.css';
import axios from 'axios';
import React from 'react';
import ResultsBox from './ResultsBox'

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      word: "",
      results: {}
    };
  }

  handleChange = event => {
    this.setState({
      word: event.target.value
    });
  }
  
  componentDidMount(){
    axios.get(`http://localhost:3000/${this.state.word}`).
          then(response => {
            console.log(response);
            this.setState({
              results: response.data
            });
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
