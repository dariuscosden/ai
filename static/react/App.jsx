import React, { Component } from 'react';
import { Provider } from 'react-redux';
import Ai from './Ai';
import store from '../redux/store';

// main app component
class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Ai />
      </Provider>
    );
  }
}

export default App;
