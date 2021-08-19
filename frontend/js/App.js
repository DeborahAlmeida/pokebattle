import React from 'react';
import { hot } from 'react-hot-loader/root';
import {
	BrowserRouter as Router,
	Switch,
	Route,
} from 'react-router-dom';
import Home from './pages/Home';
import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
	<Router>
		<Switch>
			<Route path="/react/battle/detail/:id" component={Home} />
		</Switch>
	</Router>
  </SentryBoundary>
);

export default hot(App);
