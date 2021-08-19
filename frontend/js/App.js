import React from 'react';

import { hot } from 'react-hot-loader/root';

import {
	BrowserRouter as Router,
	Switch,
	Route,
} from 'react-router-dom';

import BattleDetail from './pages/BattleDetail';

import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
	<Router>
		<Switch>
			<Route path="/react/battle/detail/:id" component={BattleDetail} />
		</Switch>
	</Router>
  </SentryBoundary>
);

export default hot(App);
