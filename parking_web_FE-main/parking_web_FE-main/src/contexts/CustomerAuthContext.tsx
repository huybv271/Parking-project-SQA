'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

import { customerAuthAPI } from '@/lib/api/customer/CustomerAuth';
import {
  LoginData,
  RegisterData,
  RegisterResponse,
  CustomerUser,
  VerifyEmailResponse,
  ResendVerifyResponse,
  SendBarcodeResponse,
  ResetPasswordResponse,
} from '@/lib/api/types';

import { setCustomerToken, getCustomerToken, clearCustomerTokens } from '@/lib/auth_token';

type CustomerAuthContextType = {
  user: CustomerUser | null;
  loading: boolean;
  isAuthenticated: boolean;

  loginCustomer: (payload: LoginData) => Promise<void>;
  registerCustomer: (payload: RegisterData) => Promise<RegisterResponse>;

  verifyEmail: (token: string) => Promise<VerifyEmailResponse>;
  resendVerify: (gmail: string) => Promise<ResendVerifyResponse>;
  sendResetBarcode: (gmail: string) => Promise<SendBarcodeResponse>;
  resetPassword: (gmail: string, token: string, pw: string) => Promise<ResetPasswordResponse>;

  logoutCustomer: () => void;
  refreshUser: () => Promise<void>;
};

const CustomerAuthContext = createContext<CustomerAuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CustomerUser | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * -----------------------------------------------------
   * LẤY USER HIỆN TẠI (TỪ /user/infor)
   * -----------------------------------------------------
   */
  const fetchCurrentUser = useCallback(async () => {
    try {
      const token = getCustomerToken();
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      const data = await customerAuthAPI.getCurrentUser();
      setUser(data.user);
    } catch (error) {
      console.error('Failed to fetch user info:', error);
      setUser(null);
      clearCustomerTokens();
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * -----------------------------------------------------
   * LOGIN CUSTOMER
   * -----------------------------------------------------
   */
  const loginCustomer = useCallback(
    async (payload: LoginData) => {
      const response = await customerAuthAPI.loginCustomer(payload);

      if (response.token) {
        setCustomerToken(response.token, '');
        await fetchCurrentUser();
      }
    },
    [fetchCurrentUser]
  );

  /**
   * -----------------------------------------------------
   * REGISTER CUSTOMER — TRẢ VỀ RegisterResponse
   * -----------------------------------------------------
   */
  const registerCustomer = useCallback(async (payload: RegisterData): Promise<RegisterResponse> => {
    try {
      const res = await customerAuthAPI.registerCustomer(payload);
      return res; // ⭐ Quan trọng: FE sẽ nhận message
    } catch (err) {
      console.error('Register failed:', err);
      throw err;
    }
  }, []);

  /**
   * -----------------------------------------------------
   * VERIFY EMAIL
   * -----------------------------------------------------
   */
  const verifyEmail = useCallback(async (token: string) => {
    return await customerAuthAPI.verifyEmail(token);
  }, []);

  /**
   * -----------------------------------------------------
   * RESEND VERIFY
   * -----------------------------------------------------
   */

  const resendVerify = useCallback(async (gmail: string) => {
    return await customerAuthAPI.resendVerify(gmail);
  }, []);

  /**
   * -----------------------------------------------------
   * SEND RESET BARCODE
   * -----------------------------------------------------
   */

  const sendResetBarcode = useCallback(async (gmail: string) => {
    return await customerAuthAPI.sendResetBarcode(gmail);
  }, []);

  /**
   * -----------------------------------------------------
   * RESET PASSWORD
   * -----------------------------------------------------
   */
  const resetPassword = useCallback(async (gmail: string, token: string, pw: string) => {
    return await customerAuthAPI.resetPassword(gmail, token, pw);
  }, []);

  /**
   * -----------------------------------------------------
   * LOGOUT
   * -----------------------------------------------------
   */
  const logoutCustomer = useCallback(() => {
    clearCustomerTokens();
    setUser(null);
    if (typeof window !== 'undefined') {
      window.location.href = '/auth/login';
    }
  }, []);

  /**
   * -----------------------------------------------------
   * REFRESH USER
   * -----------------------------------------------------
   */
  const refreshUser = useCallback(async () => {
    await fetchCurrentUser();
  }, [fetchCurrentUser]);

  //INIT AUTH
  useEffect(() => {
    fetchCurrentUser();
  }, [fetchCurrentUser]);

  /**
   * CONTEXT VALUE
   */
  const value: CustomerAuthContextType = {
    user,
    loading,
    isAuthenticated: !!user && !!getCustomerToken(),

    loginCustomer,
    registerCustomer,

    verifyEmail,
    resendVerify,
    sendResetBarcode,
    resetPassword,

    logoutCustomer,
    refreshUser,
  };

  return <CustomerAuthContext.Provider value={value}>{children}</CustomerAuthContext.Provider>;
}

/**
 * HOOK: useCustomerAuth
 */
export function useCustomerAuth() {
  const context = useContext(CustomerAuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider!');
  return context;
}
