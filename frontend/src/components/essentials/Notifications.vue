<template>
  <div class="notif-container" v-if="notifStore.notifications">
    <TransitionGroup name="notifs">
      <SingleNotif
        v-for="notif in notifStore.notifications"
        :key="notif.id"
        v-bind="notif"
        @destroy="removeNotification"
      />
    </TransitionGroup>
  </div>
</template>

<script setup>
import SingleNotif from "./SingleNotif.vue";
import { useNotifStore } from "../../stores/notificationstore";

const notifStore = useNotifStore();
function removeNotification(id) {
  notifStore.removeNotif(id);
}
</script>

<style>
.notif-container {
  position: fixed;
  top: 80px;
  right: 0;
  width: 370px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.notifs-enter-active {
  animation: bouncein 0.5s ease-in;
}
.notifs-leave-active {
  transition: all 0.5s;
  position: absolute;
}
.notifs-leave-to {
  opacity: 0;
}
.notifs-move {
  transition: all 0.5s;
}
@keyframes bouncein {
  0% {
    transform: translateX(400px);
  }
  70% {
    transform: translateX(-45px);
  }
  100% {
    transform: translateX(0);
  }
}
</style>
