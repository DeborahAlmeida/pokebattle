import axios from 'axios';

import Urls from './urls';

const baseUrl = window.location.host;

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCurrentUserData = async (setCurrentUser) => {
  const user = await getFromApi(Urls.api_current_user());
  setCurrentUser(user);
  return user;
};

const getBattleData = async (id, setBattle) => {
  const data = await getFromApi(Urls.api_battle_detail(id));
  setBattle(data);
  return data;
};

export { getFromApi, getCurrentUserData, getBattleData };
