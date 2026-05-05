// import { adminClient } from './adminClients';

// import { LoginData, AdminLoginResponse, AdminInfoResponse } from '../types';
// import { setAdminToken, clearAdminTokens } from '@/lib/auth_token';

// const ADMIN_BASE = process.env.NEXT_PUBLIC_ADMIN_BASE || 'admin';

// export const adminAuthAPI = {
//   async loginAdmin(payload: LoginData): Promise<AdminLoginResponse> {
//     const requestPayload = {
//       username: payload.username,
//       password: payload.password,
//     };

//     const { data } = await adminClient.post<AdminLoginResponse>(
//       `${ADMIN_BASE}/login`,
//       requestPayload
//     );

//     if (data.token) {
//       setAdminToken(data.token, '');
//     }
//     return data;
//   },

//   async getCurrentAdmin(): Promise<AdminInfoResponse> {
//     const { data } = await adminClient.get<AdminInfoResponse>(`${ADMIN_BASE}/info`);
//     return data;
//   },

//   logout(): void {
//     clearAdminTokens();
//   },
// };
