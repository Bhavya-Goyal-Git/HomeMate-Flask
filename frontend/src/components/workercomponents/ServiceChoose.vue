<template>
  <Teleport to="body">
    <ModalComp @destroymodal="closeChoose">
      <div class="serv-head-div modal-table">
        <h1>Services Available</h1>
        <span class="dropdown-title">View:</span>
        <div class="select-dropdown">
          <select v-model="viewCat">
            <option value="all">All</option>
            <option v-for="cat in serviceCats" :key="cat.id" :value="cat.title">
              {{ cat.title }}
            </option>
          </select>
        </div>
      </div>
      <table class="service-tab" v-if="servicesData">
        <thead>
          <tr>
            <th>Id</th>
            <th>Title</th>
            <th>Category</th>
            <th>Base_price</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(serv, index) in servicesData"
            :key="serv.id"
            class="chooser-tab"
            @click="closeChoose(serv)"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ serv.title }}</td>
            <td>{{ serv.category }}</td>
            <td>&#8377;{{ serv.base_price }}</td>
            <td>{{ serv.description }}</td>
          </tr>
        </tbody>
      </table>
    </ModalComp>
  </Teleport>
</template>

<script setup>
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref, watch } from "vue";
import { backend_req } from "../../composables/requestbackend";
import ModalComp from "../essentials/Modal.vue";

const servicesData = ref(null);
const allServiceData = ref(null);
const viewCat = ref("all");
const serviceCats = ref(null);
const notifStore = useNotifStore();
const emit = defineEmits(["servicechosen"]);

onMounted(async () => {
  backend_req("/service/categories", "GET", null).then((val) => {
    if (val) {
      serviceCats.value = val;
    }
  });
});

onMounted(async () => {
  backend_req("/service", "GET", null).then((val) => {
    if (val) {
      allServiceData.value = val;
      servicesData.value = val;
    }
  });
});

watch(viewCat, (newval, oldval) => {
  if (newval == "all") {
    servicesData.value = allServiceData.value;
  } else {
    servicesData.value = allServiceData.value.filter((serv) => {
      if (serv.category == newval) {
        return true;
      }
    });
  }
});

function closeChoose(serv) {
  if (serv) {
    emit("servicechosen", serv);
  } else {
    emit("servicechosen");
  }
}
</script>

<style>
.modal-table {
  max-width: 90%;
}
.chooser-tab {
  cursor: pointer;
}
</style>
