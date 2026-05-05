'use client';

import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link, { useSearchParams } from 'next/navigation';
import { useToast } from '@/hooks/use-toast';
import { customerAuthAPI } from '@/lib/api/customer/CustomerAuth';

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const router = useRouter();
  const { toast } = useToast();

  const gmail = params.get('gmail') || '';
  const [token, setToken] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { resetPassword } = useCustomerAuth();

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!gmail || !token || !password) {
      toast({
        title: 'Lack of information',
        description: 'Please fill all information',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);

    try {
      await resetPassword(gmail, token, password);
      toast({
        title: 'Reset uccessfully',
        description: 'Reset password successfully!',
        variant: 'default',
      });

      router.push('/auth/login');
    } catch (error: any) {
      toast({
        title: 'Reset failed',
        description: error?.response?.data?.message || 'Cannot reset password, please try again!',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow">
        <h1 className="mb-4 text-center text-2xl font-bold text-blue-600">Đặt lại mật khẩu</h1>

        <form onSubmit={handleReset} className="space-y-6">
          <div>
            <label className="mb-2 block text-sm font-medium">Gmail</label>
            <input
              type="email"
              value={gmail}
              disabled
              className="w-full cursor-not-allowed rounded-lg border bg-gray-100 px-4 py-3"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">Mã Barcode</label>
            <input
              type="text"
              placeholder="Nhập mã token"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="w-full rounded-lg border px-4 py-3"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">Mật khẩu mới</label>
            <input
              type="password"
              placeholder="Nhập mật khẩu mới"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border px-4 py-3"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-medium text-white hover:bg-blue-700"
          >
            {loading ? 'Đang xử lý...' : 'Đổi mật khẩu'}
          </button>
        </form>
      </div>
    </div>
  );
}
