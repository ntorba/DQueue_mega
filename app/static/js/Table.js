import React, {Component} from 'react';


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

export default Table;
