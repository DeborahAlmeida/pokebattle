import { Formik, Field, Form } from 'formik';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { getCurrentUser } from '../actions/getUser';
import { createBattle } from '../utils/api';

function BattleCreate(props) {
  const { user } = props;

  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
  }, []);

  if (user) {
    return (
      <div className="battle_container_detail">
        <h2>Trainer</h2>
        <h4>Choose your opponent!</h4>
        <Formik
          initialValues={{
            creator: user.id,
            opponent: '',
          }}
          onSubmit={async (values) => {
            await createBattle(values);
          }}
        >
          <Form>
            <p>Opponent:</p>
            <Field id="opponent" name="opponent" placeholder="opponent@gmail.com" type="email" />
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    );
  }
  return 'loading';
}

const mapStateToProps = (store) => ({
  user: store.user.user,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate);
