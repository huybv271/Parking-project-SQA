'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AdminDashboardAPI } from '@/lib/api/admin/AdminDashboard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';

export default function ParkingRateManagementPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const VEHICLE_TYPES = ['CAR', 'MOTORBIKE'] as const;
  const TICKET_TYPES = ['STANDARD', 'OVERTIME'] as const;
  const [vehicleType, setVehicleType] = useState<string>(searchParams.get('vehicleType') ?? '');

  const [ticketType, setTicketType] = useState<string>(searchParams.get('ticketType') ?? '');

  const [unitPrice, setUnitPrice] = useState('');

  // =========================
  // LOAD CURRENT RATE
  // =========================
  useEffect(() => {
    if (!vehicleType || !ticketType) return;

    const loadRate = async () => {
      try {
        const res = await AdminDashboardAPI.getParkingRate();
        const rate = res.parkingRate.find(
          (r) =>
            r.vehicleType === vehicleType && r.ticketType === ticketType && r.status === 'active'
        );

        if (rate) {
          setUnitPrice(String(rate.unitPrice));
        }
      } catch (err) {
        console.error('Load parking rate failed', err);
      }
    };

    loadRate();
  }, [vehicleType, ticketType]);

  // =========================
  // SUBMIT UPDATE
  // =========================
  const handleSubmit = async () => {
    if (!unitPrice) {
      toast({
        variant: 'destructive',
        title: 'Thiếu dữ liệu',
        description: 'Vui lòng nhập giá',
      });
      return;
    }

    try {
      setLoading(true);

      const res = await AdminDashboardAPI.createNewParkingRate({
        vehicleType,
        ticketType,
        unitPrice: Number(unitPrice),
      });

      toast({
        title: 'Thành công 🎉',
        description: res?.message || 'Cập nhật biểu phí thành công',
      });

      router.push('/admin/dashboard');
      router.refresh(); // trigger re-fetch dashboard
    } catch (err: any) {
      console.error(err);

      toast({
        variant: 'destructive',
        title: 'Thất bại ❌',
        description: err?.response?.data?.message || err?.message || 'Cập nhật biểu phí thất bại',
      });
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // UI
  // =========================
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Card className="mx-auto max-w-lg">
        <CardHeader>
          <CardTitle>🅿️ Parking Rate Management</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Vehicle Type</label>
            <select
              value={vehicleType}
              onChange={(e) => setVehicleType(e.target.value)}
              className="mt-1 w-full rounded-md border px-3 py-2 text-sm"
            >
              <option value="">Select vehicle type</option>
              {VEHICLE_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm font-medium">Ticket Type</label>
            <select
              value={ticketType}
              onChange={(e) => setTicketType(e.target.value)}
              className="mt-1 w-full rounded-md border px-3 py-2 text-sm"
            >
              <option value="">Select ticket type</option>
              {TICKET_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm font-medium">Unit Price (VND)</label>
            <Input type="number" value={unitPrice} onChange={(e) => setUnitPrice(e.target.value)} />
          </div>

          <div className="flex justify-end gap-2 pt-4">
            <Button variant="outline" onClick={() => router.back()}>
              Cancel
            </Button>

            <Button onClick={handleSubmit} disabled={loading}>
              {loading ? 'Saving...' : 'Save'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
