<template>
  <h1 class="page-head">User Complete Registeration</h1>
  <form class="register-form" @submit.prevent="make_request">
    <div class="input-container">
      <input
        placeholder="Name"
        class="input-field"
        type="text"
        name="name"
        v-model="name"
      />
      <label for="input-field" class="input-label">Name</label>
      <span class="input-highlight"></span>
    </div>
    <div class="addressdiv">
      <div class="input-container pincode-cont">
        <input
          placeholder="Pincode"
          class="input-field"
          type="text"
          name="pindcode"
          v-model="pincode"
        />
        <label for="input-field" class="input-label">Pincode</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container base-add-cont">
        <input
          placeholder="House or flat no. or Locality"
          class="input-field"
          type="text"
          name="base_address"
          v-model="base_address"
        />
        <label for="input-field" class="input-label">Base Address</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container city-cont">
        <input
          placeholder="City"
          class="input-field"
          type="text"
          name="city"
          v-model="city"
        />
        <label for="input-field" class="input-label">City</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container state-cont">
        <input
          placeholder="State"
          class="input-field"
          type="text"
          name="state"
          v-model="state"
        />
        <label for="input-field" class="input-label">State</label>
        <span class="input-highlight"></span>
      </div>
    </div>
    <button class="register-button">Submit</button>
  </form>
</template>

<script setup>
import { ref, watch } from "vue";
import { useNotifStore } from "../../stores/notificationstore";
import { useUserStore } from "../../stores/userstore";
import { backend_req } from "../../composables/requestbackend";
import { useRouter } from "vue-router";

const notifStore = useNotifStore();
const userStore = useUserStore();
const router = useRouter();
const name = ref("");
const pincode = ref("");
const base_address = ref("");
const city = ref("");
const state = ref("");

watch(pincode, async (newval, oldval) => {
  if (newval.length == 6) {
    try {
      const req = await fetch(`https://api.postalpincode.in/pincode/${newval}`);
      const response = await req.json();
      if (req.ok) {
        city.value = response[0]["PostOffice"][0]["Block"];
        state.value = response[0]["PostOffice"][0]["State"];
      } else {
        notifStore.addNotif(
          "error",
          "Error",
          "Could not find city for given pincode."
        );
      }
    } catch (error) {}
  }
});

function make_request() {
  const regex = /^[0-9]+$/;
  if (pincode.value.length != 6 || !regex.test(pincode.value)) {
    notifStore.addNotif(
      "error",
      "Pincode invalid",
      "Pincode must be a 6 digit number"
    );
    return;
  }
  if (
    name.value.length == 0 ||
    base_address.value.length == 0 ||
    city.value.length == 0 ||
    state.value.length == 0
  ) {
    notifStore.addNotif(
      "error",
      "Submission failed",
      "One or more input fields empty."
    );
    return;
  }

  const payload = {
    name: name.value,
    address: {
      base_address: base_address.value,
      pincode: pincode.value,
      city: city.value,
      state: state.value,
    },
  };
  backend_req(`/customer/data/${userStore.uid}`, "POST", payload).then(
    (val) => {
      if (val) {
        notifStore.addNotif(
          "success",
          "Data Uploaded",
          "User Registeration completed successfully."
        );
        router.push({ name: "customerHome" });
      }
    }
  );
}
</script>

<style>
.addressdiv {
  display: grid;
  grid-template-rows: 1fr 1fr;
  grid-template-columns: repeat(4, 1fr);
}
.input-container.pincode-cont {
  grid-row: 1/2;
  grid-column: 1/2;
}
.input-container.base-add-cont {
  grid-row: 1/2;
  grid-column: 2/5;
}
.input-container.city-cont {
  grid-row: 2/3;
  grid-column: 1/3;
}
.input-container.state-cont {
  grid-row: 2/3;
  grid-column: 3/5;
}
</style>
