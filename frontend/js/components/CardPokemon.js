import React from 'react';

function CardPokemon({ pokemon }) {
  console.log("chegando no card", pokemon)
  return (
    <div className="card_pokemon">
      <img alt="pokemon" className="img_pokemon_card" src={pokemon.img_url ? pokemon.img_url : pokemon.imgUrl} />
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
