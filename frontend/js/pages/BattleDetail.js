import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import CardTeam from 'components/CardTeam';
import { getFromApi, getCurrentUserData, getBattleData } from 'utils/api';

import { orderTeamsByCurrentUser } from '../utils/battle-detail';
import Urls from '../utils/urls';

function BattleDetail() {
  const [user, setCurrentUser] = useState();
  const [battle, setBattle] = useState();

  const { id } = useParams();
  useEffect(() => {
    getCurrentUserData(setCurrentUser);
    getBattleData(id, setBattle);
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
  const { current, other } = orderTeamsByCurrentUser(battle, user);

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
          {current === null ? (
            <a
              className="button_battle button_battle_detail"
              href={getFromApi(Urls.team_create(battle.id))}
              role="button"
            >
              Create your team
            </a>
          ) : (
            <CardTeam pokemons={current.pokemons} />
          )}
        </div>
        <div>
          <p className="text_trainer">Opposing pokemons</p>
          {other === null ? 'No pokemons' : <CardTeam pokemons={other.pokemons} />}
        </div>
      </div>
    </div>
  );
}

export default BattleDetail;
