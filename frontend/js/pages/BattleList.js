import { denormalize } from 'normalizr';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getBattleList } from '../actions/getBattleList';
import { getCurrentUser } from '../actions/getUser';
import { battlesSchema } from '../utils/schema';
import Urls from '../utils/urls';

function BattleList(props) {
  const { user, battles } = props;

  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
    props.getBattleList();
  }, []);
  if (!battles) {
    return (
      <div className="battle_container_detail">
        <h1>Your Battles</h1>
        {!user ? (
          <h2 className="subtitle">You need to be logged {user}</h2>
        ) : (
          <h2 className="subtitle">There are no battle in the database.</h2>
        )}
      </div>
    );
  }

  return (
    <div className="battle_container_detail">
      <h1>Your Battles</h1>
      {!user ? (
        <h2 className="subtitle">You need to be logged</h2>
      ) : (
        <h2 className="subtitle">Click to see more information</h2>
      )}
      <ul className="list_battle">
        <div className="settled">
          <h3>Settled battles</h3>
          {battles.map((battle) =>
            battle.winner ? (
              <li key={battle.id} className="item">
                <Link className="battle_settled" to={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </Link>
              </li>
            ) : null
          )}
        </div>

        <div className="your_opponent">
          <h3>On goind Battles</h3>
          {battles.map((battle) =>
            !battle.winner ? (
              <li key={battle.id} className="item">
                <Link className="battle_ongoing" to={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </Link>
              </li>
            ) : null
          )}
        </div>
      </ul>
    </div>
  );
}

function mapStateToProps(store) {
  let battles = null;
  if (store.battle.battles) {
    battles = denormalize(
      store.battle.battles.result,
      battlesSchema,
      store.battle.battles.entities
    );
  }
  return {
    battles,
    user: store.user.user,
  };
}
const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattleList: () => dispatch(getBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
