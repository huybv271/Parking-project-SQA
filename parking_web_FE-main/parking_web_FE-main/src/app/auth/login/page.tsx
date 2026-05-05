'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useToast } from '@/hooks/use-toast';

export default function LoginPage() {
  const router = useRouter();
  const { loginCustomer, isAuthenticated, user } = useCustomerAuth();
  const { toast } = useToast();

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<{ username: string; password: string }>({
    username: '',
    password: '',
  });

  //Neu da login roi thi khong cho quay lai login nua
  useEffect(() => {
    if (!isAuthenticated || !user) return;
    if (user.role === 'customer') {
      router.replace('/customer/dashboard');
    } else {
      router.replace('/');
    }
  }, [isAuthenticated, router, user]);

  const handleSubmit = async (e: React.FormEvent, role: 'customer' | 'staff') => {
    e.preventDefault();

    // Client-side validation
    if (!formData.username || !formData.password) {
      toast({
        title: 'Vui lòng điền đủ thông tin',
        description: 'Username và password không được để trống',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);

    try {
      await loginCustomer(formData);

      toast({
        title: 'Login successfully',
        description: 'Login successfully!!!',
        variant: 'default',
      });

      router.push('/customer/dashboard');
    } catch (error: any) {
      toast({
        title: 'Đăng nhập thất bại!',
        description:
          error?.response?.data?.message || error?.message || 'Sai tài khoản hoặc mật khẩu',
        variant: 'destructive',
      });
      console.error('Customer login error:', error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-lg">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-center">
          <h1 className="mb-2 text-2xl font-bold text-white">LICHT-PARKING</h1>
          <h2 className="text-3xl font-bold text-white">Đăng nhập</h2>
        </div>

        <div className="p-8">
          {/* Register prompt */}
          <div className="mb-6 text-center">
            <span className="text-gray-600">Chưa có tài khoản? </span>
            <Link href="/auth/register" className="font-medium text-blue-600 hover:text-blue-700">
              Đăng ký
            </Link>
          </div>

          <form onSubmit={(e) => handleSubmit(e, 'customer')} className="space-y-6">
            {/* Phone input */}
            <div>
              <label htmlFor="phone" className="mb-2 block text-sm font-medium text-gray-700">
                Tên đăng nhập
              </label>
              <div className="relative">
                <input
                  id="phone"
                  type="text"
                  placeholder="Nhập tên đăng nhập"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            {/* Password input */}
            <div>
              <div className="mb-2 flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Mật khẩu
                </label>
                <Link
                  href="/auth/forgot-password"
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  Quên mật khẩu?
                </Link>
              </div>
              <input
                id="password"
                type="password"
                placeholder="Nhập mật khẩu"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Submit button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-700 px-4 py-3 font-medium text-white transition hover:from-blue-700 hover:to-indigo-800 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
            </button>
          </form>

          {/* Staff login link */}
          <div className="mt-6 text-center">
            <Link href="/staff/auth/login" className="text-sm text-gray-600 hover:text-gray-800">
              Đăng nhập cho nhân viên →
            </Link>
          </div>

          {/* Back to Home */}
          <div className="mt-4 text-center">
            <Link
              href="/"
              className="inline-flex items-center gap-1 text-sm text-gray-600 transition hover:text-blue-600"
            >
              ← Quay về trang chủ
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
