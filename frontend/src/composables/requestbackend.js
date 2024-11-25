import { useNotifStore } from "../stores/notificationstore";
import { useUserStore } from "../stores/userstore";

export async function backend_req(endpoint, typeofreq, payload) {
    const notifStore = useNotifStore();
    const userStore = useUserStore();

    const options = {
        method: typeofreq,
        headers: {
            Authorization: `Bearer ${userStore.access_token}`
        }
    }
    if (payload != null) {
        if (payload instanceof FormData) {
            options.body = payload;
        } else {
            options.body = JSON.stringify(payload);
            options.headers["Content-Type"] = "application/json"
        }
    }
    try {
        const req = await fetch(`http://localhost:5000${endpoint}`, options);
        const response = await req.json();
        if (req.ok) {
            return response;
        }
        else {
            // maybe access token expired
            if (response["message"] == "Token is expired") {
                try {
                    await userStore.refresh_accestoken();
                    //retry now
                    return await backend_req(endpoint, typeofreq, payload);
                } catch (error) { }
            }
            else {
                for (const key in response.errors) {
                    notifStore.addNotif("error", "Request Error", response.errors[key]);
                }
            }
        }
    }
    catch (error) {
        notifStore.addNotif("error", "Error", error.message);
    }
    return false;
}