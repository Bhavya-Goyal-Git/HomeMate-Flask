<template>
  <nav>
    <img
      src="/mylogo.png"
      class="logoimg"
      @click="$router.push({ name: 'homepage' })"
    />
    <!-- <RouterLink to="#" active-class="selected-navlink" class="nav-link"
      >Login</RouterLink
    > -->

    <RouterLink
      :to="{ name: 'signup' }"
      active-class="selected-navlink"
      class="nav-link last-navtab"
      >SignIn</RouterLink
    >
  </nav>
  <div class="top-nav-div"></div>
</template>

<script setup>
import { RouterLink } from "vue-router";
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
.last-navtab {
  margin-right: 20px;
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
</style>
