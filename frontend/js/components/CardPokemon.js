import React from 'react';

function CardPokemon({ pokemon }) {
  return (
    <div className="card_pokemon">
      <img alt="pokemon" className="img_pokemon_card" src={pokemon.img_url} />
      <p>{pokemon.name}</p>
      <div className="base_stats">
        <div className="base_stats_title">
          <p>Attack</p>
          <p>{pokemon.attack}</p>
        </div>
        <div className="base_stats_title">
          <p>Defense</p>
          <p>{pokemon.defense}</p>
        </div>
        <div className="base_stats_title">
          <p>HP</p>
          <p>{pokemon.hp}</p>
        </div>
      </div>
    </div>
  );
}
export default CardPokemon;
