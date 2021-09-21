import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams, Link } from 'react-router-dom';

function CardDetailFromAPI(props) {
  console.log('>>>>>>>', props);

  return (
    <>
      <h2 className="subtitle_detail">Creator:</h2>
      <h2 className="subtitle_detail">Opponent:</h2>
    </>
  );
}

// function mapStateToProps(store) {
//   const battle = _.get(store, 'battle.battleDetail', null);
//   const user = _.get(store, 'user.data', null);

//   return {
//     battle,
//     user,
//   };
// }

export default CardDetailFromAPI;
