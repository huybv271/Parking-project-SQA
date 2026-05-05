'use client';

import Sidebar, { SidebarItem } from '@/components/SideBar';
import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { useRouter } from 'next/navigation';

export default function StaffLayout({ children }: { children: React.ReactNode }) {
  const { staff, loading, isAuthenticated, logoutStaff } = useStaffAuth();
  const router = useRouter();

  if (loading) return null;

  // ❌ Sai role hoặc chưa login → Access Denied
  if (!isAuthenticated || !staff || staff.role !== 'staff') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-100">
        <div className="rounded-xl bg-white p-8 text-center shadow-lg">
          <h1 className="mb-4 text-2xl font-bold text-red-600">Access Denied</h1>
          <p className="mb-6 text-gray-700">Vui lòng đăng nhập với tài khoản nhân viên.</p>
          <button
            onClick={() => router.push('/auth/login')}
            className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            🔐 Back to Login
          </button>
        </div>
      </div>
    );
  }

  // 🎉 Đúng role → render layout staff
  const staffMenu: SidebarItem[] = [
    { href: '/staff/ticket/create', label: 'Create ticket', icon: '🅿️' },
    { href: '/staff/ticket/checkout', label: 'Checkout ', icon: '🏁' },
  ];

  return (
    <div className="flex min-h-screen">
      <Sidebar menu={staffMenu} user={staff} onLogout={logoutStaff} />
      <main className="flex-1 bg-gray-100 p-8">{children}</main>
    </div>
  );
}
