<template>
  <div class="searchBox">
    <input
      class="searchInput"
      type="text"
      v-model="search_query"
      placeholder="Search Professional's name, Service name or a Service category"
    />
    <button class="searchButton" @click="search_profess">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="29"
        height="29"
        viewBox="0 0 29 29"
        fill="none"
      >
        <g clip-path="url(#clip0_2_17)">
          <g filter="url(#filter0_d_2_17)">
            <path
              d="M23.7953 23.9182L19.0585 19.1814M19.0585 19.1814C19.8188 18.4211 20.4219 17.5185 20.8333 16.5251C21.2448 15.5318 21.4566 14.4671 21.4566 13.3919C21.4566 12.3167 21.2448 11.252 20.8333 10.2587C20.4219 9.2653 19.8188 8.36271 19.0585 7.60242C18.2982 6.84214 17.3956 6.23905 16.4022 5.82759C15.4089 5.41612 14.3442 5.20435 13.269 5.20435C12.1938 5.20435 11.1291 5.41612 10.1358 5.82759C9.1424 6.23905 8.23981 6.84214 7.47953 7.60242C5.94407 9.13789 5.08145 11.2204 5.08145 13.3919C5.08145 15.5634 5.94407 17.6459 7.47953 19.1814C9.01499 20.7168 11.0975 21.5794 13.269 21.5794C15.4405 21.5794 17.523 20.7168 19.0585 19.1814Z"
              stroke="white"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
              shape-rendering="crispEdges"
            ></path>
          </g>
        </g>
        <defs>
          <filter
            id="filter0_d_2_17"
            x="-0.418549"
            y="3.70435"
            width="29.7139"
            height="29.7139"
            filterUnits="userSpaceOnUse"
            color-interpolation-filters="sRGB"
          >
            <feFlood flood-opacity="0" result="BackgroundImageFix"></feFlood>
            <feColorMatrix
              in="SourceAlpha"
              type="matrix"
              values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
              result="hardAlpha"
            ></feColorMatrix>
            <feOffset dy="4"></feOffset>
            <feGaussianBlur stdDeviation="2"></feGaussianBlur>
            <feComposite in2="hardAlpha" operator="out"></feComposite>
            <feColorMatrix
              type="matrix"
              values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"
            ></feColorMatrix>
            <feBlend
              mode="normal"
              in2="BackgroundImageFix"
              result="effect1_dropShadow_2_17"
            ></feBlend>
            <feBlend
              mode="normal"
              in="SourceGraphic"
              in2="effect1_dropShadow_2_17"
              result="shape"
            ></feBlend>
          </filter>
          <clipPath id="clip0_2_17">
            <rect
              width="28.0702"
              height="28.0702"
              fill="white"
              transform="translate(0.403503 0.526367)"
            ></rect>
          </clipPath>
        </defs>
      </svg>
    </button>
  </div>
  <div class="search-radio-inputs">
  <label class="search-radio">
    <input type="radio" name="radio" v-model="search_filter" value="none">
    <span class="search-rname">None</span>
  </label>
  <label class="search-radio">
    <input type="radio" name="radio" v-model="search_filter" value="pincode">
    <span class="search-rname">Pincode</span>
  </label>
  <label class="search-radio">
    <input type="radio" name="radio" v-model="search_filter" value="city">
    <span class="search-rname">City</span>
  </label>
  <label class="search-radio">
    <input type="radio" name="radio" v-model="search_filter" value="state">
    <span class="search-rname">State</span>
  </label>
