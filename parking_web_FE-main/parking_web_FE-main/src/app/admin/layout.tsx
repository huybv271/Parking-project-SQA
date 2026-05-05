'use client';

import Sidebar, { SidebarItem } from '@/components/SideBar';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { useStaffAuth } from '@/contexts/StaffAuthContext';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { staff, loading, isAuthenticated, logoutStaff } = useStaffAuth();
  const router = useRouter();

  // =========================
  // REDIRECT LOGIC
  // =========================
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.replace('/staff/auth/login');
    }
  }, [loading, isAuthenticated, router]);

  // =========================
  // AUTH LOADING
  // =========================
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-gray-500">
        Đang kiểm tra quyền truy cập...
      </div>
    );
  }

  // =========================
  // CHƯA LOGIN (đang redirect)
  // =========================
  if (!isAuthenticated) {
    return null;
  }

  // =========================
  // ACCESS DENIED (SAI ROLE)
  // =========================
  if (!staff || staff.role !== 'admin') {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <h2 className="text-2xl font-bold text-red-600">Access Denied</h2>
        <p className="text-gray-600">Bạn không có quyền truy cập khu vực dành cho Admin.</p>

        <div className="flex gap-4">
          <Button onClick={() => router.push('/')}>⬅️ Về trang chủ</Button>
          <Button variant="secondary" onClick={() => router.push('/staff/auth/login')}>
            Đăng nhập bằng tài khoản khác
          </Button>
        </div>
      </div>
    );
  }

  // =========================
  // ADMIN MENU
  // =========================
  const adminMenu: SidebarItem[] = [
    { href: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/admin/traffic_flow', label: 'Traffic Flow', icon: '🚦' },

    // =================
    // STAFFS
    // =================
    { href: '/admin/staffs/list', label: 'Staff List', icon: '👥' },
    { href: '/admin/staffs/create', label: 'Create Staff', icon: '➕' },
    { href: '/admin/staffs/trash', label: 'Deleted Staffs', icon: '🗑️' },

    // =================
    // SPOTS
    // =================
    { href: '/admin/spots/A', label: 'Spots  Area', icon: '🅿️' },

    { href: '/admin/spots/create', label: 'Create Spot', icon: '➕' },
    { href: '/admin/spots/trash', label: 'Deleted Spots', icon: '🗑️' },

    // =================
    // TICKETS
    // =================
    { href: '/admin/tickets', label: 'Tickets', icon: '🎟️' },
    { href: '/admin/monitor', label: 'Monitor', icon: '🖥️' },
  ];

  // =========================
  // RENDER ADMIN LAYOUT
  // =========================
  return (
    <div className="flex min-h-screen">
      <Sidebar menu={adminMenu} user={staff} onLogout={logoutStaff} />
      <main className="flex-1 bg-gray-100 p-8">{children}</main>
    </div>
  );
}
