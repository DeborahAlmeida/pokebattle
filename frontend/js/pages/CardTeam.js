import React from 'react';

import CardPokemon from 'pages/CardPokemon';

function CardTeam(props) {
  return (
    <div className="content_card">
      <CardPokemon pokemon={props.pokemons[0]} />
      <CardPokemon pokemon={props.pokemons[1]} />
      <CardPokemon pokemon={props.pokemons[2]} />
    </div>
  );
}
export default CardTeam;