</div>
  <div id="wifi-loader" v-show="showSearchingLoader">
    <svg class="circle-outer" viewBox="0 0 86 86">
      <circle class="back" cx="43" cy="43" r="40"></circle>
      <circle class="front" cx="43" cy="43" r="40"></circle>
      <circle class="new" cx="43" cy="43" r="40"></circle>
    </svg>
    <svg class="circle-middle" viewBox="0 0 60 60">
      <circle class="back" cx="30" cy="30" r="27"></circle>
      <circle class="front" cx="30" cy="30" r="27"></circle>
    </svg>
    <svg class="circle-inner" viewBox="0 0 34 34">
      <circle class="back" cx="17" cy="17" r="14"></circle>
      <circle class="front" cx="17" cy="17" r="14"></circle>
    </svg>
    <div class="text" data-text="Searching"></div>
  </div>
  <div class="worker-card" v-for="pdata in searchResultsfiltered" :key="pdata.id">
    <div class="worker-subcard1">
      <div class="infor-div">
        <h1>{{ pdata.name }}</h1>
        <p>
          {{ pdata.address.base_address }}, {{ pdata.address.city }}-{{
            pdata.address.pincode
          }}, {{ pdata.address.state }}, Contact: {{ pdata.contact_no }}
        </p>
        <div class="card-service-container">
          <h2>Service Offered: {{ getService(pdata.service_id).title }}</h2>
          <h4>{{ getService(pdata.service_id).category }}</h4>
        </div>
        <p>
          Service Description: {{ getService(pdata.service_id).description }}
        </p>
      </div>
      <div class="ratings-div">
        <div
          style="
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 7px;
          "
        >
          <i
            class="fa-solid fa-star"
            v-for="i in getStars(pdata.rating, pdata.num_raters)"
            :key="i"
          ></i
          ><i
            class="fa-regular fa-star"
            v-for="i in (5 - getStars(pdata.rating, pdata.num_raters))"
            :key="i"
          ></i>
        </div>
        <p class="review-show" @click="showReview(pdata.id)">Show Reviews</p>
      </div>
    </div>
    <div class="worker-subcard2">
      <div class="infor-div-2">
        <p>Experience : {{pdata.experience}} years</p>
        <p>
          Professional Description: {{pdata.description}}
        </p>
      </div>
      <div class="worker-actions-div">
        <p>Base Charge: &#8377;{{getService(pdata.service_id).base_price}}</p>
        <p>Fee: &#8377;{{pdata.fees}} {{pdata.fees_unit}}</p>
        <button class="tab-btn tab-btn-create worker-cardbtn" @click="book_service(pdata.id)">
          Book Service
        </button>
      </div>
    </div>
  </div>
<ShowReviewComp :pid="currentReview" v-if="showWorkerReview" @closerev="closeWorkerReview"/>
<Teleport to="body">
  <ModalComp @destroymodal="killBooker" v-if="showBooker">
    <h1 class="component-head">Pick date for Service!</h1>
    <div class="input-container">
      <input
        class="input-field"
        type="date"
        v-model="service_Date"
        :min="new Date(Date.now() + 86400000).toISOString().split('T')[0]"
      />
      <label for="input-field" class="input-label">Date for service</label>
      <span class="input-highlight"></span>
    </div>
    <button class="modal-re-btn" @click="confirm_service">Send Service Request</button>
  </ModalComp>
</Teleport>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";
import { onMounted, ref, watch } from "vue";
import ShowReviewComp from "../workercomponents/ShowReviews.vue"
import ModalComp from "../essentials/Modal.vue"

const notifStore = useNotifStore();
const search_query = ref(null);
const showSearchingLoader = ref(false);
const searchResults = ref(null);
const searchResultsfiltered = ref(null);
const servicesData = ref(null);
const search_filter = ref("none");
const service_Date = ref(null);
const showBooker = ref(false);
const props = defineProps({
  "cdata":{
    type:Object,
    required:true
  }
})

onMounted(() => {
  backend_req("/service", "GET", null).then((val) => {
    if (val) {
      servicesData.value = val;
    }
  });
});

const currentReview=ref(null);
const showWorkerReview=ref(false);

function search_profess() {
  const pattern = /^[a-zA-Z0-9]+$/;
  if (!pattern.test(search_query.value)) {
    notifStore.addNotif(
      "error",
      "Cannot Search",
      "Search query contains invalid characters!"
    );
    return;
  }
  searchResults.value = [];
  searchResultsfiltered.value = [];
  search_filter.value = "none";
  showSearchingLoader.value = true;
  backend_req(`/professional/search?q=${search_query.value}`, "GET", null).then(
    (val) => {
      showSearchingLoader.value = false;
      if (val) {
        if (val.length == 0) {
          notifStore.addNotif(
            "error",
            "0 Results found",
            "No professionals found for given search query"
          );
        } else {
          notifStore.addNotif(
            "success",
            `${val.length} Results found`,
            "Professionals found for given search query!"
          );
          searchResults.value = val;
          searchResultsfiltered.value = val;
          search_query.value = "";
        }
      }
    }
  );
}
function getService(servId) {
  return servicesData.value.find((s) => {
    if (s.id == servId) return true;
  });
}
function getStars(rating, raters) {
  if (raters == 0) return 0;
  return Math.floor(rating / raters);
}
watch(search_filter,(newval,oldval)=>{
  if(searchResults.value){
    if(newval=="none"){
      searchResultsfiltered.value = searchResults.value;
    }
    else if(newval=="pincode"){
      searchResultsfiltered.value = searchResults.value.filter((s)=>{
        if(s.address.pincode == props.cdata.address.pincode) return true;
        return false
      })
    }
    else if(newval=="city"){
      searchResultsfiltered.value = searchResults.value.filter((s)=>{
        if(s.address.city == props.cdata.address.city) return true;
        return false
      })
    }
    else if(newval=="state"){
      searchResultsfiltered.value = searchResults.value.filter((s)=>{
        if(s.address.state == props.cdata.address.state) return true;
        return false
      })
    }
  }
})

