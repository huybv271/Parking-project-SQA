'use client';

import Sidebar, { SidebarItem } from '@/components/SideBar';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useRouter } from 'next/navigation';

export default function CustomerLayout({ children }: { children: React.ReactNode }) {
  const { user, loading, isAuthenticated, logoutCustomer } = useCustomerAuth();
  const router = useRouter();

  if (loading) return null;

  // ❌ Sai role hoặc chưa login → Access Denied
  if (!isAuthenticated || !user || user.role !== 'customer') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-100">
        <div className="rounded-xl bg-white p-8 text-center shadow-lg">
          <h1 className="mb-4 text-2xl font-bold text-red-600">Access Denied</h1>
          <p className="mb-6 text-gray-700">Vui lòng đăng nhập với tài khoản khách hàng.</p>

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

  // 🎉 Đúng role → render layout customer
  const customerMenu: SidebarItem[] = [
    { href: '/customer/reservation', label: 'Reservation', icon: '🅿️' },
    { href: '/customer/history', label: 'History', icon: '📜' },
    { href: '/customer/infor', label: 'My infor', icon: '🧑‍💻' },
  ];

  return (
    <div className="flex min-h-screen">
      <Sidebar menu={customerMenu} user={user} onLogout={logoutCustomer} />
      <main className="flex-1 bg-blue-50 p-8">{children}</main>
    </div>
  );
}
