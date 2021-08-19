import React, { useState, useEffect } from 'react';
 
import CardPokemon from 'pages/CardPokemon.js';

// {{pokemons_creator.pokemon_1.img_url}}

function CardTeam(props){
    return (
        <div className="content_card">
            <CardPokemon pokemon={props.pokemons[0]}/>
            <CardPokemon pokemon={props.pokemons[1]}/>
            <CardPokemon pokemon={props.pokemons[2]}/>
        </div>
    );
}
export default CardTeam;
