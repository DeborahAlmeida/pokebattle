import { getTeamData } from 'utils/api';

import { BATTLE_DETAIL } from '../constants';

function getBattle(battleId) {
  return (dispatch) =>
    getTeamData(battleId).then((battleData) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battleData });
    });
}

export { getBattle };
