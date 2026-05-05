'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { Button } from '@/components/ui/button';

type ProtectedRouteProps = {
  children: React.ReactNode;
  redirectTo?: string;
};

export default function ProtectedRouteCustomer({
  children,
  redirectTo = '/auth/login',
}: ProtectedRouteProps) {
  const { isAuthenticated, loading, user } = useCustomerAuth();
  const router = useRouter();
  const [denied, setDenied] = useState(false);

  useEffect(() => {
    if (loading) return;

    // ❌ Không đăng nhập → về trang login
    if (!isAuthenticated) {
      router.replace(redirectTo);
      return;
    }

    // ❌ Token thuộc loại STAFF hoặc ADMIN → không cho vào khu customer
    if (user && user.role !== 'customer') {
      setDenied(true);
      return;
    }
  }, [loading, isAuthenticated, redirectTo, router, user]);

  // 🔄 Loading UI
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-gray-500">
        Đang kiểm tra quyền truy cập...
      </div>
    );
  }

  // ❌ Không đúng role → Access Denied UI
  if (denied) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <h2 className="text-2xl font-bold text-red-600">Access Denied</h2>
        <p className="text-gray-600">Bạn không có quyền truy cập khu vực dành cho khách hàng.</p>

        <div className="flex gap-4">
          <Button onClick={() => router.push('/')}>⬅️ Quay về trang chủ</Button>

          <Button variant="secondary" onClick={() => router.push('/auth/login')}>
            Đăng nhập bằng tài khoản khác
          </Button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
