import { staffClient } from '../staff/staffClient';

export interface Staff {
  username: string;
  name: string;
  date: string;
  role?: string;
  status: number;
  createdAt?: string;
  deletedAt?: string | null;
}

export interface StaffListResponse {
  message: string;
  staffs: Staff[];
}

export interface StaffDetailResponse {
  message: string;
  staff: Staff;
}

export interface BaseResponse {
  message: string;
}

export const AdminStaffAPI = {
  async getAllStaffs(): Promise<StaffListResponse> {
    const { data } = await staffClient.get<StaffListResponse>('/admin/staffs');
    return data;
  },

  async getStaff(username: string): Promise<StaffDetailResponse> {
    const { data } = await staffClient.get<StaffDetailResponse>(`/admin/staff/${username}`);
    return data;
  },

  async createStaff(payload: {
    name: string;
    date: string;
    username: string;
    password: string;
  }): Promise<BaseResponse> {
    const { data } = await staffClient.post<BaseResponse>('/admin/newStaff', payload);
    return data;
  },

  async deleteStaff(username: string): Promise<BaseResponse> {
    const { data } = await staffClient.post<BaseResponse>(`/admin/deleteStaff/${username}`);
    return data;
  },

  async getDeletedStaffs(): Promise<StaffListResponse> {
    const { data } = await staffClient.get<StaffListResponse>('/admin/trash/deletedStaffs');
    return data;
  },

  async restoreStaff(username: string): Promise<{ message: string }> {
    const { data } = await staffClient.post<{ message: string }>(`/admin/restoreStaff/${username}`);
    return data;
  },
};
