<template>
  <nav>
    <img
      src="/mylogo.png"
      class="logoimg"
      @click="$router.push({ name: 'homepage' })"
    />
    <template v-if="userstore.is_loggedIn">
      <template v-if="userstore.role == 'customer'">
        <RouterLink
          :to="{ name: 'customerHome' }"
          active-class="selected-navlink"
          class="nav-link"
          >Home</RouterLink
        >
        <RouterLink
          :to="{ name: 'customerStats' }"
          active-class="selected-navlink"
          class="nav-link"
          >Statistics</RouterLink
        >
      </template>
      <template v-else-if="userstore.role == 'professional'">
        <RouterLink
          :to="{ name: 'workerHome' }"
          active-class="selected-navlink"
          class="nav-link"
          >Home</RouterLink
        >
        <RouterLink
          :to="{ name: 'workerStats' }"
          active-class="selected-navlink"
          class="nav-link"
          >Statistics</RouterLink
        >
      </template>
      <template v-else>
        <RouterLink
          :to="{ name: 'adminHome' }"
          active-class="selected-navlink"
          class="nav-link"
          >Home</RouterLink
        >
        <RouterLink
          :to="{ name: 'adminFlagUsers' }"
          active-class="selected-navlink"
          class="nav-link"
          >Manage Users</RouterLink
        >
        <RouterLink
          :to="{ name: 'adminStats' }"
          active-class="selected-navlink"
          class="nav-link"
          >Statistics</RouterLink
        >
      </template>
    </template>
    <button
      @click="signinout"
      class="nav-btn"
      :class="{ 'nav-btn-logout': userstore.is_loggedIn }"
    >
      <span class="nav-btn-span">{{ buttonTitle }}</span>
    </button>
  </nav>
  <div class="top-nav-div"></div>
</template>

<script setup>
import { useNotifStore } from "@/stores/notificationstore";
import { ref, watch } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useUserStore } from "../../stores/userstore";

const router = useRouter();
const notifStore = useNotifStore();
const userstore = useUserStore();

const buttonTitle = ref("Login");
watch(
  () => userstore.is_loggedIn,
  (newval, oldval) => {
    if (newval === true) {
      buttonTitle.value = "Log Out";
    } else {
      buttonTitle.value = "Login";
    }
  },
  { immediate: true }
);

function signinout() {
  if (userstore.is_loggedIn) {
    router.push({ name: "homepage" });
    userstore.resetData();
    notifStore.addNotif("success", "Logged Out", "Logged Out successfully!");
  } else {
    router.push({ name: "login" });
  }
}
</script>

<style>
nav {
  background-color: var(--mygrey);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}
.top-nav-div {
  height: 70px;
  width: 100%;
}
.logoimg {
  width: 200px;
  margin-left: 8px;
  cursor: pointer;
}
.nav-link {
  font-size: 20px;
  text-decoration: none;
  color: var(--darkgrey2);
  padding: 5px;
}
.nav-link:hover {
  color: var(--darkgrey3);
  border-bottom: 2px solid var(--darkgrey3);
}
.selected-navlink {
  color: var(--darkgrey3);
  font-weight: bold;
}
.nav-btn {
  outline: none;
  cursor: pointer;
  border: none;
  padding: 0.6rem 1.5rem;
  margin-right: 20px;
  font-family: inherit;
  position: relative;
  display: inline-block;
  letter-spacing: 0.05rem;
  font-weight: 700;
  font-size: 20px;
  border-radius: 500px;
  overflow: hidden;
  background: #66ff66;
  color: ghostwhite;
}
.nav-btn-logout {
  background: var(--myred);
}
.nav-btn .nav-btn-span {
  position: relative;
  z-index: 10;
  transition: color 0.4s;
}

.nav-btn:hover .nav-btn-span {
  color: black;
}

.nav-btn::before,
.nav-btn::after {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.nav-btn::before {
  content: "";
  background: var(--darkgrey3);
  width: 120%;
  left: -10%;
  transform: skew(30deg);
  transition: transform 0.4s cubic-bezier(0.3, 1, 0.8, 1);
}

.nav-btn:hover::before {
  transform: translate3d(100%, 0, 0);
}
</style>
