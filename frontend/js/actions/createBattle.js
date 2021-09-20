import { createBattle } from 'utils/api';

import { BATTLE_CREATE } from '../constants';

function createBattleAction(data) {
  return (dispatch) =>
    createBattle(data).then((response) => {
      return dispatch({ type: BATTLE_CREATE, payload: response });
    });
}

export { createBattleAction };
