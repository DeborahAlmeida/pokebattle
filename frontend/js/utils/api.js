import axios from 'axios';

const baseUrl = window.location.host;

const apiUrls = {
  battleDetail: (id) => `api/battle/${id}`,
  currentUser: 'api/user/',
};

const createTeamUrl = (id) => {
  const url = `http://${baseUrl}/team/${id}/create/`;
  return url;
};

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}/${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCurrentUserData = async (setCurrentUser) => {
  const user = await getFromApi(apiUrls.currentUser);
  setCurrentUser(user);
  return user;
};

const getTeamData = async (id, setBattle) => {
  const data = await getFromApi(apiUrls.battleDetail(id));
  setBattle(data);
  return data;
};

export { apiUrls, getFromApi, createTeamUrl, getCurrentUserData, getTeamData };
