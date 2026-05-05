'use client';

import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from '@/hooks/use-toast';

export default function ForgotPasswordPage() {
  const router = useRouter();
  const { toast } = useToast();
  const { sendResetBarcode } = useCustomerAuth();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email) {
      toast({
        title: 'Lack of information',
        description: 'Please fill your email',
        variant: 'destructive',
      });
      return;
    }
    setLoading(true);
    try {
      await sendResetBarcode(email);
      toast({
        title: 'Barcode has been sent',
        description: 'Barcode has been sent, please check your email!',
        variant: 'default',
      });
      router.push(`/auth/reset-password?gmail=${encodeURIComponent(email)}`);
    } catch (error: any) {
      const message = error?.response?.data?.message;
      toast({
        title: 'Send failed',
        description: message || 'Unknown fault',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow">
        <h1 className="mb-4 text-center text-2xl font-bold text-blue-600">Quên mật khẩu</h1>

        <form onSubmit={handleSend} className="space-y-6">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">Gmail đã đăng ký</label>
            <input
              type="email"
              placeholder="Nhập email của bạn"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border px-4 py-3"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-medium text-white hover:bg-blue-700"
          >
            {loading ? 'Đang gửi...' : 'Gửi mã reset mật khẩu'}
          </button>
        </form>
      </div>
    </div>
  );
}
