/**  
 * Associations results box componenet.
 */
import React from 'react';
import './ResultsBox.scss';
import logo from './assets/logo.png';

class ResultsBox extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      highlights: []
    }
  }

  /**
   * Is the given word is already highlighted (list).
   * @param {string} word Clicked word. 
   */
  isAlreadyHighlighted = word => {
    return this.state.highlights.includes(word);
  }

  /***
   * Add clicked word into marked list.
   */
  handleWordClick = event => {
    const word = event.target.text;
    let highlights = this.state.highlights;

    if(!this.isAlreadyHighlighted(word))  
      highlights.push(word);

      else{
      const index = this.state.highlights.indexOf(word);
      highlights.splice(index, 1);
    }

    this.setState({highlights})
  }
  
  /**
   * Get specific split results.
   * @param {int} index Split number. 
   */
  getResultsSection = (results) => {
    let associationsList = results.associations.map(result => {
      let className = "association";
      
      if(this.isAlreadyHighlighted(result.name))
        className += " mark"

      return <a className={className} href="#" onClick={this.handleWordClick}>{result.name}</a>;
    });
    return (
      <div>
        <header className="word_split">{results.word}</header>
        <div className="associations_list">
          {associationsList}
        </div>
        <br/>
      </div>
    );
  }
  
  render(){
    let box_class = this.props.loadingNewResults ? "box_container loading" : "box_container";
    if(!this.props.results || Object.keys(this.props.results).length === 0){
      return (
        <div className={box_class}>
          <a>
            <img src={logo} className="logo"/>
            <br/>
          </a>
        </div>
      );
    }
    return (
      <div className={box_class}>
        {
          this.props.results.splits.map((element)=>{
            return this.getResultsSection(element)
          })
        } 
      </div>
    );
  }
}

export default ResultsBox;
