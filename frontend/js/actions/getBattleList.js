import { getBattles } from 'utils/api';

import { BATTLE_LIST } from '../constants';

function getBattleList() {
  return (dispatch) =>
    getBattles().then((battlesData) => {
      return dispatch({ type: BATTLE_LIST, payload: battlesData });
    });
}

export { getBattleList };
