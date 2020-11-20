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
  
  TYPING_TIMEOUT = 1000 // miliseconds
  DEFAULT_ASSOCIATIONS_LIMIT = 10;
  
  constructor(props){
    super(props);
    this.typingTimer = 0;
    this.state = {
      // User input word.
      word: "",
      closestWord: "",
      
      results: {},
      isLoading: false,
      
      // Closest word dictionary.
      dictionary: {
        word: "",
        definitions: []
      },

      // Advanced search.
      autoSplitting: true,
      showingAdvancedSearch: true,
      associationsLimit: this.DEFAULT_ASSOCIATIONS_LIMIT,
    };
  }

  handleMainInputChange = event => {
    let currentWord = event.target.value; 
    this.setState({
      word: currentWord,
      closestWord: ""
    });
    
    if(currentWord === ""){
      return;
    }

    if(this.typingTimer){
      clearTimeout(this.typingTimer);
    }

    this.typingTimer = setTimeout(() => {
      this.findClosestWord(currentWord);
    }, this.TYPING_TIMEOUT);
  }

  findClosestWord = word => {
    axios.get(`/closest/${word}`).
    then(response => {
      if(word === this.state.word){
        // If the current input word is the searched word.
        console.log(response.data.word)
        this.setState({
          closestWord: response.data.word,
        });
      }
    });
  }

  handleAssociationsLimitChange = event => {
    this.setState({associationsLimit: event.target.value});
  }

  getErrorBox = () => {
    if(!this.isAllLetters(this.state.word) && this.state.word){
      return <div className="helper error"> 
                  We don't like associate stuff that are not letters...
              </div>; 
    }
  }

  isAllLetters = (string) => {
   let letters = /^[A-Za-z]+$/;
   if(string.match(letters))
      return true;
   return false;
  }

  handleSubmit = event => {
    event.preventDefault()
    let searchedWord = this.state.word;
    if(!this.isAllLetters(searchedWord))
      return;
      
    if(this.state.isLoading){
      alert("Already searching another query.");  
      return;
    }

    this.fetchWordDefinition(searchedWord);
    this.fetchWordAssociations(searchedWord);
  }

  fetchWordAssociations = word => {
    this.setState({isLoading: true});
    axios.get(`/associations/${word}`, {
      params: {
        split: this.state.autoSplitting,
        limit: this.state.associationsLimit
      }
    }).
    then(response => {
      this.setState({
        isLoading: false,
        results: response.data,
      });
    });
  }

  fetchWordDefinition = word => {
    axios.get(`/definitions/${word}`).
    then(response => {
      this.setState({
        dictionary: {
          word: response.data.word,
          definitions: response.data.definitions,
        }});
    });
  }
  
  getWordCorrectionBox = () => {
    if(this.state.closestWord !== this.state.word &&
       this.state.closestWord !== ""){
      return <div className="helper" 
                  onClick={() => this.setState({
                    word: this.state.closestWord
                  })}>
        Did you mean <i>{this.state.closestWord}</i>?
      </div>;
    }  
    return <div></div>;
  }

  handleAutosplittingCheck = () => {
    this.setState({ autoSplitting: !this.state.autoSplitting })
  }
  
  getAdvancedSearchBox = () => {
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
              value={this.state.associationsLimit}/>

        <span className="input_header"> Autosplitting</span>
        <input className="checkbox" checked={this.state.autoSplitting} 
                onChange={this.handleAutosplittingCheck} type="checkbox"/>
      </div>
     )
     // Insert to the  autosplittting functionality and design.
    }
  }
  
  render(){
    let loading = this.state.isLoading;
    let button_class = loading ? "rotating" : "";

    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            <input className="main_input" onChange={this.handleMainInputChange} 
                   placeholder="Memorize a word." value={this.state.word}/>
            <button className="main_input submit_button" type="submit">
              <AiOutlineAlert className={button_class}/>
            </button>
          </form>
          { this.getWordCorrectionBox() }
          { this.getAdvancedSearchBox() }
          { this.getErrorBox() }
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
