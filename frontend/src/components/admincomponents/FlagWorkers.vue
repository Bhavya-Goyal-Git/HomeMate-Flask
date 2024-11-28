<template>
  <h1 class="component-head">Professionals on Platform</h1>
  <table class="service-tab">
    <thead>
      <tr>
        <th>Id</th>
        <th>Name</th>
        <th>Address, Contact</th>
        <th>Service ID</th>
        <th>Experience</th>
        <th>Description</th>
        <th>Fees</th>
        <th>Rating</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(cust, index) in cdata" :key="cust.id">
        <td>{{ index + 1 }}</td>
        <td>{{ cust.name }}</td>
        <td>
          {{ cust.address.base_address }}, {{ cust.address.city }}-{{
            cust.address.pincode
          }}, {{ cust.address.state }}, {{ cust.contact_no }}
        </td>
        <td>{{ cust.service_id }}</td>
        <td>{{ cust.experience }} yrs</td>
        <td>{{ cust.description }}</td>
        <td>{{ cust.fees }} {{ cust.fees_unit }}</td>
        <td>{{ getStars(cust.rating, cust.num_raters) }}</td>
        <td>
          <div class="action-btn-cont">
            <button class="tab-btn tab-btn-create" @click="showrev(cust.id)">
              SHOW REVIEWS
            </button>
            <button
              class="tab-btn tab-btn-edit"
              v-if="cust.isflagged"
              @click="flagCustomer(cust.id, index)"
            >
              UNFLAG
            </button>
            <button
              class="tab-btn tab-btn-del"
              v-else
              @click="flagCustomer(cust.id, index)"
            >
              FLAG
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <ShowReviewComp
    :pid="currentReview"
    v-if="showWorkerReview"
    @closerev="closeWorkerReview"
  />
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref } from "vue";
import ShowReviewComp from "../workercomponents/ShowReviews.vue";

const notifStore = useNotifStore();
const cdata = ref(null);
const currentReview = ref(null);
const showWorkerReview = ref(false);

onMounted(() => {
  backend_req("/professional/data", "GET", null).then((val) => {
    if (val) {
      cdata.value = val;
    }
  });
});

function getStars(rating, raters) {
  if (raters == 0) return "--";
  let num = rating / raters;
  return parseFloat(num.toFixed(2));
}

function flagCustomer(cid, index) {
  backend_req(`/professional/data/${cid}`, "PATCH", null).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        "Action done!",
        "Sucessfully changed flag status of professional"
      );
      cdata.value[index].isflagged = !cdata.value[index].isflagged;
    }
  });
}

function showrev(pid) {
  currentReview.value = pid;
  showWorkerReview.value = true;
}
function closeWorkerReview() {
  showWorkerReview.value = false;
}
</script>
