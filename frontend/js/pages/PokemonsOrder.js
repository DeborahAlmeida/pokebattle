import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

function PokemonsOrder(props) {
  console.log('>>>> props', props);
  return <div className="battle_container_detail">hello</div>;
}
const mapStateToProps = (store) => ({
  user: store.user.user,
  pokemons: _.get(store, 'pokemons.pokemons', null),
});

export default connect(mapStateToProps)(PokemonsOrder);
