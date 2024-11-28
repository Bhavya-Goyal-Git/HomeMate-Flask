<template>
    <Teleport to="body">
    <ModalComp @destroymodal="closeReviews">
        <h1 style="text-align:center; margin-bottom:15px">Professional Reviews</h1>
        <div class="reviews-cont" v-if="reviewsData">
            <div class="one-review" v-for="rw in reviewsData" :key="rw.id">
                <h2>{{rw.customer_name}}</h2>
                <div class="star-cont-flex">
                    <i class="fa-solid fa-star" v-for="i in rw.stars" :key="i"></i>
                    <i class="fa-regular fa-star" v-for="i in (5-rw.stars)" :key="i"></i>
                    <p>{{rw.dateofreview}}</p>
                </div>
                <p>{{rw.review}}</p>
            </div>
        </div>
        <div class="error-div" v-else><h1>No reviews available for this professional!</h1></div>
    </ModalComp>
  </Teleport>
</template>

<script setup>
import { onMounted, ref } from "vue";
import ModalComp from "../essentials/Modal.vue";
import { backend_req } from "../../composables/requestbackend";
import { useNotifStore } from "@/stores/notificationstore";

const props = defineProps({
    pid:{
        type:Number, //professional's id
        required:true
    }
});

const reviewsData = ref(null);
onMounted(()=>{
    backend_req(`/professional/review/${props.pid}`,"GET",null).then((val)=>{
        if(val && val.length>0){
            reviewsData.value = val;
        }
    })
})
const emit = defineEmits(["closerev"]);
function closeReviews(){
    emit("closerev");
}

</script>

<style>
.reviews-cont{
    display: flex;
    flex-wrap: wrap;
}
.one-review{
    padding: 15px;
    border-radius: 10px;
    background-color: var(--mygrey);
    margin: 10px;
}
.star-cont-flex{
    display: flex;
    margin: 10px 0;
}
.star-cont-flex p{
    margin-left: 6px;
    color: #000000bb;
}
</style>