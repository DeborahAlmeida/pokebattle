import { getBattles } from 'utils/api';

import { BATTLE_LIST } from '../constants';

function fetchBattleList() {
  return (dispatch) =>
    getBattles().then((battlesData) => {
      return dispatch({ type: BATTLE_LIST, payload: battlesData });
    });
}

export { fetchBattleList };
