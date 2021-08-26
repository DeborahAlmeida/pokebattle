// import pages
import * as Sentry from '@sentry/browser';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import App from './App';
import { store } from './store';

import './bootstrap-includes';
import '../sass/style.scss';

Sentry.init({
  dsn: window.SENTRY_DSN,
  release: window.COMMIT_SHA,
});

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('react-app')
);
