'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { AdminSpotAPI, Spot } from '@/lib/api/admin/spotAPI';

export default function DeletedSpotsPage() {
  const router = useRouter();
  const [spots, setSpots] = useState<Spot[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchDeletedSpots = async () => {
    try {
      const res = await AdminSpotAPI.getDeletedSpots();
      setSpots(res.spots || []);
    } catch (error) {
      console.error('Fetch deleted spots failed', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestore = async (id: number) => {
    await AdminSpotAPI.restoreSpot(id);
    fetchDeletedSpots();
  };

  useEffect(() => {
    fetchDeletedSpots();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🗑️ Deleted Spots</h1>

      {loading && <p className="text-sm text-muted-foreground">Loading data...</p>}

      {!loading && spots.length === 0 && (
        <p className="text-sm text-muted-foreground">Không có spot nào trong thùng rác</p>
      )}

      <div className="space-y-3">
        {spots.map((spot) => (
          <Card
            key={spot.id}
            className="flex items-center justify-between rounded-xl p-4 shadow-sm"
          >
            <div className="space-y-1">
              <p className="font-medium">
                Khu {spot.area} – Vị trí {spot.position}
              </p>
              <p className="text-sm text-muted-foreground">
                {spot.vehicleType} · {spot.slotType}
              </p>
            </div>

            <Button variant="outline" onClick={() => handleRestore(spot.id)}>
              ♻️ Restore
            </Button>
          </Card>
        ))}
      </div>

      <Button
        onClick={() => router.push('/admin/spots')}
        className="mt-10 rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
      >
        ⬅️ Quay lại
      </Button>
    </div>
  );
}
