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
        <th>Customer Name</th>
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
          {{ serv.customer_name }}
          <i
            class="fa-solid fa-circle-info info-btn"
            @click="showCustomermodal(serv.id)"
          ></i>
        </td>
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
  <CustModal
    v-if="showcustomer"
    :cid="showcustomerId"
    @closecustomer="showcustomer = false"
  />
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { onMounted, ref } from "vue";
import CustModal from "../usercomponents/CustModal.vue";

const props = defineProps({
  pid: {
    type: Number,
    required: true,
  },
});
const servData = ref(null);
const showError = ref(false);
const showcustomer = ref(false);
const showcustomerId = ref(null);
function getReqs() {
  showError.value = false;
  servData.value = null;
  backend_req(`/service/requests/professional/${props.pid}`, "GET", null).then(
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
function showCustomermodal(cid) {
  showcustomerId.value = cid;
  showcustomer.value = true;
}
</script>

<style></style>
