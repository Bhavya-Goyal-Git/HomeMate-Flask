<template>
  <h1 class="component-head">Customers on Platform</h1>
  <table class="service-tab" v-if="cdata">
    <thead>
      <tr>
        <th>Id</th>
        <th>Name</th>
        <th>Address</th>
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
          }}, {{ cust.address.state }}
        </td>
        <td>
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
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref } from "vue";

const notifStore = useNotifStore();
const cdata = ref(null);

onMounted(() => {
  backend_req("/customer/data", "GET", null).then((val) => {
    if (val) {
      cdata.value = val;
    }
  });
});

function flagCustomer(cid, index) {
  backend_req(`/customer/data/${cid}`, "PATCH", null).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        "Action done!",
        "Sucessfully changed flag status of customer"
      );
      cdata.value[index].isflagged = !cdata.value[index].isflagged;
    }
  });
}
</script>
