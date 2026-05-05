import { staffClient } from '../staff/staffClient';

export interface ParkingStatus {
  id: number;
  area: string;
  position: string;
  vehicleType: 'CAR' | 'MOTORBIKE';
  status: 'AVAILABLE' | 'BOOKED' | 'OCCUPIED' | 'LOCKED';
  color: string;
  channel: 'ONLINE' | 'OFFLINE' | 'NONE';
}

export interface ParkingMonitorResponse {
  mapStatus: ParkingStatus[];
  availableSlot: number;
  occupiedSlot: number;
  bookedSlot: number;
  lockedSlot: number;
}

export const ParkingMonitorAPI = {
  getRealtimeStatus: async (): Promise<ParkingMonitorResponse> => {
    const { data } = await staffClient.get('/admin/slot-available');
    return data;
  },
};
