import { Formik, Field, Form } from 'formik';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { createBattleAction } from '../actions/createBattle';
import { getCurrentUser } from '../actions/getUser';

function BattleCreate(props) {
  const { user, errorMessage } = props;

  const validate = (value) => {
    let error = null;
    if (!value) {
      error = 'You need to choose an opponent';
    } else if (value === user.email) {
      error = 'You cannot choose yourself';
    } else if (!/^[\w%+.-]+@[\d.a-z-]+\.[a-z]{2,4}$/i.test(value)) {
      error = 'Invalid email address';
    }
    return error;
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
            creator: user.id,
            opponent: '',
          }}
          onSubmit={async (values) => {
            props.createBattleAction(values);
          }}
        >
          {({ errors, touched }) => (
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
                  validate={validate}
                />
                {errors.opponent && touched.opponent && <div>{errors.opponent}</div>}
                {errorMessage ? <p className="error_message_v2">{errorMessage.detail}</p> : null}
                <button className="button_next" type="submit">
                  Next
                </button>
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
