<template>
  <div class="serv-head-div">
    <h1>Services on Platform</h1>
    <span class="dropdown-title">View:</span>
    <div class="select-dropdown">
      <select v-model="viewCat">
        <option value="all">All</option>
        <option v-for="cat in serviceCats" :key="cat.id" :value="cat.title">
          {{ cat.title }}
        </option>
      </select>
    </div>
    <button class="tab-btn tab-btn-create" @click="service_form('Create', {})">
      CREATE NEW
    </button>
  </div>
  <table class="service-tab" v-if="servicesData">
    <thead>
      <tr>
        <th>Id</th>
        <th>Title</th>
        <th>Category</th>
        <th>Base_price</th>
        <th>Description</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(serv, index) in servicesData" :key="serv.id">
        <td>{{ index + 1 }}</td>
        <td>{{ serv.title }}</td>
        <td>{{ serv.category }}</td>
        <td>&#8377;{{ serv.base_price }}</td>
        <td>{{ serv.description }}</td>
        <td>
          <div class="action-btn-cont">
            <button
              class="tab-btn tab-btn-edit"
              @click="service_form('Edit', serv)"
            >
              EDIT
            </button>
            <button class="tab-btn tab-btn-del" @click="delete_serv(serv.id)">
              DELETE
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <EditServiceComp
    v-if="showEditModal"
    :mode="editServicemode"
    :suggestions="serviceCats"
    v-bind="editServiceobj"
    @workdone="completeEdit"
  />
</template>

<script setup>
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref, watch } from "vue";
import { backend_req } from "../../composables/requestbackend";
import EditServiceComp from "./EditService.vue";

const servicesData = ref(null);
const allServiceData = ref(null);
const viewCat = ref("all");
const serviceCats = ref(null);
const notifStore = useNotifStore();

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

function delete_serv(service_id) {
  backend_req(`/service/${service_id}`, "DELETE", null).then((val) => {
    if (val) {
      notifStore.addNotif(
        "success",
        "Service Deleted",
        "Service deleted successfully!"
      );
      allServiceData.value = allServiceData.value.filter((serv) => {
        if (serv.id == service_id) {
          return false;
        }
        return true;
      });
      if (viewCat.value == "all") {
        servicesData.value = allServiceData.value;
      } else {
        servicesData.value = allServiceData.value.filter((serv) => {
          if (serv.category == viewCat.value) {
            return true;
          }
        });
      }
    }
  });
}

const editServicemode = ref(null);
const editServiceobj = ref({});
const showEditModal = ref(false);
function service_form(mode, payload) {
  editServicemode.value = mode;
  editServiceobj.value = payload;
  showEditModal.value = true;
}
function completeEdit(servnew) {
  showEditModal.value = false;
  if (servnew && editServicemode.value == "Create") {
    allServiceData.value.push(servnew);
  } else if (servnew && editServicemode.value == "Edit") {
    let ind = allServiceData.value.findIndex((s) => s.id === servnew.id);
    allServiceData.value[ind] = servnew;
  }
}
</script>

<style>
.serv-head-div {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px auto;
}
.serv-head-div h1 {
  margin-right: 10px;
}
.service-tab {
  border-collapse: collapse;
  margin: 25px auto;
  font-size: 16px;
  min-width: 400px;
  max-width: 1250px;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.service-tab thead tr {
  background-color: #009879;
  color: #ffffff;
  text-align: left;
  font-weight: bold;
}

.service-tab th,
.service-tab td {
  padding: 12px 10px;
}

.service-tab tbody tr {
  border-bottom: 1px solid #dddddd;
}

.service-tab tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}

.service-tab tbody tr:last-of-type {
  border-bottom: 2px solid #009879;
}

.service-tab tbody tr:hover {
  font-weight: bold;
  color: #009879;
}
.action-btn-cont {
  display: flex;
  justify-content: center;
  align-items: center;
}
.tab-btn {
  padding: 8px 10px;
  border-radius: 5px;
  border: none;
  color: white;
  margin: 3px;
  cursor: pointer;
}
.tab-btn:hover {
  font-weight: bold;
}
.tab-btn-edit {
  background-color: var(--myyellow);
}
.tab-btn-del {
  background-color: var(--myred);
}
.tab-btn-create {
  background-color: var(--mygreen);
}
.select-dropdown {
  border-radius: 5px;
  margin-right: 10px;
  color: black;
  font-size: 16px;
  background-color: var(--myyellow);
}
.select-dropdown select {
  padding: 8px 10px;
  border: none;
  background-color: transparent;
  width: 100%;
}
.select-dropdown select:active,
.select-dropdown select:focus {
  outline: none;
  box-shadow: none;
}
.select-dropdown:after {
  content: " ";
  position: absolute;
  top: 50%;
  margin-top: -2px;
  right: 8px;
  width: 0;
  height: 0;
}
.select-dropdown option {
  font-size: 16px;
  background: var(--darkgrey1);
  color: black;
  width: 100%;
}
.dropdown-title {
  font-size: 16px;
  font-weight: bold;
  margin-right: 8px;
}
</style>
