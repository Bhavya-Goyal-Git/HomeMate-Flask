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
            <button
              class="tab-btn tab-btn-create"
              v-if="serv.status == 'booked'"
              @click="acceptRejectService(serv.id, index, 'accepted')"
            >
              ACCEPT
            </button>
            <button
              class="tab-btn tab-btn-del"
              v-if="serv.status == 'booked'"
              @click="acceptRejectService(serv.id, index, 'rejected')"
            >
              REJECT
            </button>
            <button
              class="tab-btn tab-btn-create"
              v-if="serv.status == 'accepted'"
              @click="serveService(serv.id, index)"
            >
              MARK SERVED
            </button>
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
  <Teleport to="body">
    <ModalComp @destroymodal="killServingModal" v-if="showServingModal">
      <h1 class="page-head">Mark Served</h1>
      <div style="display: flex; justify-content: center; align-items: center">
        <div class="input-container">
          <input
            placeholder="Work units"
            class="input-field"
            type="number"
            v-model="work_units"
          />
          <label for="input-field" class="input-label">Work Units</label>
          <span class="input-highlight"></span>
        </div>
        <p style="margin-left: 10px; font-size: 20px">
          {{ props.pfees.substring(props.pfees.indexOf(" ") + 1) + "(s)" }}
        </p>
      </div>
      <div style="display: flex; justify-content: center; align-items: center">
        <div class="input-container">
          <input
            placeholder="Parts or Materials Cost"
            class="input-field"
            type="number"
            v-model="parts_cost"
          />
          <label for="input-field" class="input-label"
            >Parts or Materials Cost</label
          >
          <span class="input-highlight"></span>
        </div>
      </div>
      <button
        class="modal-re-btn"
        style="margin-left: 25vw"
        @click="serveServiceFinal()"
      >
        Submit
      </button>
    </ModalComp>
  </Teleport>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref } from "vue";
import CustModal from "../usercomponents/CustModal.vue";
import ModalComp from "../essentials/Modal.vue";

const props = defineProps({
  pid: {
    type: Number,
    required: true,
  },
  pfees: {
    type: String,
    required: true,
  },
});
const servData = ref(null);
const showError = ref(false);
const showcustomer = ref(false);
const showcustomerId = ref(null);
const notifStore = useNotifStore();
const servingReq = ref({
  sid: null,
  index: null,
});
const showServingModal = ref(false);
const parts_cost = ref(null);
const work_units = ref(null);
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
function acceptRejectService(sid, index, keywd) {
  let payload = { status: keywd };
  backend_req(`/service/request/${sid}`, "PUT", payload).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        `Request ${keywd.toUpperCase()}`,
        `Service request ${keywd} successfully!`
      );
      servData.value[index].status = keywd;
    }
  });
}
function serveService(sid, index) {
  servingReq.value.sid = sid;
  servingReq.value.index = index;
  showServingModal.value = true;
}
function killServingModal() {
  servingReq.value.sid = null;
  servingReq.value.index = null;
  showServingModal.value = false;
  parts_cost.value = null;
  work_units.value = null;
}
function serveServiceFinal() {
  if (!work_units.value) {
    notifStore.addNotif("error", "Error", "Input fields empty!");
    killServingModal();
    return;
  }
  if (parts_cost.value < 0 || work_units.value <= 0) {
    notifStore.addNotif(
      "error",
      "Error",
      "Input fields must be positive numbers!"
    );
    killServingModal();
    return;
  }
  let payload = {
    status: "served",
    work_units: work_units.value,
    parts_cost: parts_cost.value,
  };
  backend_req(`/service/request/${servingReq.value.sid}`, "PUT", payload).then(
    (val) => {
      if (val) {
        servData.value[servingReq.value.index].status = "served";
        notifStore.addNotif(
          "success",
          "Request Served",
          "Successfully served the service request!"
        );
        killServingModal();
      } else {
        killServingModal();
      }
    }
  );
}
</script>

<style></style>
