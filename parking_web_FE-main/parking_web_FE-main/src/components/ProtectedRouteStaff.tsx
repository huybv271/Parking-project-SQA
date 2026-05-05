'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { Button } from '@/components/ui/button';

type ProtectedRouteProps = {
  children: React.ReactNode;
  requiredRole?: 'staff' | 'admin';
  redirectTo?: string;
};

export default function ProtectedRouteStaff({
  children,
  requiredRole = 'staff',
  redirectTo = '/staff/auth/login',
}: ProtectedRouteProps) {
  const { isAuthenticated, staff, loading } = useStaffAuth();
  const router = useRouter();

  const [denied, setDenied] = useState(false);

  useEffect(() => {
    if (loading) return;

    // ❌ 1. Chưa đăng nhập → về trang login staff
    if (!isAuthenticated) {
      router.replace(redirectTo);
      return;
    }

    // ❌ 2. User là admin → không được vào khu staff → chuyển sang admin dashboard
    if (staff?.role === 'admin') {
      router.replace('/admin/dashboard');
      return;
    }

    // ❌ 3. Không phải staff hoặc admin
    if (staff && staff.role !== 'staff') {
      setDenied(true);
      return;
    }

    // ❌ 4. Route yêu cầu admin (rare case)
    // ❌ 4. Route yêu cầu admin nhưng không phải admin
    // if (requiredRole === 'admin' && staff?.role !== 'admin') {
    //   setDenied(true);
    //   return;
    // }
  }, [loading, isAuthenticated, staff, requiredRole, redirectTo, router]);

  // 🔄 Loading UI
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-gray-500">
        Đang kiểm tra quyền truy cập...
      </div>
    );
  }

  // ❌ Access Denied UI
  if (denied) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <h2 className="text-2xl font-bold text-red-600">Access Denied</h2>
        <p className="text-gray-600">Bạn không có quyền truy cập khu vực dành cho nhân viên.</p>

        <div className="flex gap-4">
          <Button onClick={() => router.push('/')}>⬅️ Quay về trang chủ</Button>

          <Button variant="secondary" onClick={() => router.push('/staff/auth/login')}>
            Đăng nhập bằng tài khoản khác
          </Button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
