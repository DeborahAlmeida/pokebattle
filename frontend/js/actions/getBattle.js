import { getTeamData } from 'utils/api';

import { BATTLE_DETAIL_STARTED, BATTLE_DETAIL_SUCCESSED, BATTLE_DETAIL_FAILED } from '../constants';

const getBattleDetailsStarted = () => ({
  type: BATTLE_DETAIL_STARTED,
});
const getBattleDetailsSuccess = (repoDetails) => ({
  type: BATTLE_DETAIL_SUCCESSED,
  payload: repoDetails,
});
const getBattleDetailsFailed = (error) => ({
  type: BATTLE_DETAIL_FAILED,
  error,
});

const getBattle = (battleId) => async (dispatch) => {
  dispatch(getBattleDetailsStarted());
  try {
    const battleDetails = await getTeamData(battleId);
    dispatch(getBattleDetailsSuccess(battleDetails));
  } catch (err) {
    dispatch(getBattleDetailsFailed(err.toString()));
  }
};

export { getBattle };
