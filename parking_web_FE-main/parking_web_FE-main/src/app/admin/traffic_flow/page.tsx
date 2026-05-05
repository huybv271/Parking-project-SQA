'use client';

import { useEffect, useState } from 'react';
import { TrafficFlowAPI } from '@/lib/api/admin/trafficFlowAPI';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { GenericBarChart } from '@/components/charts/GenericBarChart';

export default function TrafficFlowPage() {
  // =========================
  // STATE
  // =========================
  const today = new Date().toISOString().split('T')[0];

  const [date, setDate] = useState(today);
  const [loading, setLoading] = useState(false);
  const [checkInNumbers, setCheckInNumbers] = useState<number[]>([]);
  const [checkOutNumbers, setCheckOutNumbers] = useState<number[]>([]);

  // =========================
  // API CALL
  // =========================
  const loadTrafficFlow = async () => {
    if (!date) return;

    try {
      setLoading(true);
      const res = await TrafficFlowAPI.getTrafficFlow(date);
      setCheckInNumbers(res.checkInNumbers ?? []);
      setCheckOutNumbers(res.checkOutNumbers ?? []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // loadTrafficFlow();
  }, []);

  // =========================
  // DERIVED DATA (📌 NẰM Ở ĐÂY)
  // =========================
  const chartData = Array.from({ length: 24 }).map((_, hour) => {
    const start = hour.toString().padStart(2, '0');
    const end = (hour + 1).toString().padStart(2, '0');

    return {
      hour: `${start}-${end}`, // 👈 interval label
      checkIn: checkInNumbers[hour] ?? 0,
      checkOut: checkOutNumbers[hour] ?? 0,
    };
  });

  const totalCheckIn = checkInNumbers.reduce((a, b) => a + b, 0);
  const totalCheckOut = checkOutNumbers.reduce((a, b) => a + b, 0);

  // =========================
  // UI
  // =========================
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="mb-6 text-3xl font-bold text-gray-800">🚦 Giám sát lưu lượng bãi xe</h1>

      {/* FILTER */}
      <div className="mb-6 flex items-center gap-4">
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="rounded border px-3 py-2"
        />
        <Button onClick={loadTrafficFlow}>Thống kê</Button>
      </div>

      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : (
        <>
          {/* STATS */}
          <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>🚗 Tổng xe vào</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-green-600">{totalCheckIn}</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>🚙 Tổng xe ra</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-red-600">{totalCheckOut}</p>
              </CardContent>
            </Card>
          </div>

          {/* CHART */}
          <Card>
            <CardHeader>
              <CardTitle>📊 Lưu lượng xe theo giờ</CardTitle>
            </CardHeader>
            <CardContent>
              <GenericBarChart
                data={chartData}
                xKey="hour"
                bars={[
                  {
                    key: 'checkIn',
                    label: 'Xe vào',
                    color: '#22c55e',
                  },
                  {
                    key: 'checkOut',
                    label: 'Xe ra',
                    color: '#ef4444',
                  },
                ]}
              />
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
