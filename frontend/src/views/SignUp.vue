<template>
  <h1 class="page-head">User Sign Up</h1>
  <form class="register-form" @submit.prevent="register_user">
    <div class="radio-input">
      <label>
        <input
          type="radio"
          id="customer"
          name="role"
          value="customer"
          v-model="role"
        />
        <span>Customer</span>
      </label>
      <label>
        <input
          type="radio"
          id="professional"
          name="role"
          value="professional"
          v-model="role"
        />
        <span>Service Professional</span>
      </label>
      <span class="selection"></span>
    </div>
    <div class="input-container">
      <p class="input-err-msg" v-if="!username_valid">
        * {{ username_errmsg }}
      </p>
      <input
        placeholder="Username"
        class="input-field"
        type="text"
        name="username"
        v-model="username"
      />
      <label for="input-field" class="input-label">Username</label>
      <span
        class="input-highlight"
        :class="{ 'input-highlight-red': !username_valid }"
      ></span>
    </div>
    <div class="input-container">
      <p class="input-err-msg" v-if="!email_add_valid">
        * {{ email_add_errmsg }}
      </p>
      <input
        placeholder="Email Address"
        class="input-field"
        name="email_address"
        type="text"
        v-model="email_add"
      />
      <label for="input-field" class="input-label">Email Address</label>
      <span
        class="input-highlight"
        :class="{ 'input-highlight-red': !email_add_valid }"
      ></span>
    </div>
    <div class="input-container">
      <p class="input-err-msg" v-if="!password_valid">
        * {{ password_errmsg }}
      </p>
      <input
        placeholder="Password"
        class="input-field"
        name="password"
        type="password"
        v-model="password"
      />
      <label for="input-field" class="input-label">Password</label>
      <span
        class="input-highlight"
        :class="{ 'input-highlight-red': !password_valid }"
      ></span>
    </div>
    <div class="input-container">
      <p class="input-err-msg" v-if="!confirm_passwd_valid">
        * {{ confirm_passwd_errmsg }}
      </p>
      <input
        placeholder="Confirm Password"
        class="input-field"
        type="password"
        v-model="confirm_passwd"
      />
      <label for="input-field" class="input-label">Confirm Password</label>
      <span
        class="input-highlight"
        :class="{ 'input-highlight-red': !confirm_passwd_valid }"
      ></span>
    </div>
    <button class="register-button">Register</button>
    <p class="end-formline">
      Already have an account?<RouterLink :to="{ name: 'login' }">
        Login here</RouterLink
      >
    </p>
  </form>
</template>

<script setup>
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";
import { useUserStore } from "../stores/userstore";
import { useNotifStore } from "../stores/notificationstore";
import { login_user } from "../composables/loginuser";

const username = ref("");
const email_add = ref("");
const password = ref("");
const confirm_passwd = ref("");
const role = ref("customer");
const username_errmsg = ref(null);
const email_add_errmsg = ref(null);
const password_errmsg = ref(null);
const confirm_passwd_errmsg = ref(null);

const username_valid = computed(() => {
  const regex = /^[a-z][a-zA-Z0-9_]+$/;
  if (username.value && username.value.length < 5) {
    username_errmsg.value = "Username too small";
    return false;
  }
  if (username.value && username.value.length > 16) {
    username_errmsg.value = "Username too large";
    return false;
  }
  if (username.value && !regex.test(username.value)) {
    username_errmsg.value = "Username contains invalid characters";
    return false;
  }
  username_errmsg.value = null;
  return true;
});

const email_add_valid = computed(() => {
  const regex = /^[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z0-9_]+\.[a-zA-Z]{2,}$/;
  if (email_add.value && !regex.test(email_add.value)) {
    email_add_errmsg.value = "Invalid Email Address";
    return false;
  }
  email_add_errmsg.value = null;
  return true;
});

const password_valid = computed(() => {
  if (password.value && password.value.length < 8) {
    password_errmsg.value = "Password length too small";
    return false;
  }
  password_errmsg.value = null;
  return true;
});

const confirm_passwd_valid = computed(() => {
  if (confirm_passwd.value && confirm_passwd.value !== password.value) {
    confirm_passwd_errmsg.value = "Confirm Password does not match Password";
    return false;
  }
  confirm_passwd_errmsg.value = null;
  return true;
});

