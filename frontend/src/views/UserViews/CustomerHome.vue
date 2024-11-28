<template>
  <div class="error-div full-page-error" v-if="showError">
    <p>
      Your Account has been Flagged by Admin for Suspicious Activity! You cannot
      view anything until the issue is resolved!!
    </p>
  </div>
  <template v-if="showComponents">
    <UserServiceReqs :cid="customerData.id" />
    <SearchWorkers :cdata="customerData" />
  </template>
  <div class="user-loader" v-if="!showComponents && !showError"></div>
</template>

<script setup>
import SearchWorkers from "@/components/usercomponents/SearchWorkers.vue";
import { backend_req } from "@/composables/requestbackend";
import { useUserStore } from "@/stores/userstore";
import { onMounted, ref } from "vue";
import UserServiceReqs from "../../components/usercomponents/UserServiceReqs.vue";

const userStore = useUserStore();
const showComponents = ref(false);
const customerData = ref(null);
const showError = ref(false);

onMounted(() => {
  backend_req(`/customer/data/${userStore.uid}`, "GET", null).then((val) => {
    if (val && !val.isflagged) {
      customerData.value = val;
      showComponents.value = true;
    } else {
      showError.value = true;
    }
  });
});
</script>

<style>
.error-div p {
  text-align: center;
}
.full-page-error {
  transform: translateY(200px) scale(2);
}

.user-loader {
  border: 4px solid rgba(0, 0, 0, 0.4);
  border-left-color: transparent;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  animation: spin89345 1s linear infinite;
  margin: 30px auto;
  transform: scale(2);
}

@keyframes spin89345 {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
