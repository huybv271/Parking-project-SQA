'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AdminSpotAPI, Spot } from '@/lib/api/admin/spotAPI';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import clsx from 'clsx';

const VEHICLE_LABEL: Record<string, string> = {
  CAR: '🚗 CAR',
  MOTORBIKE: '🏍️ MOTORBIKE',
};

const SLOT_LABEL: Record<string, string> = {
  ONLINE: 'Online',
  OFFLINE: 'Offline',
};

// hardcode trước – sau này replace bằng API
const AREAS = ['A', 'B'];

export default function SpotManagementPage() {
  const router = useRouter();

  const [area, setArea] = useState<string>('A');
  const [spots, setSpots] = useState<Spot[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  // =====================
  // FETCH SPOTS
  // =====================
  const fetchSpots = async (selectedArea: string) => {
    try {
      setLoading(true);
      const res = await AdminSpotAPI.getSpotByArea(selectedArea);
      setSpots(res.spots || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSpots(area);
  }, [area]);

  // =====================
  // TOGGLE ACTIVE
  // =====================
  const handleToggleActive = async (spot: Spot) => {
    try {
      setUpdatingId(spot.id);

      await AdminSpotAPI.editSpot(spot.id, {
        isActive: spot.isActive ? 0 : 1,
      });

      // optimistic update
      setSpots((prev) =>
        prev.map((s) => (s.id === spot.id ? { ...s, isActive: s.isActive === 1 ? 0 : 1 } : s))
      );
    } catch (error) {
      alert('Cập nhật trạng thái thất bại');
    } finally {
      setUpdatingId(null);
    }
  };

  // =====================
  // DELETE
  // =====================
  const handleDelete = async (id: number) => {
    if (!confirm('Bạn chắc chắn muốn xoá spot này?')) return;
    await AdminSpotAPI.deleteSpot(id);
    fetchSpots(area);
    
  };

  if (loading) {
    return <Card className="p-4">Loading spots...</Card>;
  }

  return (
    <Card className="space-y-6 p-6">
      {/* ===== Header ===== */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">📍 Quản lý Spot</h1>

        <select
          value={area}
          onChange={(e) => setArea(e.target.value)}
          className="rounded-md border px-3 py-2 text-sm"
        >
          {AREAS.map((a) => (
            <option key={a} value={a}>
              Khu vực {a}
            </option>
          ))}
        </select>
      </div>

      {/* ===== Table ===== */}
      <table className="w-full border text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2">Vị trí</th>
            <th className="p-2">Loại xe</th>
            <th className="p-2">Slot</th>
            <th className="p-2">Hoạt động</th>
            <th className="p-2">Action</th>
          </tr>
        </thead>

        <tbody>
          {spots.length > 0 ? (
            spots.map((spot) => (
              <tr key={spot.id} className="border-t text-center">
                <td className="p-2 font-semibold">{spot.position}</td>

                <td className="p-2">{VEHICLE_LABEL[spot.vehicleType]}</td>

                <td className="p-2">{SLOT_LABEL[spot.slotType]}</td>

                {/* ===== ACTIVE TOGGLE ===== */}
                <td className="p-2">
                  <button
                    disabled={updatingId === spot.id}
                    onClick={() => handleToggleActive(spot)}
                    className={clsx(
                      'relative inline-flex h-6 w-11 items-center rounded-full transition',
                      spot.isActive ? 'bg-green-500' : 'bg-red-500',
                      updatingId === spot.id && 'cursor-not-allowed opacity-50'
                    )}
                  >
                    <span
                      className={clsx(
                        'inline-block h-4 w-4 transform rounded-full bg-white transition',
                        spot.isActive ? 'translate-x-6' : 'translate-x-1'
                      )}
                    />
                  </button>
                </td>

                {/* ===== ACTION ===== */}
                <td className="space-x-2 p-2">
                  <Button size="sm" variant="destructive" onClick={() => handleDelete(spot.id)}>
                    Delete
                  </Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={5} className="p-6 text-center text-sm text-muted-foreground">
                Không có spot nào trong khu vực {area}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </Card>
  );
}
