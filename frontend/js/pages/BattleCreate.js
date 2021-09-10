import { Formik, Field, Form } from 'formik';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { createBattleAction } from '../actions/createBattle';
import { getCurrentUser } from '../actions/getUser';

function BattleCreate(props) {
  const { user, errorMessage } = props;

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
            creator: user.id,
            opponent: '',
          }}
          onSubmit={async (values) => {
            props.createBattleAction(values);
          }}
        >
          <Form>
            <div className="div_trainer">
              <p className="title_battle">Trainer</p>
              <p className="subtitle_battle">Choose your opponent!</p>
              <Field
                className="input_opponent_v2"
                id="opponent"
                name="opponent"
                placeholder="opponent@gmail.com"
                type="email"
              />
              {errorMessage ? <p className="error_message_v2">{errorMessage.detail}</p> : null}
              <button className="button_next" type="submit">
                Next
              </button>
            </div>
          </Form>
        </Formik>
      </div>
    );
  }
  return 'loading';
}

const mapStateToProps = (store) => ({
  user: store.user.user,
  battle: store.battle.battle,
  errorMessage: store.battle.errorMessage,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    createBattleAction: (form) => dispatch(createBattleAction(form)),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate);
