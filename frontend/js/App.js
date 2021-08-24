import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import BattleDetail from './pages/BattleDetail';
import BattleList from './pages/BattleList';
import SentryBoundary from './utils/SentryBoundary';
import Urls from './utils/urls';

const App = () => (
  <SentryBoundary>
    <Router>
      <Switch>
        <Route component={BattleDetail} path={Urls.spa_template(':id')} />
        <Route component={BattleList} path={Urls.spa_template_list()} />
      </Switch>
    </Router>
  </SentryBoundary>
);

export default hot(App);
