'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { useToast } from '@/hooks/use-toast';
import Link from 'next/link';

export default function StaffLoginPage() {
  const router = useRouter();
  const { loginStaff, isAuthenticated, staff } = useStaffAuth();
  const { toast } = useToast();

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  // Nếu đã đăng nhập → redirect đúng theo role
  useEffect(() => {
    if (!isAuthenticated || !staff) return;

    if (staff.role === 'staff') {
      router.replace('/staff/dashboard');
    } else if (staff.role === 'admin') {
      router.replace('/admin/dashboard');
    } else {
      router.replace('/');
    }
  }, [isAuthenticated, staff, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.username || !formData.password) {
      toast({
        title: 'Thiếu thông tin',
        description: 'Tên đăng nhập và mật khẩu không được để trống.',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);

    try {
      await loginStaff(formData);

      toast({
        title: 'Đăng nhập thành công!',
      });

      // Điều hướng theo role
      if (staff?.role === 'admin') {
        router.push('/admin/dashboard');
      } else {
        router.push('/staff/dashboard');
      }
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } } };

      toast({
        title: 'Đăng nhập thất bại!',
        description: err?.response?.data?.message || 'Sai thông tin đăng nhập',
        variant: 'destructive',
      });

      console.error('Staff login failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 p-4">
      <div className="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-lg">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-emerald-700 p-6 text-center">
          <h1 className="mb-2 text-2xl font-bold text-white">LICHT-PARKING</h1>
          <h2 className="text-3xl font-bold text-white">Đăng nhập Nhân viên / Admin</h2>
          <p className="mt-2 text-sm text-green-100">Hệ thống dành cho Nhân viên & Quản trị</p>
        </div>

        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Tên đăng nhập</label>
              <input
                type="text"
                placeholder="Tên đăng nhập"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            {/* Password */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Mật khẩu</label>
              <input
                type="password"
                placeholder="Mật khẩu"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-gradient-to-r from-green-600 to-emerald-700 px-4 py-3 font-medium text-white transition hover:from-green-700 hover:to-emerald-800 disabled:opacity-50"
            >
              {loading ? 'Đang đăng nhập...' : '🔐 Đăng nhập'}
            </button>
          </form>

          {/* Switch to customer login */}
          <div className="mt-6 text-center">
            <Link href="/auth/login" className="text-sm text-gray-600 hover:text-gray-800">
              ← Quay lại đăng nhập Khách hàng
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
