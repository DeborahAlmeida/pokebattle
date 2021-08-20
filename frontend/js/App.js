import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import BattleDetail from './pages/BattleDetail';
import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
    <Router>
      <Switch>
        <Route component={BattleDetail} path="/react/battle/detail/:id" />
      </Switch>
    </Router>
  </SentryBoundary>
);

export default hot(App);
