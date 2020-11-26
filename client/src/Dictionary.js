import React from 'react';
import './Dictionary.scss';

/** Dictionary box component. */
class Dictionary extends React.Component {
  /**
   * Check if the dictionary searched word equals to the main input word.
   * @returns {boolean}
   */
  isSyncedToMainInput = () => {
    return this.props.dictionary.word.toLowerCase() === this.props.word.toLowerCase();
  }

  /**
   * Check if the dictionary is empty.
   * @returns {boolean}
   */
  isEmptyDictionary = () => {
    return this.props.dictionary.definitions.length == 0;
  }

  /**
   * Get dictionary definitions div.
   */
  getDictionaryDefinitions = definitions => {
    return definitions.map(
      definition => {
        // Definition format: `type definition_paragraph`
        let definition_parts = definition.split(/[^A-Za-z]/);
        const definition_type = definition_parts[0];
        const extracted_definition = definition_parts.splice(1).join(" ");
        return (
          <li>
            <span> {definition_type} </span>
            {` ${extracted_definition}.`}
          </li>
        );
      }
    )
  }

  render = () => {
    if(this.isEmptyDictionary() || !this.isSyncedToMainInput()){
      return <div></div>
    }
    
    return (
      <div className="definitions_container">
        <h3> {this.props.dictionary.word} </h3>
        <ul> {this.getDictionaryDefinitions(this.props.dictionary.definitions)} </ul>
      </div>
    )
  }
}

export default Dictionary;
