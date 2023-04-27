import axios from 'axios'

const http = axios.create({
    baseURL: process.env.VUE_APP_PAWL_MS_API_URL,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
    }
});

export default http


