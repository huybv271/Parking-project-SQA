'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useStaffAuth } from '@/contexts/StaffAuthContext';
import Link from 'next/link';

type ProtectedRouteAdminProps = {
  children: React.ReactNode;
  redirectTo?: string;
};

export default function ProtectedRouteAdmin({
  children,
  redirectTo = '/staff/auth/login',
}: ProtectedRouteAdminProps) {
  const { isAuthenticated, staff, loading } = useStaffAuth();
  const router = useRouter();

  const [accessDenied, setAccessDenied] = useState(false);

  useEffect(() => {
    if (loading) return;

    if (!isAuthenticated) {
      router.replace('/');
      return;
    }

    if (!staff || staff.role !== 'admin') {
      setAccessDenied(true);
      return;
    }

    setAccessDenied(false);
  }, [loading, isAuthenticated, staff, router, redirectTo]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-gray-500">
        Đang kiểm tra quyền truy cập...
      </div>
    );
  }

  // ❌ Access Denied UI
  if (accessDenied) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-6">
        <h1 className="text-2xl font-bold text-red-600">Access Denied</h1>
        <p className="text-center text-gray-600">
          Chỉ tài khoản <strong>Admin</strong> mới được phép truy cập khu vực này.
        </p>

        <div className="flex gap-4">
          <Link href="/" className="rounded-md bg-gray-200 px-4 py-2 hover:bg-gray-300">
            ⬅ Trang chủ
          </Link>

          <Link
            href="/staff/auth/login"
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            🔐 Đăng nhập lại
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
