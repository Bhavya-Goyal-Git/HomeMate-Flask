<template>
  <Teleport to="body">
    <ModalComp @destroymodal="closeEdit">
      <h1 class="page-head">{{ mode }} Service</h1>
      <form @submit.prevent="make_request">
        <div class="input-container">
          <input
            placeholder="Service Title"
            class="input-field"
            type="text"
            name="title"
            v-model="serv_title"
          />
          <label for="input-field" class="input-label">Service Title</label>
          <span class="input-highlight"></span>
        </div>
        <div class="input-container">
          <input
            placeholder="Category"
            class="input-field"
            type="text"
            name="category"
            v-model="serv_cat"
            list="categs"
          />
          <datalist id="categs">
            <option
              v-for="servcat in suggestions"
              :key="servcat.id"
              :value="servcat.title"
            >
              {{ servcat.title }}
            </option>
          </datalist>

          <label for="input-field" class="input-label">Category</label>
          <span class="input-highlight"></span>
        </div>
        <div class="input-container">
          <input
            placeholder="Base Price"
            class="input-field"
            type="number"
            min="1"
            name="base_price"
            v-model="serv_bp"
          />
          <label for="input-field" class="input-label">Base Price</label>
          <span class="input-highlight"></span>
        </div>
        <div class="input-container">
          <textarea
            placeholder="Service Description"
            class="input-field"
            type="text"
            name="description"
            v-model="serv_desc"
          />
          <label for="input-field" class="input-label"
            >Service Description</label
          >
          <span class="input-highlight"></span>
        </div>
        <button class="register-button">{{ mode }}</button>
      </form>
    </ModalComp>
  </Teleport>
</template>

<script setup>
import { ref } from "vue";
import ModalComp from "../essentials/Modal.vue";
import { backend_req } from "../../composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";

const emit = defineEmits(["workdone"]);

function closeEdit() {
  emit("workdone");
}

const props = defineProps({
  id: {
    type: Number,
    default: 0,
  },
  title: {
    type: String,
    default: "",
  },
  base_price: {
    type: Number,
    default: null,
  },
  description: {
    type: String,
    default: "",
  },
  category: {
    type: String,
    default: "",
  },
  mode: {
    type: String,
    required: true,
  },
  suggestions: {
    type: Array,
    required: true,
  },
});
const notifStore = useNotifStore();
const serv_id = ref(0);
const serv_title = ref("");
const serv_bp = ref(0);
const serv_desc = ref("");
const serv_cat = ref("");
serv_id.value = props.id;
serv_title.value = props.title;
serv_bp.value = props.base_price;
serv_desc.value = props.description;
serv_cat.value = props.category;

function isNumber(value) {
  return typeof value === "number" && value > 0;
}

function make_request() {
  if (
    serv_title.value.length == 0 ||
    !isNumber(serv_bp.value) ||
    serv_cat.value.length == 0
  ) {
    notifStore.addNotif(
      "error",
      "Submission error",
      "One or more input fields empty!"
    );
    return;
  }
  const payload = {
    title: serv_title.value,
    category: serv_cat.value,
    base_price: serv_bp.value,
  };
  if (serv_desc.value.length > 0) {
    payload.description = serv_desc.value;
  }

  if (props.mode == "Create") {
    backend_req("/service", "POST", payload).then((val) => {
      if (val) {
        notifStore.addNotif(
          "success",
          "Service Added",
          "Service has been created successfully"
        );
        emit("workdone", val);
      }
    });
  } else {
    backend_req(`/service/${serv_id.value}`, "PUT", payload).then((val) => {
      if (val) {
        notifStore.addNotif(
          "success",
          "Service Modified",
          "Service has been edited successfully"
        );
        emit("workdone", val);
      }
    });
  }
}
</script>

<style></style>
