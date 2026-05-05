// src/lib/api/StaffAuth.ts
import { staffClient } from './staffClient';
import { LoginData, StaffLoginResponse, StaffInfoResponse } from '../types';
import { setStaffToken, clearStaffTokens } from '../../auth_token';

const STAFF_BASE = process.env.NEXT_PUBLIC_STAFF_BASE || '/staff';

export const StaffAuthAPI = {
  async loginStaff(payload: LoginData): Promise<StaffLoginResponse> {
    const requestPayload = {
      username: payload.username,
      password: payload.password,
    };

    const { data } = await staffClient.post<StaffLoginResponse>(
      `${STAFF_BASE}/login`,
      requestPayload
    );

    if (data.token) {
      setStaffToken(data.token, '');
    }
    return data;
  },

  async getCurrentStaff(): Promise<StaffInfoResponse> {
    const { data } = await staffClient.get<StaffInfoResponse>(`${STAFF_BASE}/infor`);
    return data; // chứa {message, staff}
  },

  logout(): void {
    clearStaffTokens();
  },
};
