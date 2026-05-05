'use client';

import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AdminDashboardAPI } from '@/lib/api/admin/AdminDashboard';
import type { ParkingRate } from '@/lib/api/admin/AdminDashboard';
import VehicleRatioChart from '@/components/charts/VehicleRatioChart';
import MonthlyRevenueChart from '@/components/charts/MonthlyRevenueChart';
import { useRouter } from 'next/navigation';

type MonthlyChart = {
  labels: string[];
  data: number[];
};

export default function AdminDashboardPage() {
  const { staff, loading, isAuthenticated } = useStaffAuth();
  const router = useRouter();

  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [todayRevenue, setTodayRevenue] = useState(0);
  const [monthlyChart, setMonthlyChart] = useState<MonthlyChart | null>(null);
  const [parkingRate, setParkingRate] = useState<ParkingRate[]>([]);
  const [vehicleRatio, setVehicleRatio] = useState<any>(null);

  // 🔥 NEW: toggle inactive rates
  const [showInactive, setShowInactive] = useState(false);

  // =========================
  // LOAD DASHBOARD DATA
  // =========================
  const loadDashboard = async () => {
    try {
      setDashboardLoading(true);

      const [revenueRes, chartRes, ratioRes, rateRes] = await Promise.all([
        AdminDashboardAPI.getNowRevenue(),
        AdminDashboardAPI.getMonthlyRevenue(),
        AdminDashboardAPI.getRatioVehicle(),
        AdminDashboardAPI.getParkingRate(),
      ]);

      setTodayRevenue(revenueRes.sum);
      setMonthlyChart(chartRes.chartData);
      setVehicleRatio(ratioRes);
      setParkingRate(rateRes.parkingRate);
    } catch (err) {
      console.error('Load admin dashboard failed:', err);
    } finally {
      setDashboardLoading(false);
    }
  };

  useEffect(() => {
    if (!loading && isAuthenticated && staff?.role === 'admin') {
      loadDashboard();
    }
  }, [loading, isAuthenticated, staff]);

  // =========================
  // AUTH CHECK
  // =========================
  if (loading) {
    return <div className="flex min-h-screen items-center justify-center">Đang xác thực...</div>;
  }

  if (!isAuthenticated || staff?.role !== 'admin') {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <h1 className="text-xl font-bold text-red-600">Access Denied</h1>
      </div>
    );
  }

  // =========================
  // FILTER PARKING RATE
  // =========================
  const filteredParkingRate = showInactive
    ? parkingRate
    : parkingRate.filter((rate) => rate.status === 'active');

  // =========================
  // DASHBOARD UI
  // =========================
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-800">Admin Dashboard</h1>
        <p className="text-gray-600">
          Xin chào <span className="font-semibold text-blue-600">{staff.username}</span>
        </p>
      </div>

      {dashboardLoading ? (
        <p>Đang tải dữ liệu dashboard...</p>
      ) : (
        <>
          {/* TOP STATS */}
          <div className="mb-10 grid grid-cols-1 gap-6 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>💰 Doanh thu hôm nay</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold text-green-600">
                  {todayRevenue.toLocaleString()} VND
                </p>
              </CardContent>
            </Card>

            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>🚗 Tỉ lệ phương tiện</CardTitle>
              </CardHeader>
              <CardContent>
                {vehicleRatio ? (
                  <VehicleRatioChart data={vehicleRatio} />
                ) : (
                  <p className="text-gray-500">Không có dữ liệu</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* MONTHLY CHART */}
          <Card>
            <CardHeader>
              <CardTitle>📊 Doanh thu theo tháng</CardTitle>
            </CardHeader>
            <CardContent>{monthlyChart && <MonthlyRevenueChart data={monthlyChart} />}</CardContent>
          </Card>

          {/* PARKING RATE */}
          <Card className="mt-10">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>🅿️ Biểu phí gửi xe</CardTitle>

              <div className="flex gap-2">
                {/* TOGGLE */}
                <button
                  onClick={() => setShowInactive((prev) => !prev)}
                  className="rounded border px-3 py-1 text-sm hover:bg-gray-100"
                >
                  {showInactive ? 'Hide inactive' : 'Show all'}
                </button>

                {/* ADD */}
                <button
                  onClick={() => router.push('/admin/parking-rate-management')}
                  className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
                >
                  + Add Parking Rate
                </button>
              </div>
            </CardHeader>

            <CardContent>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                {filteredParkingRate.map((rate, index) => (
                  <div
                    key={index}
                    className={`flex flex-col justify-between rounded-lg border p-4 shadow-sm ${
                      rate.status === 'inactive' ? 'bg-gray-50 opacity-60' : 'bg-white'
                    }`}
                  >
                    <div>
                      <div className="mb-2 flex items-center justify-between">
                        <span className="font-semibold">{rate.vehicleType}</span>
                        <span
                          className={`rounded px-2 py-0.5 text-xs ${
                            rate.status === 'active'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-gray-200 text-gray-600'
                          }`}
                        >
                          {rate.status}
                        </span>
                      </div>

                      <p className="text-sm text-gray-500">{rate.ticketType}</p>

                      <p className="mt-3 text-xl font-bold text-blue-600">
                        {Number(rate.unitPrice).toLocaleString('vi-VN')} {rate.currency}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
