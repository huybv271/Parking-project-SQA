'use client';

import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useEffect } from 'react';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';
import { customerAuthAPI } from '@/lib/api/customer/CustomerAuth';

export default function CustomerInfoPage() {
  const router = useRouter();
  const { toast } = useToast();

  const { user, loading, refreshUser } = useCustomerAuth();

  useEffect(() => {
    const interval = setInterval(() => {
      refreshUser();
    }, 20000); // check mỗi 4 giây

    return () => clearInterval(interval);
  }, []);

  async function resendVerify() {
    try {
      await customerAuthAPI.resendVerify(user!.gmail);

      toast({
        title: 'Email sent',
        description: 'Please check your email.',
      });

      await refreshUser();
    } catch (err: any) {
      toast({
        title: 'Lỗi',
        description: err?.response?.data?.message || 'Sent email failed',
        variant: 'destructive',
      });
    }
  }

  if (loading) return <div className="p-8">Đang tải thông tin...</div>;
  if (!user) return <div className="p-8">Không tìm thấy thông tin người dùng.</div>;

  return (
    <div className="space-y-6 p-8">
      {/* Header */}
      <h1 className="text-2xl font-bold text-gray-800">Thông Tin Tài Khoản</h1>

      {/* USER INFO CARD */}
      <div className="rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-lg font-semibold">👤 Thông tin cá nhân</h2>

        <div className="space-y-2 text-gray-700">
          <p>
            <strong>Username:</strong> {user.username}
          </p>
          <p>
            <strong>Email:</strong> {user.gmail}
          </p>

          <p>
            <strong>Trạng thái:</strong>{' '}
            {user.status ? 'Hoạt động' : <span className="text-red-500">Bị khóa</span>}
          </p>
          <p>
            <strong>Xác minh email:</strong>{' '}
            {user.verified ? (
              <span className="text-green-600">Đã xác minh</span>
            ) : (
              <span className="text-red-500">Chưa xác minh</span>
            )}
          </p>
        </div>

        {/* BUTTONS */}
        <div className="mt-6 flex gap-3">
          <button
            onClick={() => router.push('/customer/dashboard')}
            className="rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
          >
            ⬅️ Quay lại
          </button>

          {!user.verified && (
            <button
              onClick={resendVerify}
              className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Gửi lại email xác minh
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
