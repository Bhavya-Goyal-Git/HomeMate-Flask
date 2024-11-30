<template>
  <div class="error-div full-page-error" v-if="showError">
    <p>
      Your Account has been Flagged by Admin for Suspicious Activity! You cannot
      view anything until the issue is resolved!!
    </p>
  </div>
  <div class="error-div full-page-error" v-if="showUnverified">
    <p>
      {{ content }}
    </p>
  </div>
  <template v-if="showComponents">
    <WorkerServiceReqs :pid="workerData.id" :pfees="workerData.fees_unit" />
  </template>
  <div
    class="user-loader"
    v-if="!showComponents && !showError && !showUnverified"
  ></div>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useUserStore } from "@/stores/userstore";
import { onMounted, ref } from "vue";
import WorkerServiceReqs from "../../components/workercomponents/WorkerServiceReqs.vue";

const userStore = useUserStore();
const showComponents = ref(false);
const workerData = ref(null);
const showError = ref(false);
const showUnverified = ref(false);
const content = ref(null);

onMounted(() => {
  backend_req(`/professional/data/${userStore.uid}`, "GET", null).then(
    (val) => {
      if (val && !val.isflagged && val.isverified == "approved") {
        workerData.value = val;
        showComponents.value = true;
      } else if (val && !val.isflagged && val.isverified == "pending") {
        showUnverified.value = true;
        content.value =
          "Your Documents have not been verified by Admin yet, please wait before you start recieving customer requests!";
      } else if (val && !val.isflagged && val.isverified == "rejected") {
        showUnverified.value = true;
        content.value =
          "Your Documents have not been REJECTED by Admin, please contact at admin@homemate.in for retrying to register on the platform";
      } else {
        showError.value = true;
      }
    }
  );
});
</script>

<style></style>
