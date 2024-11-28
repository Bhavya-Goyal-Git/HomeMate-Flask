<template>
  <h1 class="component-head">Pending Professional Approvals</h1>
  <table class="service-tab" v-if="pendingProfessionals && professionalsData">
    <thead>
      <tr>
        <th>Id</th>
        <th>Name</th>
        <th>Address</th>
        <th>Contact no</th>
        <th>Service</th>
        <th>Experience (yrs)</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(pdata, index) in professionalsData" :key="pdata.id">
        <td>{{ index + 1 }}</td>
        <td>{{ pdata.name }}</td>
        <td>
          {{ pdata.address.base_address }}, {{ pdata.address.city }}-{{
            pdata.address.pincode
          }},
          {{ pdata.address.state }}
        </td>
        <td>{{ pdata.contact_no }}</td>
        <td>{{ get_servicename(pdata.service_id) }}</td>
        <td>{{ pdata.experience }}</td>
        <td>
          <div class="action-btn-cont">
            <button
              class="tab-btn tab-btn-edit"
              @click="view_worker_docs(pdata.id)"
            >
              VIEW DOCUMENTS
            </button>
            <button
              class="tab-btn tab-btn-create"
              @click="update_worker(pdata.id, 'approved')"
            >
              APPROVE
            </button>
            <button
              class="tab-btn tab-btn-del"
              @click="update_worker(pdata.id, 'rejected')"
            >
              REJECT
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <div v-if="showError" class="error-div">
    <p>There are no pending Approvals!</p>
    <button class="error-refresh-btn" @click="getunverified">Refresh</button>
  </div>
  <div class="user-loader" v-if="!pendingProfessionals && !showError"></div>
</template>

<script setup>
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref } from "vue";
import { backend_req } from "../../composables/requestbackend";
import { backend_req_file } from "../../composables/requestfile";

const notifStore = useNotifStore();
const professionalsData = ref(null);
const pendingProfessionals = ref(false);
const showError = ref(false);
const servicesData = ref(null);

onMounted(() => {
  backend_req("/service", "GET", null)
    .then((val) => {
      if (val) {
        servicesData.value = val;
      }
    })
    .then(() => {
      getunverified();
    });
});

function getunverified() {
  showError.value = false;
  backend_req("/professional/data?unverified=true", "GET", null).then((val) => {
    if (val && val.length > 0) {
      pendingProfessionals.value = true;
      professionalsData.value = val;
    } else {
      showError.value = true;
    }
  });
}

function get_servicename(servId) {
  return servicesData.value.find((ser) => {
    return ser.id == servId;
  }).title;
}

function update_worker(workerId, status) {
  const payload = {
    status: status,
  };
  backend_req(`/professional/data/${workerId}`, "PATCH", payload).then(
    (val) => {
      if (val) {
        notifStore.addNotif(
          "success",
          "Proposal updated",
          `Successfully ${status} professional's request.`
        );
        professionalsData.value = professionalsData.value.filter((s) => {
          if (s.id != workerId) return true;
          return false;
        });
        if (professionalsData.value.length == 0) {
          pendingProfessionals.value = false;
          showError.value = true;
        }
      }
    }
  );
}

function view_worker_docs(pid) {
  backend_req_file(`/professional/docs/${pid}`, "GET");
}
</script>

<style>
.component-head {
  font-size: 45px;
  text-align: center;
  margin-top: 15px;
}
.error-div {
  padding: 20px 20px;
  justify-content: center;
  align-items: center;
  display: flex;
  border: 2px solid var(--myred);
  background-color: #fe4a4977;
  border-radius: 10px;
  margin: 10px auto;
  width: 40%;
}
.error-refresh-btn {
  color: white;
  background-color: #4f29f0bb;
  padding: 10px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}
</style>
