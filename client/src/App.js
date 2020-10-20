import './App.scss';
import axios from 'axios';
import React from 'react';
import ResultsBox from './ResultsBox'
import Dictionary from './Dictionary';

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      word: "",
      results: {},
      isLoading: false,
      dictionary: {
        word: "",
        definitions: []
      },
    };
  }

  handleChange = event => {
    this.setState({word: event.target.value});
  }

  handleSubmit = event => {
    event.preventDefault()
    if(!this.state.word)
      return;
      
    if(this.state.isLoading){
      alert("Already searching another query.");  
      return;
    }
    
    // TODO: Split to functions.

    this.setState({isLoading: true});
    axios.get(`/associations/${this.state.word}`).
    then(response => {
      this.setState({
        isLoading: false,
        results: response.data,
      });
    });
    
    axios.get(`/definitions/${this.state.word}`).
    then(response => {
      this.setState({
        dictionary: {
          word: response.data.word,
          definitions: response.data.definitions,
        }});
    });
  }
  
  render(){
    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            <input onChange={this.handleChange} placeholder="Memorize a word."/>
            <input className="submit_button" type="submit" value=">"/>
          </form>
          <Dictionary dictionary={this.state.dictionary}/>
        </div>
        <div className="results_container">
          <ResultsBox word={this.state.word}
                      results={this.state.results}
                      isLoading={this.state.isLoading}/>
        </div>

      </div>
    );
  }
}

export default App;
