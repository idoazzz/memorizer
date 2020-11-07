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
  
  DEFAULT_ASSOCIATIONS_LIMIT = 10;
  
  constructor(props){
    super(props);
    this.state = {
      // User input word.
      word: "",
      closest_word: "",

      // TODO: Continue with the timer: https://stackoverflow.com/questions/42217121/how-to-start-search-only-when-user-stops-typing
      typing: false,
      typingTimer: 0,

      results: {},
      isLoading: false,
      
      // Closest word dictionary.
      dictionary: {
        word: "",
        definitions: []
      },

      // Advanced search.
      showingAdvancedSearch: true,
      associations_limit: this.DEFAULT_ASSOCIATIONS_LIMIT,
    };
  }

  handleMainInputChange = event => {
    let current_word = event.target.value; 
    this.setState({word: current_word});
    
    if(this.state.word === ""){
      return;
    }
  }

  findClosestWord = current_word => {
    axios.get(`/closest/${current_word}`).
    then(response => {
      this.setState({
        closest_word: response.data.word,
      });
    });
  }

  handleAssociationsLimitChange = event => {
    this.setState({associations_limit: event.target.value});
  }

  getWordCorrection = () => {
    if(this.state.closest_word !== this.state.word &&
       this.state.closest_word !== ""){
      return <div className="helper">
        Did you mean <i>{this.state.closest_word}</i>?
      </div>;
    }  
    return <div></div>;
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
    axios.get(`/associations/${this.state.word}`, {
      params: {
        limit: this.state.associations_limit
      }
    }).
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
  
  getAdvancedSearch = () => {
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
      <span className="input_header">Associations</span>
      <input placeholder="?" onChange={this.handleAssociationsLimitChange} 
             value={this.state.associations_limit}/>
      </div>
     )
    }
  }
  
  render(){
    let loading = this.state.isLoading;
    let button_class = loading ? "rotating" : "";

    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            <input className="main_input" onChange={this.handleMainInputChange} placeholder="Memorize a word."/>
            <button className="main_input submit_button" type="submit">
              <AiOutlineAlert className={button_class}/>
            </button>
          </form>
          { this.getWordCorrection() }
          { this.getAdvancedSearch() }
          <Dictionary dictionary={this.state.dictionary} word={this.state.word}/>
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
