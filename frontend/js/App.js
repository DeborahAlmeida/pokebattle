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
        <Route component={BattleDetail} path={Urls.battle_detail_v2(':id')} />
        <Route component={BattleList} path={Urls.battle_list_v2()} />
      </Switch>
    </Router>
  </SentryBoundary>
);

export default hot(App);