function showReview(pid){
  currentReview.value = pid;
  showWorkerReview.value = true;
}
function closeWorkerReview(){
  showWorkerReview.value = false;
}
const bookingFor = ref(null);
function book_service(pid){
  showBooker.value = true;
  bookingFor.value = pid;
}
function killBooker(){
  showBooker.value = false;
  bookingFor.value = null;
}
 
function confirm_service(){
  if(!service_Date.value){
    notifStore.addNotif("error","Date not selected","Select a date to make request!")
    killBooker();
    return;
  }
  const payload = {
    professional_id:bookingFor.value,
    dateofservice:service_Date.value
  }
  backend_req("/service/request","POST",payload).then((val)=>{
    killBooker();
    if(val){
      notifStore.addNotif("success","Request Made","Service Request made successfully!");
    }
  })
}
</script>

<style>
.searchBox {
  display: flex;
  width: 60%;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  background: var(--darkgrey1);
  border-radius: 50px;
  position: relative;
  margin: 45px auto 10px;
}

.searchButton {
  color: white;
  position: absolute;
  right: 8px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(
    --gradient-2,
    linear-gradient(90deg, #2af598 0%, #009efd 100%)
  );
  border: 0;
  display: inline-block;
  transition: all 300ms cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}
/*hover effect*/
.searchButton:hover {
  color: #fff;
  background-color: #1a1a1a;
  box-shadow: rgba(0, 0, 0, 0.5) 0 10px 20px;
  transform: translateY(-3px);
}
/*button pressing effect*/
.searchButton:active {
  box-shadow: none;
  transform: translateY(0);
}

.searchInput {
  border: none;
  background: none;
  outline: none;
  color: black;
  font-size: 20px;
  padding: 18px 36px 18px 20px;
  width: 100%;
}

.searchBox:has(.searchInput:focus) {
  box-shadow: 0 0 1em #2ab7ca44;
}

#wifi-loader {
  --background: #62abff;
  --front-color: #4f29f0;
  --back-color: #c3c8de;
  --text-color: #414856;
  width: 64px;
  height: 64px;
  border-radius: 50px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 85px auto 10px;
  transform: scale(1.5);
}

#wifi-loader svg {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
}

#wifi-loader svg circle {
  position: absolute;
  fill: none;
  stroke-width: 6px;
  stroke-linecap: round;
  stroke-linejoin: round;
  transform: rotate(-100deg);
  transform-origin: center;
}

#wifi-loader svg circle.back {
  stroke: var(--back-color);
}

#wifi-loader svg circle.front {
  stroke: var(--front-color);
}

#wifi-loader svg.circle-outer {
  height: 86px;
  width: 86px;
}

#wifi-loader svg.circle-outer circle {
  stroke-dasharray: 62.75 188.25;
}

#wifi-loader svg.circle-outer circle.back {
  animation: circle-outer135 1.8s ease infinite 0.3s;
}

#wifi-loader svg.circle-outer circle.front {
  animation: circle-outer135 1.8s ease infinite 0.15s;
}

#wifi-loader svg.circle-middle {
  height: 60px;
  width: 60px;
}

#wifi-loader svg.circle-middle circle {
  stroke-dasharray: 42.5 127.5;
}

#wifi-loader svg.circle-middle circle.back {
  animation: circle-middle6123 1.8s ease infinite 0.25s;
}

#wifi-loader svg.circle-middle circle.front {
  animation: circle-middle6123 1.8s ease infinite 0.1s;
}

#wifi-loader svg.circle-inner {
  height: 34px;
  width: 34px;
}

#wifi-loader svg.circle-inner circle {
  stroke-dasharray: 22 66;
}

#wifi-loader svg.circle-inner circle.back {
  animation: circle-inner162 1.8s ease infinite 0.2s;
}

#wifi-loader svg.circle-inner circle.front {
  animation: circle-inner162 1.8s ease infinite 0.05s;
}

