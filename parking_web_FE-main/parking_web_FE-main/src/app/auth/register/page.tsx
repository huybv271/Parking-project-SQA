'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { customerAuthAPI } from '@/lib/api/customer/CustomerAuth';
import { useToast } from '@/hooks/use-toast';
import Link from 'next/link';
export default function RegisterPage() {
  const { toast } = useToast();
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    gmail: '',
    password: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.username || !formData.gmail || !formData.password) {
      toast({
        title: 'Lack of Information',
        description: 'Please fill all information',
        variant: 'destructive',
      });
      return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.gmail)) {
      toast({
        title: 'wrong format of gmail',
        description: 'Please fill valid email address!',
        variant: 'destructive',
      });
    }
    setLoading(true);
    try {
      await customerAuthAPI.registerCustomer({
        username: formData.username,
        gmail: formData.gmail,
        password: formData.password,
      });

      toast({
        title: 'Register successfully!',
        description: 'PLease check your email to verify account',
        variant: 'default',
      });
      router.push('/auth/login');
    } catch (error: any) {
      const message = error?.response?.data?.message || 'Register failed, please try again!';
      toast({
        title: 'Register failed',
        description: message,
        variant: 'destructive',
      });
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
          <h2 className="text-3xl font-bold text-white">Đăng ký tài khoản</h2>
        </div>

        <div className="p-8">
          {/* Login prompt */}
          <div className="mb-6 text-center">
            <span className="text-gray-600">Đã có tài khoản? </span>
            <Link href="/auth/login" className="font-medium text-blue-600 hover:text-blue-700">
              Đăng nhập
            </Link>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Username</label>
              <input
                type="text"
                placeholder="Nhập số điện thoại"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Gmail */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Gmail</label>
              <input
                type="email"
                placeholder="Nhập gmail"
                value={formData.gmail}
                onChange={(e) => setFormData({ ...formData, gmail: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Password */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Mật khẩu</label>
              <input
                type="password"
                placeholder="Nhập mật khẩu"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-700 px-4 py-3 font-medium text-white transition hover:from-blue-700 hover:to-indigo-800 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Đang xử lý...' : 'Đăng ký'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
