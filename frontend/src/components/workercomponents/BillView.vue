<template>
  <Teleport to="body">
    <Modal @destroymodal="closepay(false)">
      <h1 class="page-head">Service Bill</h1>
      <div class="bill-div" v-if="billData">
        <p>Base Price of Service .......... {{ billData.base_price }}</p>
        <p>
          Professional fees .......... &#8377;{{ billData.worker_fee }}
          {{ billData.worker_fee_unit }}
        </p>
        <p>
          Professional's working units .......... {{ billData.work_units }}
          {{
            billData.worker_fee_unit.substring(
              billData.worker_fee_unit.indexOf(" ") + 1
            ) + "(s)"
          }}
        </p>
        <p>
          Parts or Materials cost .......... &#8377;{{ billData.parts_cost }}
        </p>
        <hr />
        <p>Net Total Bill .......... &#8377;{{ billData.total_bill }}</p>
      </div>
      <button
        class="modal-re-btn"
        @click="closepay(true)"
        style="margin-left: 25vw"
      >
        Pay
      </button>
    </Modal>
  </Teleport>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { onMounted, ref } from "vue";
import Modal from "../essentials/Modal.vue";
const props = defineProps({
  sid: {
    type: Number,
    required: true,
  },
});
const billData = ref(null);
onMounted(() => {
  backend_req(`/service/bill/${props.sid}`, "GET", null).then((val) => {
    if (val) {
      billData.value = val;
    }
  });
});
const emit = defineEmits(["closepayment"]);
function closepay(how) {
  emit("closepayment", how);
}
</script>

<style>
.bill-div {
  background-color: var(--darkgrey1);
  display: flex;
  flex-direction: column;
  margin: 10px auto;
  align-items: center;
  padding: 15px;
  border-radius: 12px;
  max-width: 500px;
}
.bill-div p {
  margin-bottom: 7px;
  font-size: 22px;
}
</style>
