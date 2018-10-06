import React, { Component } from 'react';

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
  export default Form;
