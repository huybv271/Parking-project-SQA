import { customerClient } from '../customer/customerClient';

import {
  LoginData,
  RegisterData,
  CustomerLoginResponse,
  CustomerInfoResponse,
  RegisterResponse,
  VerifyEmailResponse,
  ResendVerifyResponse,
  ResetPasswordResponse,
  SendBarcodeResponse,
} from '../types';
import { setCustomerToken, getCustomerToken, clearCustomerTokens } from '../../auth_token';

const USER_BASE = process.env.NEXT_PUBLIC_USER_BASE || '/user';

export const customerAuthAPI = {
  async loginCustomer(payload: LoginData): Promise<CustomerLoginResponse> {
    const requestPayload = {
      username: payload.username,
      password: payload.password,
    };

    console.log('Login request:', {
      baseURL: customerClient.defaults.baseURL,
      url: `${USER_BASE}/login`,
      payload: requestPayload,
    });

    try {
      const { data } = await customerClient.post<CustomerLoginResponse>(
        `${USER_BASE}/login`,
        requestPayload
      );
      if (data?.token) {
        setCustomerToken(data.token, '');
        // Nếu BE trả về user info trong login response
        // if (data.user) {
        //   // Có thể lưu user info vào context ở đây hoặc trong AuthContext
        // }
      }
      return data;
    } catch (error: any) {
      console.error('Login error:', error?.response?.data || error.message);
      throw error;
    }
  },

  async registerCustomer(payload: RegisterData): Promise<RegisterResponse> {
    const { data } = await customerClient.post<RegisterResponse>(`${USER_BASE}/signup`, payload);
    return data;
  },

  async getCurrentUser(): Promise<CustomerInfoResponse> {
    const { data } = await customerClient.get<CustomerInfoResponse>(`${USER_BASE}/infor`);
    return data;
  },

  async verifyEmail(token: string): Promise<VerifyEmailResponse> {
    const { data } = await customerClient.post<VerifyEmailResponse>(`${USER_BASE}/verify-email`, {
      token,
    });
    return data;
  },

  async resendVerify(gmail: string): Promise<ResendVerifyResponse> {
    const { data } = await customerClient.post<ResendVerifyResponse>(`${USER_BASE}/resend-verify`, {
      gmail,
    });
    return data;
  },

  async sendResetBarcode(gmail: string): Promise<SendBarcodeResponse> {
    const { data } = await customerClient.post<SendBarcodeResponse>(`${USER_BASE}/send-barcode`, {
      gmail,
    });
    return data;
  },

  async resetPassword(
    gmail: string,
    token: string,
    password: string
  ): Promise<ResetPasswordResponse> {
    const { data } = await customerClient.post<ResetPasswordResponse>(
      `${USER_BASE}/forget-password`,
      {
        gmail,
        token,
        password,
      }
    );
    return data;
  },

  logout(): void {
    clearCustomerTokens();
  },
};
