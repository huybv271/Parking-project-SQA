'use client';

import React, { createContext, useContext, useCallback, useEffect, useState } from 'react';

import { StaffAuthAPI } from '@/lib/api/staff/StaffAuth';
import { StaffUser, LoginData } from '@/lib/api/types';
import { getStaffToken, setStaffToken, clearStaffTokens } from '@/lib/auth_token';

type StaffAuthContextType = {
  staff: StaffUser | null;
  loading: boolean;
  isAuthenticated: boolean;

  loginStaff: (payload: LoginData) => Promise<void>;
  logoutStaff: () => void;
  refreshStaff: () => Promise<void>;
};

const StaffAuthContext = createContext<StaffAuthContextType | undefined>(undefined);

export function StaffAuthProvider({ children }: { children: React.ReactNode }) {
  const [staff, setStaff] = useState<StaffUser | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * 🔹 Lấy thông tin staff hiện tại (STAFF hoặc ADMIN)
   */
  const fetchCurrentStaff = useCallback(async () => {
    const token = getStaffToken();

    if (!token) {
      setStaff(null);
      setLoading(false);
      return;
    }

    try {
      const res = await StaffAuthAPI.getCurrentStaff();
      setStaff(res.staff);
    } catch (err) {
      console.error('Fetch staff failed:', err);
      clearStaffTokens();
      setStaff(null);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * 🔐 LOGIN (dùng chung cho staff + admin)
   */
  const loginStaff = useCallback(
    async (payload: LoginData) => {
      const res = await StaffAuthAPI.loginStaff(payload);

      if (!res?.token) {
        throw new Error('Login failed');
      }

      setStaffToken(res.token, '');
      await fetchCurrentStaff();
    },
    [fetchCurrentStaff]
  );

  /**
   * 🚪 LOGOUT
   */
  const logoutStaff = useCallback(() => {
    clearStaffTokens();
    setStaff(null);

    if (typeof window !== 'undefined') {
      window.location.href = '/staff/auth/login';
    }
  }, []);

  /**
   * 🔄 REFRESH (khi cần)
   */
  const refreshStaff = useCallback(async () => {
    setLoading(true);
    await fetchCurrentStaff();
  }, [fetchCurrentStaff]);

  /**
   * 🚀 INIT
   */
  useEffect(() => {
    fetchCurrentStaff();
  }, [fetchCurrentStaff]);

  return (
    <StaffAuthContext.Provider
      value={{
        staff,
        loading,
        isAuthenticated: !!staff && !!getStaffToken(),
        loginStaff,
        logoutStaff,
        refreshStaff,
      }}
    >
      {children}
    </StaffAuthContext.Provider>
  );
}

/**
 * 🪝 Hook
 */
export function useStaffAuth() {
  const context = useContext(StaffAuthContext);
  if (!context) {
    throw new Error('useStaffAuth must be used within StaffAuthProvider');
  }
  return context;
}
