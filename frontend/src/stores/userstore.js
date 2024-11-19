import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('userStore', () => {
    const username = ref("");
    const email_address = ref("");
    const role = ref("");
    const access_token = ref("");
    const refresh_token = ref("");
    const is_loggedIn = ref(false);

    function upload_signupdata(data) {
        username.value = data["username"];
        email_address.value = data["email_address"];
        role.value = data["role"];
    }

    function upload_logindata(data) {
        access_token.value = data["access_token"];
        refresh_token.value = data["refresh_token"];
        is_loggedIn.value = true;
    }

    return {
        upload_signupdata,
        upload_logindata
    }
})
