import { normalize } from 'normalizr';

import { getTeamData } from 'utils/api';

import { BATTLE_DETAIL } from '../constants';
import * as schema from '../utils/schema';

function getBattle(battleId) {
  return (dispatch) =>
    getTeamData(battleId).then((battleData) => {
      const normalizedBattle = normalize(battleData, schema.battle);
      return dispatch({ type: BATTLE_DETAIL, payload: normalizedBattle });
    });
}

export { getBattle };