const userStore = useUserStore();
const notifStore = useNotifStore();
const register_user = () => {
  const formdata = new FormData(document.querySelector(".register-form"));
  if (
    username.value.length == 0 ||
    email_add.value.length == 0 ||
    password.value.length == 0 ||
    confirm_passwd.value.length == 0
  ) {
    notifStore.addNotif(
      "error",
      "Sign Up Failed",
      "One or more input fields have been left blank"
    );
    return;
  }
  if (
    !(
      username_valid.value &&
      email_add_valid.value &&
      password_valid.value &&
      confirm_passwd_valid.value
    )
  ) {
    notifStore.addNotif(
      "error",
      "Sign Up Failed",
      "One or more input fields are not filled properly"
    );
    return;
  }
  async function make_request() {
    try {
      const request = await fetch("http://localhost:5000/auth/signup", {
        method: "POST",
        body: formdata,
      });
      const response = await request.json();
      if (request.ok) {
        userStore.upload_signupdata(response);
        notifStore.addNotif(
          "success",
          "Sign Up Success",
          "User Registeration successfull."
        );
        formdata.delete("email_address");
        formdata.delete("role");
        login_user(formdata);
      } else {
        if (response.errors) {
          for (const key in response.errors) {
            notifStore.addNotif("error", "SignUp Error", response.errors[key]);
          }
        } else {
          notifStore.addNotif("error", "SignUp Error", response.message);
        }
      }
    } catch (error) {
      notifStore.addNotif("error", "Error", error.message);
    }
  }
  make_request();
};
</script>

<style>
.page-head {
  text-align: center;
  font-size: 60px;
  margin: 40px 0 10px;
}
.register-form {
  width: 700px;
  margin: 0 auto 100px;
  padding: 20px 20px;
}
.radio-input input {
  display: none;
}

.radio-input {
  --container_width: 400px;
  position: relative;
  display: flex;
  align-items: center;
  border-radius: 10px;
  background-color: var(--backgroundwhite);
  color: #000000;
  width: var(--container_width);
  overflow: hidden;
  border: 1px solid rgba(53, 52, 52, 0.226);
  margin: 0 auto;
}

.radio-input label {
  width: 100%;
  padding: 10px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
  font-weight: 600;
  letter-spacing: -1px;
  font-size: 20px;
}

.selection {
  display: none;
  position: absolute;
  height: 100%;
  width: calc(var(--container_width) / 2);
  z-index: 0;
  left: 0;
  top: 0;
  transition: 0.15s ease;
}

.radio-input label:has(input:checked) {
  color: #fff;
}

.radio-input label:has(input:checked) ~ .selection {
  background-color: rgb(11 117 223);
  display: inline-block;
}

.radio-input label:nth-child(1):has(input:checked) ~ .selection {
  transform: translateX(calc(var(--container_width) * 0 / 2));
}

.radio-input label:nth-child(2):has(input:checked) ~ .selection {
  transform: translateX(calc(var(--container_width) * 1 / 2));
}
/* Input container */
.input-container {
  position: relative;
  margin: 40px 20px;
}

/* Input field */
.input-field {
  display: block;
  width: 100%;
  padding: 10px;
  font-size: 20px;
  border: none;
  border-bottom: 2px solid #ccc;
  outline: none;
  background-color: transparent;
}

/* Input label */
.input-label {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 20px;
  color: rgba(204, 204, 204, 0);
  pointer-events: none;
  transition: all 0.3s ease;
}
.end-formline {
  text-align: center;
  margin-top: 10px;
}
/* Input highlight */
.input-highlight {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 0;
  background-color: #007bff;
  transition: all 0.3s ease;
}
.input-highlight-red {
  width: 100%;
  background-color: rgba(224, 0, 0, 0.782);
}
.input-err-msg {
  color: rgba(224, 0, 0, 0.782);
  text-align: right;
  position: absolute;
  bottom: -20px;
  right: 0px;
  font-size: 15px;
}
/* Input field:focus styles */
.input-field:focus + .input-label {
  top: -20px;
  font-size: 16px;
  color: #007bff;
}

.input-field:focus + .input-label + .input-highlight {
  width: 100%;
}

.register-button {
  margin: 0 50%;
  transform: translateX(-50%);
  padding: 12.5px 30px;
  border: 0;
  border-radius: 100px;
  background-color: #2ba8fb;
  color: #ffffff;
  font-weight: Bold;
  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  cursor: pointer;
  font-size: 25px;
}

.register-button:hover {
  background-color: #6fc5ff;
  box-shadow: 0 0 20px #6fc5ff50;
  transform: scale(1.1) translateX(-50%);
}

.register-button:active {
  background-color: #3d94cf;
  transition: all 0.25s;
  -webkit-transition: all 0.25s;
  box-shadow: none;
  transform: scale(0.98);
}
</style>
