<template>
  <h1 class="page-head">User Log In</h1>
  <form class="register-form" @submit.prevent="make_request">
    <div class="input-container">
      <input
        placeholder="Username"
        class="input-field"
        type="text"
        name="username"
        v-model="username"
      />
      <label for="input-field" class="input-label">Username</label>
      <span class="input-highlight"></span>
    </div>
    <div class="input-container">
      <input
        placeholder="Password"
        class="input-field"
        type="password"
        name="password"
        v-model="password"
      />
      <label for="input-field" class="input-label">Password</label>
      <span class="input-highlight"></span>
    </div>
    <button class="register-button">Login</button>
    <p class="end-formline">
      Don't have an account?<RouterLink :to="{ name: 'signup' }">
        Register here</RouterLink
      >
    </p>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { login_user } from "../composables/loginuser";
import { useNotifStore } from "../stores/notificationstore";

const username = ref("");
const password = ref("");
const notifStore = useNotifStore();
function make_request() {
  const formdata = new FormData(document.querySelector(".register-form"));
  if (username.value.length == 0 || password.value.length == 0) {
    notifStore.addNotif(
      "error",
      "LogIn Failed",
      "One or more input fields have been left blank"
    );
    return;
  }
  login_user(formdata);
}
</script>
