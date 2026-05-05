import { staffClient } from '../staff/staffClient';

export interface CreateSpotPayload {
  area: string;
  slotNumber: number;
  vehicleType: 'CAR' | 'MOTORBIKE';
  slotType: 'ONLINE' | 'OFFLINE';
}

export interface EditSpotPayload {
  isActive: number; // 1 | 0
}

export type VehicleType = 'CAR' | 'MOTORBIKE';
export type SlotType = 'ONLINE' | 'OFFLINE';

export interface Spot {
  id: number;
  area: string;
  position: number;
  vehicleType: VehicleType;
  slotType: SlotType;
  status: number;
  isActive: number;
  createdAt?: string;
  updatedAt?: string;
  deletedAt?: string | null;
}

export interface SpotListResponse {
  message: string;
  spots: Spot[];
}
export interface DeletedSpotsResponse {
  message: string;
  spots: Spot[];
}

export interface SpotDetailResponse {
  message: string;
  spot: Spot;
}

/* ================= API ================= */

export const AdminSpotAPI = {
  async createSpot(payload: CreateSpotPayload): Promise<{ message: string }> {
    const { data } = await staffClient.post<{ message: string }>('/admin/newSpots', payload);
    return data;
  },

  async editSpot(spotId: number, payload: EditSpotPayload): Promise<{ message: string }> {
    const { data } = await staffClient.post<{ message: string }>(
      `/admin/editSpot/${spotId}`,
      payload
    );
    return data;
  },

  async deleteSpot(spotId: number): Promise<{ message: string }> {
    const { data } = await staffClient.post<{ message: string }>(`/admin/deleteSpot/${spotId}`);
    return data;
  },

  async restoreSpot(spotId: number): Promise<{ message: string }> {
    const { data } = await staffClient.post<{ message: string }>(`/admin/restoreSpot/${spotId}`);
    return data;
  },

  async getDeletedSpots(): Promise<DeletedSpotsResponse> {
    const { data } = await staffClient.get<DeletedSpotsResponse>('/admin/trash/deletedSpots');
    return data;
  },

  async getSpotByArea(area: string): Promise<SpotListResponse> {
    const { data } = await staffClient.get<SpotListResponse>(`/admin/spots/area/${area}`);
    return data;
  },

  async getSpotDetail(spotId: number): Promise<SpotDetailResponse> {
    const { data } = await staffClient.get<SpotDetailResponse>(`/admin/spots/${spotId}`);
    return data;
  },
};
