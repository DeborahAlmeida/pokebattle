import { Formik, Field, Form } from 'formik';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { createBattleAction } from '../actions/createBattle';
import { getCurrentUser } from '../actions/getUser';
import { createBattle } from '../utils/api';

// function validateEmail(value) {
//   let error;
//   console.log('>>>>', value);
//   if (!value) {
//     error = 'This field is required';
//   } else if (!/^[\w%+.-]+@[\d.a-z-]+\.[a-z]{2,4}$/i.test(value)) {
//     error = 'Invalid email address';
//   }
//   return error;
// }

function BattleCreate(props) {
  const { user } = props;
  console.log('props:', props);
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
            console.log('ta no submit');
            props.createBattleAction(values);
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <p>Opponent:</p>
              <Field
                id="opponent"
                name="opponent"
                placeholder="opponent@gmail.com"
                type="email"
                // validate={validateEmail}
              />
              {/* {errors.opponent && touched.opponent && <div>{errors.opponent}</div>} */}
              <button type="submit">Submit</button>
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
  battle: store.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    createBattleAction: (battle) => dispatch(createBattleAction(battle)),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate);
