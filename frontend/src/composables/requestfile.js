import { useNotifStore } from "../stores/notificationstore";
import { useUserStore } from "../stores/userstore";

export async function backend_req_file(endpoint, typeofreq) {
    const notifStore = useNotifStore();
    const userStore = useUserStore();

    const options = {
        method: typeofreq,
        headers: {
            Authorization: `Bearer ${userStore.access_token}`
        }
    }
    try {
        const req = await fetch(`http://localhost:5000${endpoint}`, options);
        if (req.ok) {
            const blob = await req.blob();
            const url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        }
        else {
            // maybe access token expired
            const response = await req.json();
            if (response["message"] == "Token is expired") {
                try {
                    await userStore.refresh_accestoken();
                    //retry now
                    await backend_req_file(endpoint, typeofreq);
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
}