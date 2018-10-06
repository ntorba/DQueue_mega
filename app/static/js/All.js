import React, {Component} from 'react';

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

class Form extends Component {
  constructor(props) {
    super(props);

    this.initialState = {
      song: '',
      artist: '',
      addedBy:'',
      voteCount: 1
    };
    this.state = this.initialState;
  }

  handleChange = event => {
    const {name, value} = event.target;

    this.setState({
      [name] : value
    });
  }

  submitForm = () => {
    this.props.handleSubmit(this.state);
    this.setState(this.initialState);
  }

  render() {
    const {song,artist,addedBy} = this.state;

    return (
      <form>
        <label>Song</label>
        <input
          type="text"
          name="song"
          value={song}
          onChange={this.handleChange}
        />

        <label>Artist</label>
        <input
          type="text"
          name="artist"
          value={artist}
          onChange={this.handleChange}
        />

        <label>Added By</label>
        <input
          type="text"
          name="addedBy"
          value={addedBy}
          onChange={this.handleChange}
        />

        <input
          type="button"
          value="Submit"
          onClick={this.submitForm}
        />

      </form>
    );

  }
}

const TableHeader = () => {
  return (
    <thead>
      <tr>
        <th>Song</th>
        <th>Artist</th>
        <th>Added By</th>
        <th>Vote Count</th>
        <th>Up Vote</th>
        <th>Delete</th>
      </tr>
    </thead>
  );
}

const TableBody = props => {
  const rows = props.characterData.sort((a,b) => a.voteCount < b.voteCount).map((row, index) => {
    return (
          <tr key={row.song}>
            <td>{row.song}</td>
            <td>{row.artist}</td>
            <td>{row.addedBy}</td>
            <td>{row.voteCount}</td>
            <td><button onClick={() => props.upVoteSong(index)}>UpVote</button></td>
            <td><button onClick={() => props.removeCharacter(index)}>Delete</button></td>
          </tr>
    );
  });

  return <tbody>{rows}</tbody>;
}

class Table extends Component {
  render() {
    const { characterData, removeCharacter, upVoteSong } = this.props;
    //console.log(this.props);
    return(
      <table>
        <TableHeader />
        <TableBody
          characterData={characterData}
          removeCharacter={removeCharacter}
          upVoteSong={upVoteSong}
        />
      </table>
  );
 }
}

ReactDOM.render(<App />, document.getElementById('root'));
