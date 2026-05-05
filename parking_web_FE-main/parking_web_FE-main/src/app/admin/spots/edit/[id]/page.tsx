'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AdminSpotAPI, Spot } from '@/lib/api/admin/spotAPI';
import clsx from 'clsx';

export default function EditSpotPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();

  const [spot, setSpot] = useState<Spot | null>(null);
  const [isActive, setIsActive] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);

  // =====================
  // FETCH SPOT DETAIL
  // =====================
  useEffect(() => {
    if (!id) return;

    const spotId = Number(id);
    if (Number.isNaN(spotId)) {
      console.error('Invalid spot id:', id);
      setLoading(false);
      return;
    }

    const fetchSpot = async () => {
      try {
        setLoading(true);
        const res = await AdminSpotAPI.getSpotDetail(spotId);
        setSpot(res.spot);
        setIsActive(Boolean(res.spot.isActive));
      } finally {
        setLoading(false);
      }
    };

    fetchSpot();
  }, [id]);

  // =====================
  // SUBMIT
  // =====================
  const handleSubmit = async () => {
    if (!spot) return;
    try {
      setSaving(true);
      await AdminSpotAPI.editSpot(spot.id, {
        isActive: isActive ? 1 : 0,
      });

      alert('Cập nhật thành công');
      router.back();
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <Card className="p-6">Loading spot...</Card>;
  }

  if (!spot) {
    return <Card className="p-6 text-red-500">Spot không tồn tại</Card>;
  }

  return (
    <Card className="mx-auto max-w-xl space-y-6 p-6">
      <h1 className="text-xl font-bold">✏️ Edit Spot</h1>

      {/* ===== INFO ===== */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-500">Khu vực</p>
          <p className="font-semibold">{spot.area}</p>
        </div>

        <div>
          <p className="text-gray-500">Vị trí</p>
          <p className="font-semibold">{spot.position}</p>
        </div>

        <div>
          <p className="text-gray-500">Loại xe</p>
          <p className="font-semibold">{spot.vehicleType}</p>
        </div>

        <div>
          <p className="text-gray-500">Slot</p>
          <p className="font-semibold">{spot.slotType}</p>
        </div>
      </div>

      {/* ===== ACTIVE TOGGLE ===== */}
      <div className="space-y-2">
        <p className="text-sm font-medium">Trạng thái hoạt động</p>

        <div className="flex gap-3">
          <button
            type="button"
            onClick={() => setIsActive(true)}
            className={clsx(
              'rounded-md border px-4 py-2 text-sm font-semibold',
              isActive
                ? 'border-green-600 bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-500'
            )}
          >
            Active
          </button>

          <button
            type="button"
            onClick={() => setIsActive(false)}
            className={clsx(
              'rounded-md border px-4 py-2 text-sm font-semibold',
              !isActive ? 'border-gray-600 bg-gray-200 text-gray-700' : 'bg-gray-100 text-gray-500'
            )}
          >
            Inactive
          </button>
        </div>
      </div>

      {/* ===== ACTIONS ===== */}
      <div className="flex justify-end gap-3">
        <Button variant="outline" onClick={() => router.back()}>
          Huỷ
        </Button>

        <Button onClick={handleSubmit} disabled={saving}>
          {saving ? 'Đang lưu...' : 'Lưu thay đổi'}
        </Button>
      </div>
    </Card>
  );
}
