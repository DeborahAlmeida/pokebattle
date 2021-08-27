import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { getBattleList } from '../actions/getBattleList';
import { getCurrentUser } from '../actions/getUser';
import Urls from '../utils/urls';

function BattleList(props) {
  const { user } = props.user;
  const { battles } = props.battles;

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
                <a className="battle_settled" href={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </a>
              </li>
            ) : null
          )}
        </div>

        <div className="your_opponent">
          <h3>On goind Battles</h3>
          {battles.map((battle) =>
            !battle.winner ? (
              <li key={battle.id} className="item">
                <a className="battle_ongoing" href={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </a>
              </li>
            ) : null
          )}
        </div>
      </ul>
    </div>
  );
}

const mapStateToProps = (store) => ({
  battles: store.battle,
  user: store.user,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattleList: () => dispatch(getBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
