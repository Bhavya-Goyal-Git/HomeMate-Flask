import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotifStore = defineStore('notifStore', () => {
    const lastid = ref(2);
    const notifications = ref([
    ]);

    function addNotif(type, title, content) {
        lastid.value = lastid.value + 1;
        notifications.value.push({
            id: lastid.value,
            notifType: type,
            title: title,
            content: content
        })
    }
    function removeNotif(id) {
        notifications.value = notifications.value.filter((obj) => {
            if (obj.id != id) return true
        })
    }

    return {
        notifications,
        removeNotif,
        addNotif,
    }
})