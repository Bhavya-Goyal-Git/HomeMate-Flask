<template>
  <div class="modal-bg" @click.self="$emit('destroymodal')">
    <div class="modal-fg">
      <slot> </slot>
    </div>
  </div>
</template>

<script setup></script>

<style>
.modal-bg {
  background-color: #35374ccc;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 300;
}
.modal-fg {
  background-color: var(--backgroundwhite);
  width: 60%;
  max-height: 70%;
  padding: 20px;
  border-radius: 15px;
  overflow-y: scroll;
}
</style>
