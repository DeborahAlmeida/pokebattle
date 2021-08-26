import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import BattleDetail from './pages/BattleDetail';
import SentryBoundary from './utils/SentryBoundary';
import Urls from './utils/urls';

const App = () => (
  <SentryBoundary>
    <Router>
      <Switch>
        <Route component={BattleDetail} path={Urls.battle_detail_v2(':id')} />
      </Switch>
    </Router>
  </SentryBoundary>
);

export default hot(App);
