<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>ReserveMe Reservation System</h1>
        <hr />
        <br /><br />
        <alert :message="message" :alertvariant="alertvariant" v-if="showMessage"></alert>

        <b-button-group>
          <button
            type="button"
            class="btn btn-success"
            v-b-modal.login-modal
            style="position: relative; top: 0px; left: 600px"
            v-if="!ifSignIn_user && !ifSignIn_admin"
          >
            Login
          </button>

          <button
            type="button"
            class="btn btn-primary"
            v-b-modal.signup-modal
            v-if="!ifSignIn_user && !ifSignIn_admin"
            style="position: relative; top: 0px; left: 600px"
          >
            Signup
          </button>
        </b-button-group>
        <button
          type="button"
          class="btn btn-success"
          v-if="ifSignIn_admin"
          @click="addRsv"
          v-b-modal.addrsv-modal
          style="position: relative; top: 0px; left: 15px"

        >
          Add Event
        </button>
        <b-button-group>
          <button
            type="button"
            class="btn btn-primary"
            v-if="ifSignIn_user || ifSignIn_admin"
            @click="logout"
            style="position: relative; top: 0px; left: 600px"
          >
            Logout
          </button>
          <button
            type="button"
            class="btn btn-success"
            v-b-modal.resetpassword-modal
            v-if="ifSignIn_user || ifSignIn_admin"
            style="position: relative; top: 0px; left: 600px"
          >
            Change Password
          </button>
        </b-button-group>
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
              <td>{{ rsv.num_now }}/{{ rsv.num_limit }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    v-if="ifSignIn_admin"
                    @click="deleteRsv(rsv.rsv_uuid)"
                  >
                    Delete
                  </button>
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-if="ifSignIn_admin"
                    @click="passModifyArg(rsv.rsv_uuid)"
                    v-b-modal.modifyrsv-modal
                  >
                    Modify
                  </button>
                  <button
                    type="button"
                    class="btn btn-primary btn-sm"
                    v-if="ifSignIn_admin"
                    @click="Get_Member(rsv.rsv_uuid)"
                    v-b-modal.listmember-modal
                  >
                    List
                  </button>
                  <button
                    type="button"
                    class="btn btn-success btn-sm"
                    v-if="ifSignIn_user && !user_data.selected_uuid"
                    @click="seclectRsv(rsv.rsv_uuid)"
                  >
                    Select
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    v-if="ifSignIn_user && rsv.rsv_uuid == user_data.selected_uuid"
                    @click="cancleRsv(rsv.rsv_uuid)"
                  >
                    Cancle
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
            type="email"
            v-model="LoginForm.email"
            required
            placeholder="Your Email"
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
            type="password"
            v-model="LoginForm.password"
            required
            placeholder="Your Password"
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
      title="User Signup"
      hide-footer
    >
      <b-form @submit="onSignup" @reset="onReset" class="w-100">
        <b-form-group
          id="form-username-group"
          label="Username:"
          label-for="form-username-input"
        >
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="SignUpForm.username"
            required
            placeholder="Enter Username"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-email-group"
          label="Email:"
          label-for="form-email-input"
        >
          <b-form-input
            id="form-email-input"
            type="email"
            v-model="SignUpForm.email"
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
            type="password"
            v-model="SignUpForm.password"
            required
            placeholder="Enter Password"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-pw-group"
          label="Check password:"
          label-for="form-chpw-input"
        >
          <b-form-input
            id="form-chpw-input"
            type="password"
            v-model="SignUpForm.checkpassword"
            required
            placeholder="Check Password"
          >
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Signup</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal
      ref="ResetPasswordModal"
      id="resetpassword-modal"
      title="Reset Password"
      hide-footer
    >
      <b-form @submit="onResetPassword" @reset="onReset" class="w-100">
        <b-form-group
          id="form-pw-group"
          label="OldPassword:"
          label-for="form-pw-input"
        >
          <b-form-input
            id="form-pw-input"
            type="password"
            v-model="ResetPasswordForm.oldpassword"
            required
            placeholder="Enter Your Old Password"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-newpw-group"
          label="NewPassword:"
          label-for="form-newpw-input"
        >
          <b-form-input
            id="form-newpw-input"
            type="password"
            v-model="ResetPasswordForm.newpassword"
            required
            placeholder="Enter Your New Password"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-rchpw-group"
          label="Check password:"
          label-for="form-rchpw-input"
        >
          <b-form-input
            id="form-rchpw-input"
            type="password"
            v-model="ResetPasswordForm.checkpassword"
            required
            placeholder="Check Password"
          >
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Confirm</b-button>
          <b-button type="reset" variant="danger">Cancle</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal
      ref="AddRSVModal"
      id="addrsv-modal"
      title="Add Reservation"
      hide-footer
    >
      <b-form @submit="addRsv" @reset="onReset" class="w-100">
        <b-form-group
          id="form-rsvname-group"
          label="Reservation name:"
          label-for="form-rsvname-input"
        >
          <b-form-input
            id="form-rsvname-input"
            type="text"
            v-model="RSVForm.rsvname"
            required
            placeholder="Enter reservation name"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-num-group"
          label="Number Limit:"
          label-for="form-num-input"
        >
          <b-form-input
            autocomplete="off"
            id="form-num-input"
            type="number"
            min="1"
            value="10"
            max="100"
            step="1"
            v-model="RSVForm.num"
            required
            placeholder="Enter num"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-time-group"
          label="Date&Time:"
          label-for="form-time-input"
        >
          <b-form-timepicker
            v-model="RSVForm.time"
            hourCycle="h23"
            v-validate="'required'"
          ></b-form-timepicker>
          <p>{{ RSVForm.time }}</p>
          <b-form-datepicker
            v-model="RSVForm.date"
            v-validate="'required'"
          ></b-form-datepicker>
          <p>{{ RSVForm.date }}</p>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Confirm</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal
      ref="ModifyRSVModal"
      id="modifyrsv-modal"
      title="Modify Reservation"
      hide-footer
    >
      <b-form @submit="modifyRsv" @reset="onReset" class="w-100">
        <b-form-group
          id="form-rsvname-group"
          label="RSVname:"
          label-for="form-rsvname-input"
        >
          <b-form-input
            id="form-rsvname-input"
            type="text"
            v-model="RSVForm.rsvname"
            placeholder="Enter Event name"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-num-group"
          label="num:"
          label-for="form-num-input"
        >
          <b-form-input
            autocomplete="off"
            id="form-num-input"
            type="number"
            min="1"
            value="10"
            max="100"
            step="1"
            v-model="RSVForm.num"
            placeholder="Enter num limit"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-time-group"
          label="Time:"
          label-for="form-time-input"
        >
          <b-form-timepicker
            v-model="RSVForm.time"
            hourCycle="h23"
          ></b-form-timepicker>
          <b-form-datepicker v-model="RSVForm.date"></b-form-datepicker>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Confirm</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal
      ref="ListMemberModal"
      id="listmember-modal"
      title="Members seclected this reservation"
      scrollable
      hide-footer
    >
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">UserName</th>
            <th scope="col">email</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(member, index) in members" :key="index">
            <td>{{ member.username }}</td>
            <td>{{ member.email }}</td>
          </tr>
        </tbody>
      </table>
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
      members: [],
      user_data: {
        access_token: '',
        refresh_token: '',
        selected_uuid: '',
      },
      user_email: '',
      modify_uuid: '',
      LoginForm: {
        email: '',
        password: '',
      },
      SignUpForm: {
        username: '',
        email: '',
        password: '',
        checkpassword: '',
      },
      RSVForm: {
        rsvname: '',
        num: 0,
        date: '',
        time: '',
      },
      ResetPasswordForm: {
        oldpassword: '',
        newpassword: '',
        checkpassword: '',
      },
      message: '',
      alertvariant: '',
      showMessage: false,
      ifSignIn_user: false,
      ifSignIn_admin: false,
      show_select_button: true,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    get_list() {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/get_rsv_list`;
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
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/login`;
      axios.post(path, payload).then((res) => {
        this.user_data = res.data;
        this.user_email = payload.email;
        this.alertvariant = 'success';
        this.message = `Hi, ${this.user_data.username}!`;
        this.showMessage = true;
        if (res.data.is_admin === true) {
          this.ifSignIn_admin = true;
        } else {
          this.ifSignIn_user = true;
        }
        this.get_list();
      });
      if (this.user_email === '') {
        this.alertvariant = 'danger';
        this.message = 'Email or Password incorret';
        this.showMessage = true;
      }
    },
    logout() {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/logout`;
      const token = this.user_data.access_token;
      const payload = {
        refresh_token: this.user_data.refresh_token,
      };
      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then((res) => {
          if (res.status === 200) {
            this.user_data = '';
            this.rsvs = '';
            this.user_email = '';
            this.alertvariant = 'success';
            this.message = 'Successfuly logged out!';
            this.showMessage = true;
          } else {
            this.message = 'Log out failed.';
            this.showMessage = true;
          }
          this.ifSignIn_user = false;
          this.ifSignIn_admin = false;
        });
    },
    SignUp(payload) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/signup`;
      axios.post(path, payload).then(() => {
        this.alertvariant = 'success';
        this.message = 'Successfully signed up!';
        this.showMessage = true;
      });
    },
    Get_Member(uuid) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/get_member_list`;
      const token = this.user_data.access_token;
      const payload = {
        rsv_uuid: uuid,
      };
      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then((res) => {
          this.members = res.data;
        });
    },
    initForm() {
      this.LoginForm.email = '';
      this.LoginForm.password = '';
      this.SignUpForm.username = '';
      this.SignUpForm.email = '';
      this.SignUpForm.password = '';
      this.SignUpForm.checkpassword = '';
      this.RSVForm.rsvname = '';
      this.RSVForm.num = '';
      this.RSVForm.time = '';
      this.RSVForm.date = '';
      this.ResetPasswordForm.oldpassword = '';
      this.ResetPasswordForm.newpassword = '';
      this.ResetPasswordForm.checkpassword = '';
      this.ResetPasswordForm.email = '';
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
      this.initForm();
      evt.preventDefault();
      this.$refs.LoginModal.hide();
      this.$refs.SignUpModal.hide();
      this.$refs.AddRSVModal.hide();
      this.$refs.onResetPassword.hide();
    },
    onSignup(evt) {
      evt.preventDefault();
      this.$refs.SignUpModal.hide();
      if (this.SignUpForm.password === this.SignUpForm.checkpassword) {
        const payload = {
          username: this.SignUpForm.username,
          email: this.SignUpForm.email,
          password: this.SignUpForm.password,
        };
        this.SignUp(payload);
        this.initForm();
      } else {
        this.alertvariant = 'warning';
        this.message = 'Passwords not matched, please try again';
        this.showMessage = true;
        this.onReset();
      }
    },
    addRsv(evt) {
      evt.preventDefault();
      this.$refs.AddRSVModal.hide();
      const payload = {
        rsv_name: this.RSVForm.rsvname,
        num_limit: this.RSVForm.num,
        due_date: this.RSVForm.date + this.RSVForm.time,
      };
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/add_srv`;
      const token = this.user_data.access_token;

      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then(() => {
          this.alertvariant = 'success';
          this.message = 'Successfully added event!';
          this.showMessage = true;
          this.get_list();
        });
      this.initForm();
    },
    passModifyArg(uuid) {
      this.modify_uuid = uuid;
    },
    modifyRsv(evt) {
      evt.preventDefault();
      this.$refs.ModifyRSVModal.hide();
      const payload = {
        rsv_uuid: this.modify_uuid,
        rsv_name: this.RSVForm.rsvname,
        num_limit: this.RSVForm.num,
        due_date: this.RSVForm.date + this.RSVForm.time,
      };

      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/modify_rsv`;
      const token = this.user_data.access_token;

      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then(() => {
          this.alertvariant = 'success';
          this.message = 'Successfully modified!';
          this.showMessage = true;
          this.get_list();
        });
      this.initForm();
    },
    deleteRsv(uuid) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/delete_rsv`;
      const token = this.user_data.access_token;
      const payload = {
        rsv_uuid: uuid,
      };
      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then(() => {
          this.alertvariant = 'success';
          this.message = 'Successfully deleted!';
          this.showMessage = true;
          this.get_list();
        });
    },
    cancleRsv(uuid) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/user_cancle_rsv`;
      const token = this.user_data.access_token;
      const payload = {
        rsv_uuid: uuid,
        email: this.user_email,
      };
      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then(() => {
          this.alertvariant = 'success';
          this.message = 'successfully cancled!';
          this.show_select_button = true;
          this.showMessage = true;
          this.user_data.selected_uuid = '';
          this.get_list();
        });
    },
    seclectRsv(uuid) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/user_make_rsv`;
      const token = this.user_data.access_token;
      if (this.selected_uuid) {
        this.alertvariant = 'warning';
        this.message = 'You can reserve only one event at once, please cancle first';
        this.showMessage = true;
      } else {
        const payload = {
          rsv_uuid: uuid,
          email: this.user_email,
        };
        axios
          .post(path, payload, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token} `,
            },
          })
          .then(() => {
            this.alertvariant = 'success';
            this.message = 'successfully seclected!';
            this.showMessage = true;
            this.user_data.selected_uuid = uuid;
            this.show_select_button = false;
            this.get_list();
          });
      }
    },
    onResetPassword(evt) {
      evt.preventDefault();
      this.$refs.ResetPasswordModal.hide();
      if (
        this.ResetPasswordForm.newpassword === this.ResetPasswordForm.checkpassword
      ) {
        const payload = {
          old_pass: this.ResetPasswordForm.oldpassword,
          new_pass: this.ResetPasswordForm.newpassword,
          email: this.user_email,
        };
        this.ResetPassword(payload);
        this.initForm();
      } else {
        this.alertvariant = 'warning';
        this.message = 'Passwords not matched, please try again';
        this.showMessage = true;
        this.onReset();
      }
    },
    ResetPassword(payload) {
      const path = `${process.env.VUE_APP_BACK_END_HOST}/api/reset_pw`;
      const token = this.user_data.access_token;
      axios
        .post(path, payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token} `,
          },
        })
        .then((res) => {
          if (res.data.status === 'password changed.') {
            this.alertvariant = 'success';
            this.message = 'Your password has changed!';
            this.showMessage = true;
          } else {
            this.alertvariant = 'warning';
            this.message = 'Password incorrect';
            this.showMessage = true;
          }
        });
    },
  },
  created() {},
};
</script>
