import { Formik, Field, Form } from 'formik';
import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { SortableContainer, SortableElement, arrayMove } from 'react-sortable-hoc';

import { changePokemonsIndex, createTeamAction } from '../actions/createTeam';
import { getCurrentUser } from '../actions/getUser';
import CardPokemon from '../components/CardPokemon';
import { getPokemonFromApi } from '../utils/api';

const SortableItem = SortableElement(({ value }) => <CardPokemon pokemon={value} />);

const SortableList = SortableContainer(({ items }) => {
  console.log('>>>>>>> vlores', items);
  const pokemonsValues = Object.values(items);
  return (
    <div className="card_select">
      {pokemonsValues.map((value, index) => (
        <SortableItem key={value.name} index={index} value={value} />
      ))}
    </div>
  );
});

function TeamCreate(props) {
  const { user, pokemons } = props;

  const onSortEnd = ({ oldIndex, newIndex }) => {
    const data = { oldIndex, newIndex, pokemons };
    props.changePokemonsIndex(data);
  };
  const validate = (value) => {
    let error = null;
    return getPokemonFromApi(value)
      .then(() => {
        return error;
      })
      .catch((response) => {
        if (!value) {
          error = 'This field is required';
        } else if (response.response.status === 404) {
          error = 'This pokemon name is invalid';
        }
        return error;
      });
  };
  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
  }, []);

  if (user) {
    return (
      <div className="battle_container_detail">
        <Formik
          initialValues={{
            pokemon1: '',
            pokemon2: '',
            pokemon3: '',
          }}
          onSubmit={async (values) => {
            props.createTeamAction(values);
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <div className="div_trainer">
                <p className="title_battle">Trainer</p>
                <p className="subtitle_battle">Choose your pokemons!</p>
                <div className="input_pokemon">
                  <div className="pokemon_container">
                    <p>Pokemon 1:</p>
                    <Field
                      className="input_pokemon_1_v2"
                      id="pokemon1"
                      name="pokemon1"
                      placeholder="pikachu"
                      type="text"
                      validate={validate}
                    />
                  </div>
                  <div className="error_msg">
                    {errors.pokemon1 && touched.pokemon1 && <div>{errors.pokemon1}</div>}
                  </div>
                </div>
                <div className="input_pokemon">
                  <div className="pokemon_container">
                    <p>Pokemon 2:</p>
                    <Field
                      className="input_pokemon_2_v2"
                      id="pokemon2"
                      name="pokemon2"
                      placeholder="beedrill"
                      type="text"
                      validate={validate}
                    />
                  </div>
                  <div className="error_msg">
                    {errors.pokemon2 && touched.pokemon2 && <div>{errors.pokemon2}</div>}
                  </div>
                </div>
                <div className="input_pokemon">
                  <div className="pokemon_container">
                    <p>Pokemon 3:</p>
                    <Field
                      className="input_pokemon_3_v2"
                      id="pokemon3"
                      name="pokemon3"
                      placeholder="bulbasaur"
                      type="text"
                      validate={validate}
                    />
                  </div>
                  <div className="error_msg">
                    {errors.pokemon3 && touched.pokemon3 && <div>{errors.pokemon3}</div>}
                  </div>
                </div>
                <button className="button_next" type="submit">
                  Next
                </button>
                {pokemons ? <SortableList items={pokemons} onSortEnd={onSortEnd} /> : null}
                <div />
              </div>
            </Form>
          )}
        </Formik>
      </div>
    );
  }
  return 'loading';
}

const mapStateToProps = (store) => ({
  user: _.get(store, 'user.user', null),
  pokemons: _.get(store, 'pokemons.pokemons', null),
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    createTeamAction: (pokemons) => dispatch(createTeamAction(pokemons)),
    changePokemonsIndex: (oldIndex, newIndex, pokemons) =>
      dispatch(changePokemonsIndex(oldIndex, newIndex, pokemons)),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(TeamCreate);
