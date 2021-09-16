import _ from 'lodash';
import React from 'react';

function CardPokemon({ pokemon }) {
  const pokemonSpecifics = _.get(pokemon, 'pokemon', null);
  return (
    <div className="card_pokemon">
      {pokemonSpecifics.name ? (
        <>
          {' '}
          <img
            alt="pokemon"
            className="img_pokemon_card"
            src={pokemonSpecifics.img_url ? pokemonSpecifics.img_url : pokemonSpecifics.imgUrl}
          />
          <p>{pokemonSpecifics.name}</p>
          <div className="base_stats">
            <div className="base_stats_title">
              <p>Attack</p>
              <p>{pokemonSpecifics.attack}</p>
            </div>
            <div className="base_stats_title">
              <p>Defense</p>
              <p>{pokemonSpecifics.defense}</p>
            </div>
            <div className="base_stats_title">
              <p>HP</p>
              <p>{pokemonSpecifics.hp}</p>
            </div>
          </div>
        </>
      ) : (
        <p className="text_pkn">Pokemon missing</p>
      )}
    </div>
  );
}
export default CardPokemon;