#wifi-loader .text {
  position: absolute;
  bottom: -40px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-transform: lowercase;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.2px;
}

#wifi-loader .text::before,
#wifi-loader .text::after {
  content: attr(data-text);
}

#wifi-loader .text::before {
  color: var(--text-color);
}

#wifi-loader .text::after {
  color: var(--front-color);
  animation: text-animation76 3.6s ease infinite;
  position: absolute;
  left: 0;
}

@keyframes circle-outer135 {
  0% {
    stroke-dashoffset: 25;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 301;
  }

  80% {
    stroke-dashoffset: 276;
  }

  100% {
    stroke-dashoffset: 276;
  }
}

@keyframes circle-middle6123 {
  0% {
    stroke-dashoffset: 17;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 204;
  }

  80% {
    stroke-dashoffset: 187;
  }

  100% {
    stroke-dashoffset: 187;
  }
}

@keyframes circle-inner162 {
  0% {
    stroke-dashoffset: 9;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 106;
  }

  80% {
    stroke-dashoffset: 97;
  }

  100% {
    stroke-dashoffset: 97;
  }
}

@keyframes text-animation76 {
  0% {
    clip-path: inset(0 100% 0 0);
  }

  50% {
    clip-path: inset(0);
  }

  100% {
    clip-path: inset(0 0 0 100%);
  }
}
</style>

<style>
.worker-card {
  margin: 15px auto 5px;
  width: 70%;
  padding: 10px 25px 0 20px;
  border-radius: 16px;
  background-color: var(--mygrey);
  display: flex;
  flex-direction: column;
  transition: all 0.5s;
}
.worker-card:hover {
  z-index: 3;
  border: 2px solid var(--darkgrey3);
  transform: scale(1.05);
}
.worker-subcard1,
.worker-subcard2 {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-top: 7px;
}
.worker-subcard2 p {
  margin-top: 5px;
}
.infor-div,
.infor-div-2 {
  width: 80%;
}
.infor-div p,
.infor-div-2 p {
    font-size: 18px;
    margin-top: 5px;
}
.infor-div h1 {
  font-size: 45px;
}

.worker-actions-div,
.ratings-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
.fa-star.fa-solid {
  color: var(--mygreen);
}
.fa-star {
  font-size: 20px;
}
.ratings-div {
  margin-top: 20px;
  margin-right: 15px;
}
.worker-actions-div {
  transform: translateY(-30px);
}
.worker-actions-div p,
.ratings-div p {
  margin-top: 3px;
}
.worker-cardbtn {
  margin-top: 10px !important;
  border: 2px solid var(--mygreen) !important;
  font-size: 20px;
}
.worker-cardbtn:hover {
  color: var(--mygreen);
  background-color: var(--mygrey);
  border: 2px solid var(--mygreen);
}
.review-show {
  color: #4f29f0;
  cursor: pointer;
  text-decoration: #4f29f0 underline;
}
.review-show:hover {
  color: var(--myred);
  text-decoration: var(--myred) underline;
}
.card-service-container {
  margin: 10px 0;
  display: flex;
  align-items: center;
}
.card-service-container h4 {
  padding: 7px;
  background-color: var(--myyellow);
  border-radius: 5px;
  margin-left: 10px;
  font-weight: 400;
}
</style>

<style>
.search-radio-inputs {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  border-radius: 0.5rem;
  background-color: #EEE;
  box-sizing: border-box;
  box-shadow: 0 0 0px 1px rgba(0, 0, 0, 0.06);
  padding: 0.25rem;
  width: 300px;
  font-size: 14px;
  margin: 5px auto 40px;
}

.search-radio-inputs .search-radio {
  flex: 1 1 auto;
  text-align: center;
}

.search-radio-inputs .search-radio input {
  display: none;
}

.search-radio-inputs .search-radio .search-rname {
  display: flex;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  border: none;
  padding: .5rem 0;
  color: rgba(51, 65, 85, 1);
  transition: all .15s ease-in-out;
}

.search-radio-inputs .search-radio input:checked + .search-rname {
  background-color: #fff;
  font-weight: 600;
}
</style>

<style>
.modal-re-btn{
  text-align: center;
  padding: 10px;
  color: white;
  background-color: var(--mygreen);
  font-size: 22px;
  border-radius: 10px;
  margin: 15px 20vw;
  cursor: pointer;
  border: 2px solid var(--mygreen);
  transition: all 0.5s;
  font-weight: bold;
}
.modal-re-btn:hover{
  color:var(--mygreen);
  background-color: var(--mygrey);
}
</style>