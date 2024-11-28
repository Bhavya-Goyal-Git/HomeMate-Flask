<template>
  <Teleport to="body">
    <ModalComp @destroymodal="closeEdit">
      <h1 class="page-head">Customer Details</h1>
      <div v-if="custData" class="modal-information-div">
        <h3>Name: {{ custData.name }}</h3>
        <h3>Base Address: {{ custData.address.base_address }}</h3>
        <h3>
          City: {{ custData.address.city }}-{{ custData.address.pincode }}
        </h3>
        <h3>State: {{ custData.address.state }}</h3>
      </div>
    </ModalComp>
  </Teleport>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { onMounted, ref } from "vue";
import ModalComp from "../essentials/Modal.vue";

const props = defineProps({
  cid: {
    type: Number,
    required: true,
  },
});
const custData = ref(null);
onMounted(() => {
  backend_req(`/customer/${props.cid}`, "GET", null).then((val) => {
    if (val) {
      custData.value = val;
    }
  });
});
const emit = defineEmits(["closecustomer"]);
function closeEdit() {
  emit("closecustomer");
}
</script>

<style>
.modal-information-div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.modal-information-div h3 {
  margin-bottom: 10px;
}
</style>
