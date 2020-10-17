import React from 'react';
import './ResultsBox.scss';
import logo from './logo.png';

class ResultsBox extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      highlights: []
    }
  }

  handleWordClick = event => {
    let highlights = this.state.highlights;
    if(!this.state.highlights.includes(event.target.text))  
      highlights.push(event.target.text);
  
    else{
      const index = this.state.highlights.indexOf(event.target.text);
      if (index > -1) {
        highlights.splice(index, 1);
      }
    }

    this.setState({highlights})
  }
  
  get_split_results = (index) => {
    if(this.props.results.splits.length <= index)
      return; 

    let associations_list = this.props.results.splits[index].associations.map(result => {
      let className = "association";
      if(this.state.highlights.includes(result.name))
        className += " mark"
      return <a className={className} href="#" onClick={this.handleWordClick}>{result.name}</a>;
    });
    
    return (
    <div>
      <header className="word_split">{this.props.results.splits[index].word}</header>
      <div className="associations_list">
        {associations_list}
      </div>
      <br/>
    </div>
    );
  }
  
  get_hint(){
    if(this.state.highlights.length > 0)
      return <span>{this.props.word} > {this.state.highlights.join(" ")}</span>
    return;
  }

  render(){
    let loading = this.props.isLoading;
    let box_class = loading ? "box_container loading" : "box_container";
    if(!this.props.results || 
        Object.keys(this.props.results).length === 0)
        return <div className={box_class}>
          <a>
              <img src={logo}/>
              <br/>
              There is no associations.
          </a>
        </div>;
    return <div className={box_class}>
        {this.get_split_results(0)} 
        {this.get_split_results(1)}
        {this.get_hint()}
      </div>;
  }
}

export default ResultsBox;
