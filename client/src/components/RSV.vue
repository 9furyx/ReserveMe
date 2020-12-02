<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>ReserveMe Reservation System</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <b-button-group>
          <button
            type="button"
            class="btn btn-success btn-sm"
            v-b-modal.login-modal
            style="position:relative;top:-140px;left:900px"
            v-if="!ifSignIn_user && !ifSignIn_admin"
          >
            Login
          </button>
          <button
            type="button"
            class="btn btn-primary"
            v-b-modal.signup-modal
            v-if="!ifSignIn_user && !ifSignIn_admin"
            style="position:relative;top:-140px;left:900px"
          >
            SignUp
          </button>
        </b-button-group>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-if="ifSignIn_user"
          @click="onReserve"
        >
          make reservation
        </button>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-if="ifSignIn_admin"
          @click="onReserve"
        >
          add reservation
        </button>
        <button
          type="button"
          class="btn btn-primary"
          v-if="ifSignIn_user || ifSignIn_admin"
          @click="logOut"
          style="position:relative;top:-140px;left:900px"
        >
          log out
        </button>
        <br /><br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Date</th>
              <th scope="col">Num</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(rsv, index) in rsvs" :key="index">
              <td>{{ rsv.rsv_name }}</td>
              <td>{{ rsv.due_date }}</td>
              <td>{{ rsv.num_limit }}/{{ rsv.num_now }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="cancleRsv"
                  >
                    Cancle
                  </button>
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-if="ifSignIn_admin"
                    @click="modifyRsv"
                  >
                    modify reservation
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="LoginModal" id="login-modal" title="User Login" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-email-group"
          label="Email:"
          label-for="form-email-input"
        >
          <b-form-input
            id="form-email-input"
            type="text"
            v-model="LoginForm.email"
            required
            placeholder="Enter Email"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-pw-group"
          label="Password:"
          label-for="form-pw-input"
        >
          <b-form-input
            id="form-pw-input"
            type="text"
            v-model="LoginForm.password"
            required
            placeholder="Enter Password"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-login-group"> </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Login</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal
      ref="SignUpModal"
      id="signup-modal"
      title="User signup"
      hide-footer
    >
      <b-form @submit="onSignup" @reset="onReset" class="w-100">
        <b-form-group
          id="form-email-group"
          label="Email:"
          label-for="form-email-input"
        >
          <b-form-input
            id="form-email-input"
            type="text"
            v-model="LoginForm.email"
            required
            placeholder="Enter Email"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-pw-group"
          label="Password:"
          label-for="form-pw-input"
        >
          <b-form-input
            id="form-pw-input"
            type="text"
            v-model="LoginForm.password"
            required
            placeholder="Enter Password"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-login-group"> </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Signup</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      rsvs: [],
      user_data: {
        access_token: '',
        refresh_token: '',
        selected_uuid: '',
      },
      LoginForm: {
        email: '',
        password: '',
      },
      message: 'Hi!',
      showMessage: false,
      ifSignIn_user: false,
      ifSignIn_admin: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    get_list() {
      const path = 'http://localhost:5000/get_rsv_list';
      const token = this.user_data.access_token;
      axios
        .get(path, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then((res) => {
          this.rsvs = res.data;
        });
    },
    login(payload) {
      const path = 'http://localhost:5000/login';
      axios.post(path, payload).then((res) => {
        this.user_data = res.data;
        this.message = 'Successfully logged in!';
        this.showMessage = true;
        if (res.is_admin === true) {
          // I am not sure if it is right
          this.ifSignIn_admin = true;
        } else {
          this.ifSignIn_user = true;
        }
        this.get_list();
      });
    },
    SignUp(payload) {
      const path = 'http://localhost:5000/signup'; // check if it is correct
      axios.post(path, payload).then((res) => {
        this.user_data = res.data;
        this.message = 'Successfully signed up!';
        this.showMessage = true;
        this.get_list();
      });
    },

    initForm() {
      this.LoginForm.email = '';
      this.LoginForm.password = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.LoginModal.hide();
      const payload = {
        email: this.LoginForm.email,
        password: this.LoginForm.password,
      };
      this.login(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.LoginModal.hide();
      this.initForm();
    },
    onSignup(evt) {
      evt.preventDefault();
      this.$refs.SignUpModal.hide();
      const payload = {
        email: this.LoginForm.email,
        // I used the same form
        password: this.LoginForm.password,
      };
      this.SignUp(payload);
      this.initForm();
    },
    logOut() {
      this.ifSignIn_user = false;
      this.ifSignIn_user = false;
    },
    addRsv() {

    },
    // you can choose to add these functions
    cancleRsv() {

    },
    modifyRsv() {

    },
  },
  created() {},
};
</script>
