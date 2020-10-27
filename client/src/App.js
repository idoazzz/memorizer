import './App.scss';
import axios from 'axios';
import React from 'react';
import ResultsBox from './ResultsBox'
import Dictionary from './Dictionary';
import { AiOutlineAlert } from 'react-icons/ai';
import { AiOutlineUp } from 'react-icons/ai';
import { AiOutlineDown } from 'react-icons/ai';

/**
 * Main memorizer app component.
 */
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
      showingAdvancedSearch: true,
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
  
  get_advanced_search = () => {
    const showingAdvancedSearch = this.state.showingAdvancedSearch;
    if(!showingAdvancedSearch)
      return (
      <div>
      <AiOutlineDown
        onClick={ () => { 
          this.setState({showingAdvancedSearch: !showingAdvancedSearch}) 
        }}
        className="search_settings_button"/>
      </div>
      )
    else{
      return (
      <div className="advanced_search">

        <AiOutlineUp className="search_settings_button"
      onClick={ () => { 
        this.setState({showingAdvancedSearch: !showingAdvancedSearch}) 
      }}
      />
      <span className="input_header">Results</span>
      <input placeholder="5"/>
      
      <span className="input_header">Splits</span>
      <input placeholder="5"/>
      </div>
     )
    }
  }
  
  render(){
    // Adding advanced search: Associations limit, splits number,
    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            <input className="main_input" onChange={this.handleChange} placeholder="Memorize a word."/>
            <button className="main_input submit_button" type="submit"><AiOutlineAlert/></button>
          </form>
          { this.get_advanced_search() }
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
