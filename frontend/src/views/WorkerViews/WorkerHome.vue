<template>
  <div class="error-div full-page-error" v-if="showError">
    <p>
      Your Account has been Flagged by Admin for Suspicious Activity! You cannot
      view anything until the issue is resolved!!
    </p>
  </div>
  <template v-if="showComponents">
    <WorkerServiceReqs :pid="workerData.id" :pfees="workerData.fees_unit" />
  </template>
  <div class="user-loader" v-if="!showComponents && !showError"></div>
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

onMounted(() => {
  backend_req(`/professional/data/${userStore.uid}`, "GET", null).then(
    (val) => {
      if (val && !val.isflagged) {
        workerData.value = val;
        showComponents.value = true;
      } else {
        showError.value = true;
      }
    }
  );
});
</script>

<style></style>
