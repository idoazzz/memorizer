/**
 * Main memorizer app component.
 */
import './App.scss';
import axios from 'axios';
import React from 'react';
import ResultsBox from './ResultsBox'
import Dictionary from './Dictionary';
import { AiOutlineUp } from 'react-icons/ai';
import { AiOutlineDown } from 'react-icons/ai';
import { AiOutlineAlert } from 'react-icons/ai';

class App extends React.Component {
  TYPING_TIMEOUT = 1000 // miliseconds
  DEFAULT_ASSOCIATIONS_LIMIT = 10;

  constructor(props) {
    super(props);
    this.loadingNewResults = false;
    this.activeTypingTimer = 0;
    this.state = {
      // User input word.
      word: "",
      closestWord: "",

      results: {},

      // Closest word dictionary.
      dictionary: {
        word: "",
        definitions: []
      },

      // Advanced search.
      autoSplitting: false,
      showingAdvancedSearch: true,
      associationsLimit: this.DEFAULT_ASSOCIATIONS_LIMIT,
    };

    // Cancel token for pending requests.
    this.current_word_requests_cancel_token = axios.CancelToken.source();
  }

  /**
   * Handle changes in the main input and dispatch the typing timer.
   * @param {Event} event Onchange event. 
   * Each time the timer is finishing it calculates the closest word hint.
   */
  handleMainInputChange = event => {
    let currentWord = event.target.value;

    // Cancel token for current request and generate new one. 
    if (this.loadingNewResults) {
      this.current_word_requests_cancel_token.cancel();
      this.current_word_requests_cancel_token = axios.CancelToken.source();
    }

    this.setState({
      word: currentWord,
      closestWord: ""
    });

    if (currentWord === "") {
      return;
    }

    if (this.activeTypingTimer) {
      clearTimeout(this.activeTypingTimer);
    }

    this.activeTypingTimer = setTimeout(() => {
      this.findClosestWord(currentWord);
    }, this.TYPING_TIMEOUT);
  }

  /**
   * Check if the given word equals to the main input word.
   * @returns {boolean}
   */
  isSyncedToMainInput = word => {
    return word.toLowerCase() === this.state.word.toLowerCase()
  }

  /**
   * Check if the given string is only alpha letters.
   * @param {string} string Target string. 
   */
  isAllLetters = (string) => {
    let letters = /^[A-Za-z]+$/;
    if (string.match(letters))
      return true;
    return false;
  }

  /**
   * Find the closest word (input error correction).
   * @param {word} word Target word.
   */
  findClosestWord = word => {
    axios.get(`/closest/${word}`, {
      cancelToken: this.current_word_requests_cancel_token.token,
    }).
      then(response => {
        if (this.isSyncedToMainInput(word)) {
          this.setState({
            closestWord: response.data.word,
          });
        }
      }).catch(() => { });
  }

  /**
   * Associations limit changes handler.
   * @param {Event} event onChange event. 
   */
  handleAssociationsLimitChange = event => {
    this.setState(
      {
        associationsLimit: event.target.value,
      }
    );
  }

  /**
   * Auto splitting checkbox changes handler.
   * @param {Event} event onChange event. 
   */
  handleAutosplittingCheck = () => {
    this.setState(
      {
        autoSplitting: !this.state.autoSplitting
      }
    );
  }

  /**
   * Submitting word form for generating associations. 
   * @param {Event} event onSubmit event. 
   */
  handleSubmit = event => {
    event.preventDefault()
    let searchedWord = this.state.word.toLowerCase();
    this.performSearch(searchedWord);
  }

  /**
   * Perform total search and update results for specific word.
   * @param {string} word Searched word. 
   */
  performSearch = word => {
    if (!this.isAllLetters(word))
      return;

    this.updateWordDefinition(word);
    this.updateWordAssociations(word);
  }

  /**
   * @param {boolean} loading Is the component loading results. 
   */
  updateLoading = loading => {
    this.loadingNewResults = loading;
  }

  /**
   * Get from the server the compatible associations for this word.
   * @param {string} word Searched word. 
   */
  updateWordAssociations = word => {
    this.updateLoading(true);
    axios.get(`/associations/${word}`, {
      cancelToken: this.current_word_requests_cancel_token.token,
      params: {
        split: this.state.autoSplitting,
        limit: this.state.associationsLimit
      }
    }).
      then(response => {
        this.updateLoading(false);
        this.setState({ results: response.data });
      }).catch(() => { });
  }

  /**
   * Searching and updating word definition.
   * @param {string} word Searched word.
   */
  updateWordDefinition = word => {
    axios.get(`/definitions/${word}`, {
      cancelToken: this.current_word_requests_cancel_token.token,
    }).
      then(response => {
        this.setState({
          dictionary: {
            word: response.data.word,
            definitions: response.data.definitions,
          }
        });
      }).catch(() => { });
  }

  /**
   * Check if the word is valid, if not return an error box.
   */
  getErrorBox = () => {
    if (!this.isAllLetters(this.state.word) && this.state.word) {
      return (
        <div className="helper error">
          <AiOutlineAlert className="" /> We don't like associate stuff that are not letters...
        </div>
      );
    }
  }

  /**
   * Check if there is word connection, if exists return correction box.
   */
  getWordCorrectionBox = () => {
    const closestWord = this.state.closestWord;
    if (!this.isSyncedToMainInput(closestWord) && closestWord !== "") {
      return (
        <div className="helper" onClick={() => {
          // Correct the current word and perform new search.
          const newWord = closestWord;
          this.setState({ word: newWord });
          this.performSearch(newWord);
        }}>
        Did you mean <i>{closestWord}</i>?
        </div>
      );
    }
    return <div></div>;
  }

  /**
   * Toggle advanced search display.
   */
  toggleAdvancedSearch = () => {
    this.setState(
      { 
        showingAdvancedSearch: !this.state.showingAdvancedSearch 
      }
    );
  }

  /**
   * Get advanced search box.
   */
  getAdvancedSearchBox = () => {
    const showingAdvancedSearch = this.state.showingAdvancedSearch;
    if (!showingAdvancedSearch)
      return (
        <div>
          <AiOutlineDown onClick={this.toggleAdvancedSearch} className="search_settings_button"/>
        </div>
      );
    else {
      return (
        <div className="advanced_search">
          <AiOutlineUp onClick={this.toggleAdvancedSearch} className="search_settings_button"/>
          <span className="input_header">Associations</span>
          <input onChange={this.handleAssociationsLimitChange} placeholder="?" value={this.state.associationsLimit}/>

          <span className="input_header"> Autosplitting</span>
          <input onChange={this.handleAutosplittingCheck} className="checkbox" checked={this.state.autoSplitting} 
                 type="checkbox"/>
        </div>
      );
    }
  }

  render() {
    return (
      <div className="app_container">
        <div className="main_form">
          <form onSubmit={this.handleSubmit}>
            {this.getErrorBox()}

            <input className="main_input" onChange={this.handleMainInputChange}
              placeholder="Memorize a word." value={this.state.word} />

            <button className="main_input submit_button" type="submit">
              <AiOutlineAlert className={this.loadingNewResults ? "rotating" : ""} />
            </button>
          </form>

          {this.getWordCorrectionBox()}
          {this.getAdvancedSearchBox()}

          <Dictionary dictionary={this.state.dictionary} word={this.state.word} />
        </div>
        
        <div className="results_container">
          <ResultsBox word={this.state.word} results={this.state.results} loadingNewResults={this.loadingNewResults} />
        </div>
      </div>
    );
  }
}

export default App;
