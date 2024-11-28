import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useNotifStore } from "./notificationstore"
import { useRouter } from 'vue-router';

export const useUserStore = defineStore('userStore', () => {
    const notifStore = useNotifStore();
    const router = useRouter();
    const uid = ref("");
    const username = ref("");
    const email_address = ref("");
    const role = ref("");
    const access_token = ref("");
    const refresh_token = ref("");
    const is_loggedIn = ref(false);

    function upload_signupdata(data) {
        uid.value = data["id"];
        username.value = data["username"];
        email_address.value = data["email_address"];
        role.value = data["role"];
    }

    function upload_logindata(data) {
        access_token.value = data["access_token"];
        refresh_token.value = data["refresh_token"];
        is_loggedIn.value = true;
    }

    async function getUserData() {
        try {
            const req = await fetch("http://localhost:5000/userdata", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${access_token.value}`
                }
            });
            const response = await req.json();
            if (req.ok) {
                upload_signupdata(response);
            }
            else {
                is_loggedIn.value = false;
                notifStore.addNotif("error", "Login failed", "Could not load user data");
            }
        } catch (error) {
            notifStore.addNotif("error", "Error", error.message);
        }
    }

    async function refresh_accestoken() {
        try {
            const req = await fetch("http://localhost:5000/auth/refresh", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${refresh_token.value}`
                }
            });
            const response = await req.json();
            if (req.ok) {
                access_token.value = response["access_token"];
                return "Access token refreshed";
            }
            else {
                notifStore.addNotif("error", "Error", "User logged out, please login again");
                resetData();
                router.push({ name: 'login' });
            }
        } catch (error) {
            notifStore.addNotif("error", "Error", error.message);
        }
        return new Promise((resolve, reject) => reject("Could not refresh access token"));
    }

    function resetData() {
        uid.value = "";
        username.value = "";
        email_address.value = "";
        role.value = "";
        access_token.value = "";
        refresh_token.value = "";
        is_loggedIn.value = false;
    }

    return {
        uid,
        username,
        is_loggedIn,
        role,
        resetData,
        getUserData,
        upload_signupdata,
        upload_logindata,
        access_token,
        refresh_token,
        refresh_accestoken,
    }
})
