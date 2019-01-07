import React from 'react';
import { connect } from 'react-redux';
import { testAction, testAction2 } from '../redux/actions/postActions';

const axios = require('axios');

class Ai extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillMount() {
    this.props.testAction();
    this.props.testAction2();
  }

  // submits input to python
  submitInput = e => {
    e.preventDefault();
    const input = document.getElementById('input').value;
    const formData = new FormData();
    formData.append('input', input);

    axios
      .post('/listen', formData)
      .then(response => {
        console.log(response.data);
      })
      .catch();
  };

  render() {
    return (
      <section id="ai">
        <div className="chatbox flex-cl-c-c text-center">
          <div className="m50b-s">
            <img className="mainAiImage" src="../../dist/img/ai.svg" />
          </div>
          <form onSubmit={this.submitInput}>
            <textarea id="input" className="w100 m25b-s" />
            <input type="submit" value="submit" />
          </form>
        </div>
      </section>
    );
  }
}

const mapStateToProps = state => ({
  actions: state.actions
});

export default connect(
  mapStateToProps,
  { testAction, testAction2 }
)(Ai);
