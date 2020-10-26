import './Dictionary.scss';
import React from 'react';

// TODO: Change class name.
class Dictionary extends React.Component{
  constructor(props){
    super(props);
  }

  render(){
    if(this.props.dictionary.definitions.length==0)
    return <div></div>

    return <div className="definitions_container">
       <h3>{this.props.dictionary.word}</h3>
        <ul>
        {
          this.props.dictionary.definitions.map(definition => {
              let defintion_parts = definition.split(/[^A-Za-z]/); 
              const definition_type = defintion_parts[0];
              const extracted_definition = defintion_parts.splice(1).join(" ");
              return <li>
              <span className="definition_type">{definition_type}</span>
              {` ${extracted_definition}.`} 
              </li>;
          })
        }
        </ul>
    </div>
  }
}

export default Dictionary;
