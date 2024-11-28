<template>
  <div style="display: flex; justify-content: center; align-items: center">
    <h1 class="component-head">My Service Requests</h1>
    <button
      class="tab-btn tab-btn-create"
      style="margin: 7px 0 0 10px"
      @click="getReqs"
    >
      Refresh
    </button>
  </div>
  <table class="service-tab" v-if="servData">
    <thead>
      <tr>
        <th>Id</th>
        <th>Professional Name</th>
        <th>Service</th>
        <th>Date Requested</th>
        <th>Date of Service</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(serv, index) in servData" :key="serv.id">
        <td>{{ index + 1 }}</td>
        <td>
          {{ serv.professional_name }}
          <i
            class="fa-solid fa-circle-info info-btn"
            @click="showworkerdata(serv.id)"
          ></i>
        </td>
        <td>{{ serv.service_name }}</td>
        <td>{{ serv.dateofrequest }}</td>
        <td>{{ serv.dateofcompletion }}</td>
        <td>{{ serv.status.toUpperCase() }}</td>
        <td>
          <div class="action-btn-cont">
            <button class="tab-btn tab-btn-edit">EDIT</button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="error-div" v-if="showError">
    <p>No Service Requests available!</p>
  </div>
  <div class="user-loader" v-if="!servData && !showError"></div>
  <WorkerModal
    v-if="showprofessional"
    :pid="showprofessionalId"
    @closeprofessional="showprofessional = false"
  />
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { onMounted, ref } from "vue";
import WorkerModal from "../workercomponents/WorkerModal.vue";
const props = defineProps({
  cid: {
    type: Number,
    required: true,
  },
});
const servData = ref(null);
const showError = ref(false);
const showprofessionalId = ref(null);
const showprofessional = ref(false);
function getReqs() {
  showError.value = false;
  servData.value = null;
  backend_req(`/service/requests/customer/${props.cid}`, "GET", null).then(
    (val) => {
      if (val && val.length > 0) {
        servData.value = val;
      } else {
        showError.value = true;
      }
    }
  );
}
onMounted(() => {
  getReqs();
});
function showworkerdata(pid) {
  showprofessionalId.value = pid;
  showprofessional.value = true;
}
</script>

<style>
.info-btn {
  margin-left: 4px;
  color: #5d26c4;
  cursor: pointer;
}
</style>
