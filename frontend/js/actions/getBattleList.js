import { normalize } from 'normalizr';

import { getBattles } from 'utils/api';

import { BATTLE_LIST } from '../constants';
import * as schema from '../utils/schema';

function getBattleList() {
  return (dispatch) =>
    getBattles().then((battlesData) => {
      const normalizedBattleList = normalize(battlesData, schema.battleList);
      return dispatch({ type: BATTLE_LIST, payload: normalizedBattleList });
    });
}

export { getBattleList };
