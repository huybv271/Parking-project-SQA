'use client';

import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function StaffDashboard() {
  const { staff, isAuthenticated, loading } = useStaffAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;

    if (!isAuthenticated || !staff) {
      router.replace('/staff/auth/login');
      return;
    }

    if (staff.role === 'admin') {
      router.replace('/admin/dashboard');
    }
  }, [staff, isAuthenticated, loading, router]);

  if (loading) {
    return <div className="p-8 text-gray-600">🔐 Đang xác thực tài khoản...</div>;
  }

  if (!staff || staff.role !== 'staff') return null;

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-green-700">👋 Chào mừng, {staff.name}</h1>
        <p className="text-gray-600">
          Bạn đang đăng nhập với vai trò <span className="font-medium">Staff. </span>
          Chúc bạn có 1 ngày làm việc hiệu quả!
        </p>
      </div>

      {/* Profile card */}
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">📌 Thông tin tài khoản</h2>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Username</p>
            <p className="font-medium">{staff.username}</p>
          </div>

          <div>
            <p className="text-gray-500">Vai trò</p>
            <p className="font-medium capitalize">{staff.role}</p>
          </div>

          <div>
            <p className="text-gray-500">Trạng thái</p>
            <p className="font-medium text-green-600">Hoạt động</p>
          </div>
        </div>
      </div>
    </div>
  );
}
