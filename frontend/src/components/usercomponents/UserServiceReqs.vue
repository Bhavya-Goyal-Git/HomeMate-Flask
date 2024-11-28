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
            <button
              class="tab-btn tab-btn-del"
              v-if="serv.status == 'booked' || serv.status == 'accepted'"
              @click="cancelServiceReq(serv.id, index)"
            >
              CANCEL
            </button>
            <button
              class="tab-btn tab-btn-create"
              v-if="serv.status == 'served'"
              @click="payCompleteService(serv.id, index)"
            >
              PAY & COMPLETE
            </button>
            <button
              class="tab-btn tab-btn-del"
              v-if="serv.status == 'rejected' || serv.status == 'cancelled'"
              @click="deleteServiceReq(serv.id, index)"
            >
              DELETE
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
  <WorkerModal
    v-if="showprofessional"
    :pid="showprofessionalId"
    @closeprofessional="showprofessional = false"
  />
  <BillView
    @closepayment="proceedPayment"
    v-if="showPayment"
    :sid="paymentSid"
  />
  <ReviewWorker
    v-if="showReview"
    :pid="workingPID"
    @closereview="CloseReview"
  />
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref } from "vue";
import WorkerModal from "../workercomponents/WorkerModal.vue";
import BillView from "../workercomponents/BillView.vue";
import ReviewWorker from "../workercomponents/ReviewWorker.vue";

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
const notifStore = useNotifStore();
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
function deleteServiceReq(sid, index) {
  backend_req(`/service/request/${sid}`, "DELETE", null).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        "Request Deleted",
        "Service request deleted successfully!"
      );
      servData.value.splice(index, 1);
      if (servData.value.length == 0) {
        showError.value = true;
        servData.value = null;
      }
    }
  });
}
function cancelServiceReq(sid, index) {
  let payload = { status: "cancelled" };
  backend_req(`/service/request/${sid}`, "PUT", payload).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        "Request Cancelled",
        "Successfully cancelled service request"
      );
      servData.value[index].status = "cancelled";
    }
  });
}
const paymentSid = ref(null);
const showPayment = ref(false);
const workingIndex = ref(null);
const showReview = ref(false);
const workingPID = ref(null);
function payCompleteService(sid, index) {
  paymentSid.value = sid;
  showPayment.value = true;
  workingIndex.value = index;
}
function proceedPayment(how) {
  if (how) {
    proceedPayment2();
  } else {
    notifStore.addNotif(
      "error",
      "Payment failed",
      "Payment cancelled in between!"
    );
    paymentSid.value = null;
    showPayment.value = false;
    workingIndex.value = null;
  }
}
function proceedPayment2() {
  let payload = { status: "completed" };
  backend_req(`/service/request/${paymentSid.value}`, "PUT", payload)
    .then((val) => {
      if (val) {
        notifStore.addNotif(
          "success",
          "Payment Done",
          "Payment Success, service request completed!"
        );
        servData.value[workingIndex.value].status = "completed";
        showPayment.value = false;
        return true;
      } else {
        showPayment.value = false;
        paymentSid.value = null;
        workingIndex.value = null;
        return false;
      }
    })
    .then((val) => {
      if (val) {
        //Review box open
        workingPID.value = servData.value[workingIndex.value].professional_id;
        showReview.value = true;
      }
    });
}
function CloseReview(how) {
  showReview.value = false;
  workingPID.value = null;
  workingIndex.value = null;
  paymentSid.value = null;
  if (!how) {
    notifStore.addNotif(
      "error",
      "Review Denied",
      "No review done for professional!"
    );
  }
}
</script>

<style>
.info-btn {
  margin-left: 4px;
  color: #5d26c4;
  cursor: pointer;
}
</style>
