import { useUserStore } from "../stores/userstore";
import { useNotifStore } from "../stores/notificationstore";

export async function login_user(formdata) {
    const userStore = useUserStore();
    const notifStore = useNotifStore();
    try {
        const request = await fetch("http://localhost:5000/auth/login", {
            method: "POST",
            body: formdata,
        });
        const response = await request.json();
        if (request.ok) {
            userStore.upload_logindata(response);
            notifStore.addNotif(
                "success",
                "Login Success",
                "User logged in successfully."
            );
        }
        else {
            for (const key in response.errors) {
                notifStore.addNotif("error", "LogIn Error", response.errors[key]);
            }
        }
    } catch (error) {
        notifStore.addNotif("error", "Error", error.message);
    }
}