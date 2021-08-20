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

export { apiUrls, getFromApi, createTeamUrl };
