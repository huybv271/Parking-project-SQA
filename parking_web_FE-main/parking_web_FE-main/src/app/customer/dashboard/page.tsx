'use client';

import { useEffect, useState } from 'react';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { userReservationAPI } from '@/lib/api/customer/customerReservationAPI';

export default function CustomerDashboardPage() {
  const { user, loading } = useCustomerAuth();
  const [activeCount, setActiveCount] = useState<number>(0);
  const [loadingRes, setLoadingRes] = useState(true);

  useEffect(() => {
    if (!user) return;

    async function fetchDashboardInfo() {
      try {
        const res = await userReservationAPI.getActiveReservationNumber();
        setActiveCount(res.numbers);
      } catch (err) {
        console.log('Cannot load reservation number');
      } finally {
        setLoadingRes(false);
      }
    }

    fetchDashboardInfo();
  }, [user]);

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="space-y-6 p-8">
      {/* Greeting */}
      <h1 className="flex items-center gap-2 text-3xl font-bold text-gray-800">
        Welcome back,
        <span className="text-indigo-600">{user?.username}</span>
      </h1>

      {/* Notification Box */}
      <div className="rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-lg font-semibold">🔔 Thông báo</h2>

        {loadingRes ? (
          <p className="text-gray-600">Đang tải thông tin...</p>
        ) : activeCount > 0 ? (
          <p className="font-medium text-green-600">
            ✔ Bạn đang có <strong>{activeCount}</strong> lượt đặt chỗ đang hoạt động
          </p>
        ) : (
          <p className="text-gray-600">Hiện tại bạn chưa có lượt đặt chỗ nào.</p>
        )}
      </div>
    </div>
  );
}
