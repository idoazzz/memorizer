import './App.scss';
import axios from 'axios';
import React from 'react';
import ResultsBox from './ResultsBox'

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      word: "",
      results: {},
      isLoading: false,
    };
  }

  handleChange = event => {
    this.setState({word: event.target.value});
  }

  handleSubmit = event => {
    event.preventDefault()
    
    if(this.state.isLoading){
      alert("Already searching another query.");  
      return;
    }
    
    this.setState({isLoading: true});

    this.currentRequest = axios.get(`http://localhost:8000/${this.state.word}`).
    then(response => {
      this.setState({
        isLoading: false,
        results: response.data,
      });
    });
  }
  
  render(){
    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            <input className="main_input" onChange={this.handleChange} placeholder="Memorize a word."/>
            <input className="main_input submit_button" type="submit" value=">"/>
          </form>
        </div>
        <div className="results_container">
          <ResultsBox results={this.state.results}></ResultsBox>
        </div>
      </div>
    );
  }
}

export default App;
