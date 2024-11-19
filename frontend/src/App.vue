<template>
  <NavBar />
  <Notifications />
  <RouterView />
</template>

<script setup>
import { RouterView } from "vue-router";
import NavBar from "./components/essentials/NavBar.vue";
import Notifications from "./components/essentials/Notifications.vue";
</script>

<style></style>
