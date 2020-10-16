import React from 'react';
import './ResultsBox.scss';
import logo from './logo.png';

class ResultsBox extends React.Component{
  get_split_results = (index) => {
    if(this.props.results.splits.length <= index)
      return; 

    let associations_list = this.props.results.splits[index].associations.map(result => {
      return <span className="association">{result.name}</span>;
    });
    
    return (
    <div>
      <header className="word_split">{this.props.results.splits[index].word}</header>
      <div className="associations_list">
        {associations_list}
      </div>
    </div>
    );
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

    return (
      <div className={box_class}>
        {this.get_split_results(0)} 
        {this.get_split_results(1)}
      </div>
    );
  }
}

export default ResultsBox;
