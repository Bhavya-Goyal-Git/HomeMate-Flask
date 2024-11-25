<template>
  <h1 class="page-head">Professional Complete Registeration</h1>
  <div class="serv-ch">
    <h2>
      Service Chosen: <span class="service-tt">{{ chosenService.title }}</span>
    </h2>
    <button class="tab-btn tab-btn-create" @click="changeServ = true">
      Choose Service
    </button>
  </div>
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
          name="pincode"
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
    <div class="addressdiv">
      <div class="input-container pincode-cont">
        <input
          placeholder="Fee"
          class="input-field"
          type="number"
          name="fees"
          v-model="fees"
        />
        <label for="input-field" class="input-label">Fee Amount</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container base-add-cont">
        <input
          placeholder="Fee per unit"
          class="input-field"
          type="text"
          name="fees_unit"
          v-model="fees_unit"
        />
        <label for="input-field" class="input-label">Fee per unit</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container city-cont">
        <input
          placeholder="Experience in years"
          class="input-field"
          type="number"
          name="experience"
          v-model="experience"
        />
        <label for="input-field" class="input-label">Experience</label>
        <span class="input-highlight"></span>
      </div>
      <div class="input-container state-cont">
        <input
          placeholder="Contact number"
          class="input-field"
          type="number"
          name="contact_no"
          v-model="contact_no"
        />
        <label for="input-field" class="input-label">Contact Number</label>
        <span class="input-highlight"></span>
      </div>
    </div>
    <div class="input-container">
      <textarea
        placeholder="Description"
        class="input-field"
        type="text"
        name="description"
        v-model="description"
      />
      <label for="input-field" class="input-label">Description</label>
      <span class="input-highlight"></span>
    </div>
    <div class="document-input">
      <div>
        <span class="file-ip-span">Document for verification:</span>
        <input type="file" name="documents" @change="validateFile" />
      </div>
      <p>(Note: Please attach proof of service, pdf only, max size 1MB)</p>
    </div>
    <button class="register-button">Submit</button>
  </form>
  <ServiceChooserComp v-if="changeServ" @servicechosen="set_chosen_serv" />
</template>

<script setup>
import { ref, watch } from "vue";
import { useNotifStore } from "../../stores/notificationstore";
import { useUserStore } from "../../stores/userstore";
import { backend_req } from "../../composables/requestbackend";
import { useRouter } from "vue-router";
import ServiceChooserComp from "../../components/workercomponents/ServiceChoose.vue";

const notifStore = useNotifStore();
const userStore = useUserStore();
const router = useRouter();
const name = ref("");
const pincode = ref("");
const changeServ = ref(false);
const base_address = ref("");
const city = ref("");
const state = ref("");
const description = ref("");
const contact_no = ref(null);
const experience = ref(null);
const fees = ref(null);
const fees_unit = ref(null);
const chosenService = ref({
  title: "None",
});
let isFilevalidated = false;

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

function set_chosen_serv(servObj) {
  changeServ.value = false;
  if (servObj) {
    chosenService.value = servObj;
  }
}

function isNumber(value) {
  return typeof value === "number" && value > 0;
}

function validateFile(event) {
  const file = event.target.files[0];
  isFilevalidated = false;

  if (file) {
    const fileType = file.type;
    const fileSize = file.size;

    // Check if file is a PDF and its size is less than 1MB
    if (fileType !== "application/pdf") {
      notifStore.addNotif(
        "error",
        "Bad File",
        "Kindly upload a pdf file only!"
      );
    } else if (fileSize > 1024 * 1024) {
      notifStore.addNotif(
        "error",
        "File too big",
        "File must be smaller than 1MB"
      );
    } else {
      isFilevalidated = true;
    }
  } else {
    notifStore.addNotif("error", "File selection", "No file selected!");
  }
}

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

  if (String(contact_no.value).length != 10 || !regex.test(contact_no.value)) {
    notifStore.addNotif(
      "error",
      "Contact invalid",
      "Contact no. must be a 10 digit number"
    );
    return;
  }
  if (
    name.value.length == 0 ||
    base_address.value.length == 0 ||
    city.value.length == 0 ||
    state.value.length == 0 ||
    fees_unit.value.length == 0
  ) {
    notifStore.addNotif(
      "error",
      "Submission failed",
      "One or more input fields empty."
    );
    return;
  }
  if (!isNumber(experience.value) || !isNumber(fees.value)) {
    notifStore.addNotif(
      "error",
      "Submission failed",
      "Experience and fees must be non negative integers."
    );
    return;
  }
  if (chosenService.value.title === "None") {
    notifStore.addNotif(
      "error",
      "Submission failed",
      "Please Choose Service Type!"
    );
    return;
  }
  if (!isFilevalidated) {
    notifStore.addNotif(
      "error",
      "File selection",
      "Kindly ensure proper documents uploading."
    );
    return;
  }
  const formdata = new FormData(document.querySelector(".register-form"));
  formdata.append("service_id", chosenService.value.id);
  backend_req(`/professional/data/${userStore.uid}`, "POST", formdata).then(
    (val) => {
      if (val) {
        router.push({ name: "workerHome" });
      }
    }
  );
}
</script>

<style>
.serv-ch {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
}
.serv-ch h2 {
  margin-right: 10px;
}
.service-tt {
  color: var(--myred);
}
.document-input {
  font-size: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
}
.document-input p {
  margin-top: 5px;
  color: var(--darkgrey2);
  font-size: 15px;
}
.file-ip-span {
  margin-right: 10px;
}
</style>
