import React from 'react';

import CardPokemon from 'components/CardPokemon';

function CardTeam({ pokemons }) {
  return (
    <div className="content_card">
      {pokemons.map((pokemon) => {
        return <CardPokemon key={pokemon.pokemon.name} pokemon={pokemon} />;
      })}
    </div>
  );
}
export default CardTeam;
