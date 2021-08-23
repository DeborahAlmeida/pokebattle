import React from 'react';

import CardPokemon from 'components/CardPokemon';

function CardTeam({ pokemons }) {
  return (
    <div className="content_card">
      <CardPokemon pokemon={pokemons[0]} />
      <CardPokemon pokemon={pokemons[1]} />
      <CardPokemon pokemon={pokemons[2]} />
    </div>
  );
}
export default CardTeam;
