import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import reducer from './reducers/rootReducer';

const middleware = [thunk];

// enable extension in dev mode
//
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

// creates redux store
const store = createStore(
  reducer,
  {},
  composeEnhancers(applyMiddleware(...middleware)),
);

export default store;
