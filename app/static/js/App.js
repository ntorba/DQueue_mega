import React, {Component} from 'react';
import Table from './Table';
import Form from './Form';

class App extends Component {
    state = {
        characters: []
    };

    removeCharacter = index => {
        const { characters } = this.state;

        this.setState({
            characters: characters.filter((character, i) => {
                return i !== index;
            })
        });
    }

    upVoteSong = index => {
      const newCharacters = this.state.characters;
      newCharacters[index]["voteCount"] = newCharacters[index]["voteCount"]+1;
      this.setState({
        characters: newCharacters
      });
    }

    handleSubmit = character => {
      this.setState({characters: [...this.state.characters, character]});
    }

    render() {
        return (
            <div className="container">
                <Table
                    characterData={this.state.characters}
                    removeCharacter={this.removeCharacter}
                    upVoteSong={this.upVoteSong}
                />
                <Form handleSubmit={this.handleSubmit} />
            </div>
        );
    }
}

export default App;
