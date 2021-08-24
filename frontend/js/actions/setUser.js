import { getCurrentUserData } from 'utils/api';

import { CURRENT_USER } from '../constants';

function setCurrentUser() {
  return (dispatch) =>
    getCurrentUserData().then((userData) => {
      return dispatch({ type: CURRENT_USER, payload: userData });
    });
}
export { setCurrentUser };
