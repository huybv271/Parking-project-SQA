import axios from 'axios';
const API_BASE = 'http://localhost:8080';

export const parkingAPI = {
  getSlotStatus: async () => {
    const res = await axios.get(`${API_BASE}/user/parking/status`);
    return res.data;
  },
};
