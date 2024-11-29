<template>
  <div class="top-export-div">
    <h3>Click here to export All Service Request data!</h3>
    <button
      class="tab-btn tab-btn-create"
      style="margin-left: 10px"
      @click="getData"
    >
      Get Data
    </button>
  </div>
  <div class="user-loader" v-if="showLoader" style="margin: 5px auto"></div>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { useUserStore } from "@/stores/userstore";
import { ref, watch } from "vue";

const taskId = ref(null);
const fileName = ref(null);
const showLoader = ref(false);

const notifStore = useNotifStore();
const userStore = useUserStore();
function getData() {
  showLoader.value = true;
  backend_req("/servicerequest/getcsv", "POST", null)
    .then((val) => {
      if (val) {
        taskId.value = val.job_id;
        return true;
      }
      showLoader.value = false;
      return false;
    })
    .then((val) => {
      if (val) {
        const eventSource = new EventSource(
          `http://localhost:5000/stream?channel=${taskId.value}`
        );
        eventSource.onmessage = function (event) {
          const data = JSON.parse(event.data);
          if (data.status == "success") {
            fileName.value = data.filename;
          } else {
            notifStore.addNotif(
              "error",
              "Error",
              "Error in creating csv at backend"
            );
            showLoader.value = false;
          }
          eventSource.close();
        };
        eventSource.onerror = function (event) {
          showLoader.value = false;
          notifStore.addNotif(
            "error",
            "Error",
            "Error in connecting to SSE backend"
          );
          eventSource.close();
          showLoader.value = false;
        };
      }
    });
}
watch(fileName, (newval, oldval) => {
  fetch(`http://localhost:5000/servicerequest/getcsv?fname=${newval}`, {
    headers: {
      Authorization: `Bearer ${userStore.refresh_token}`,
    },
  })
    .then((resp) => {
      return resp.blob();
    })
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = newval;
      link.click();
      URL.revokeObjectURL(url);
      showLoader.value = false;
    })
    .catch((error) => {
      notifStore.addNotif(
        "error",
        "Error",
        "Error in fetching generated file!"
      );
      showLoader.value = false;
    });
});
</script>

<style>
.top-export-div {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  margin-top: 10px;
}
</style>
