import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams, Link } from 'react-router-dom';

import CardTeam from 'components/CardTeam';

import { getBattle } from '../actions/getBattle';
import { getCurrentUser } from '../actions/getUser';
import { orderTeamsByCurrentUser } from '../utils/battle-detail';
import { denormalizeBattleData } from '../utils/denormalize';
import Urls from '../utils/urls';

function BattleDetail(props) {
  const { id } = useParams();
  const { battle, battles, user } = props;
  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
  }, []);

  useEffect(() => {
    if (!battles) {
      props.getBattle(id);
    }
  }, []);

  if (!battle && !battles) {
    return 'loading';
  }
  const denormalizedData = denormalizeBattleData(id, battles, battle);
  const { current, other } = orderTeamsByCurrentUser(denormalizedData, user);

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">
        Creator: {denormalizedData.creator ? denormalizedData.creator.email : ''}
      </h2>
      <h2 className="subtitle_detail">
        Opponent: {denormalizedData.opponent ? denormalizedData.opponent.email : ''}
      </h2>
      {denormalizedData.winner ? (
        <>
          <img
            alt="trofeu"
            className="img_detail_winner"
            src="https://image.flaticon.com/icons/png/512/2119/2119019.png"
          />
          <h2 className="subtitle_detail">
            The winner is {denormalizedData.winner ? denormalizedData.winner.email : ''}
          </h2>
        </>
      ) : (
        ''
      )}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {current === null ? (
            <Link className="button_battle button_battle_detail" to={Urls.team_create(id)}>
              Create your team
            </Link>
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

function mapStateToProps(store) {
  const battle = _.get(store, 'battle.battleDetail', null);
  const user = _.get(store, 'user.data', null);

  return {
    battle,
    user,
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattle: (battle) => dispatch(getBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
