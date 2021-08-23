import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import CardTeam from 'components/CardTeam';
import { createTeamUrl, getCurrentUserData, getTeamData } from 'utils/api';
import { showTeams } from '../utils/battle-detail';

function BattleDetail() {
  const [user, setCurrentUser] = useState();
  const [battle, setBattle] = useState();

  const { id } = useParams();

  useEffect(() => {
    getCurrentUserData(setCurrentUser);
    getTeamData(id, setBattle);
  }, []);

  if (!battle) {
    return (
      <div className="battle_container_detail">
        <img
          alt="battle not found"
          className="img_detail"
          src="http://www.i2softbd.com/template/TPL-007/images/404-Page-Not-Found.png"
        />
      </div>
    );
  }
  const teams = showTeams(battle, user);

  const currentUserTeam = teams[0];
  const otherUserTeam = teams[1];

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">Creator: {battle.creator ? battle.creator.email : ''}</h2>
      <h2 className="subtitle_detail">Opponent: {battle.opponent ? battle.opponent.email : ''}</h2>
      {battle.winner ? (
        <>
          <img
            alt="trofeu"
            className="img_detail"
            src="https://image.flaticon.com/icons/png/512/2119/2119019.png"
          />
          <h2 className="subtitle_detail">
            The winner is {battle.winner ? battle.winner.email : ''}
          </h2>
        </>
      ) : (
        ''
      )}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {currentUserTeam === null ? (
            <a
              className="button_battle button_battle_detail"
              href={createTeamUrl(battle.id)}
              role="button"
            >
              Create your team
            </a>
          ) : (
            <CardTeam pokemons={currentUserTeam.pokemons} />
          )}
        </div>
        <div>
          <p className="text_trainer">Opposing pokemons</p>
          {otherUserTeam === null ? 'No pokemons' : <CardTeam pokemons={otherUserTeam.pokemons} />}
        </div>
      </div>
    </div>
  );
}

export default BattleDetail;
