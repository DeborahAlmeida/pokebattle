import React, { useState, useEffect } from 'react';

import { useParams } from 'react-router-dom';

import { apiUrls, getFromApi, createTeamUrl } from 'utils/api.js';

import CardTeam from 'pages/CardTeam.js';

function Home(){
  const [user, setCurrentUser] = useState();
  const [battle, setBattle] = useState();

  const { id } = useParams();

  useEffect(() => {
    let abortController = new AbortController();
    getCurrentUserData()
    getTeamData()
    return () => {
      abortController.abort();
    }
  }, []);

  const getCurrentUserData = async () => {
    const user = await getFromApi(apiUrls.currentUser);
    setCurrentUser(user)
    return user;
  }
  const getTeamData = async () => {
    const data = await getFromApi(apiUrls.battleDetail(id));
    setBattle(data);
    return data;
  };
  let currentUserTeam = null
  let otherUserTeam = null
  if (!battle){
    return 'loading'
  }else{
    if (battle.teams.length == 1){
      currentUserTeam = (battle.teams[0].trainer.email == user.email) ? battle.teams[0] : null
      otherUserTeam = (currentUserTeam == null ? battle.teams[0] : null)
    }else if(battle.teams.length == 2){
      currentUserTeam = (battle.teams[0].trainer.email == user.email) ? battle.teams[0] : battle.teams[1]
      otherUserTeam = (currentUserTeam == battle.teams[0]) ? battle.teams[1] : battle.teams[0]
    }
  }
  
  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">Creator: {battle.creator ? battle.creator.email : ''}</h2> 
      <h2 className="subtitle_detail">Opponent: {battle.opponent ? battle.opponent.email : ''}</h2>
      {battle.winner ?
        <>
        <img className="img_detail" src="https://image.flaticon.com/icons/png/512/2119/2119019.png" alt="trofeu"/>
        <h2 className="subtitle_detail">The winner is {battle.winner ? battle.winner.email : ''}</h2> 
        </> : ''}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {currentUserTeam == null ? 
          <a className="button_battle button_battle_detail" href={createTeamUrl(battle.id)} role="button">
            Create your team
          </a>
          : <CardTeam pokemons={currentUserTeam.pokemons}/>}
        </div>
        <div>
          <p className="text_trainer">Opposing pokemons</p>
          {otherUserTeam == null ? 'No pokemons'
          : <CardTeam pokemons={otherUserTeam.pokemons}/>}
        </div>
      </div>
    </div>
  );
}

export default Home;
