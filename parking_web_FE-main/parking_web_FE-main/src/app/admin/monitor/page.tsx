'use client';

import { useEffect, useMemo, useState } from 'react';
import { ParkingMonitorAPI, ParkingStatus } from '@/lib/api/admin/parkingMonitorAPI';
import { Card } from '@/components/ui/card';
import clsx from 'clsx';
import { getSocket } from '@/lib/socket';

const PAGE_SIZE = 36; // 6x6 grid

type ParkingSocketPayload = {
  action: 'updateParking';
  data: {
    spotId: number;
    status: boolean; // false = occupied, true = available
  };
};

export default function ParkingMonitorPage() {
  const [data, setData] = useState<ParkingStatus[]>([]);
  const [stats, setStats] = useState({
    availableSlot: 0,
    occupiedSlot: 0,
    bookedSlot: 0,
    lockedSlot: 0,
  });
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  // ===========================
  // INITIAL LOAD (REST – ONCE)
  // ===========================
  const fetchRealtimeStatus = async () => {
    try {
      setLoading(true);
      const res = await ParkingMonitorAPI.getRealtimeStatus();
      setData(res.mapStatus);
      setStats({
        availableSlot: res.availableSlot,
        occupiedSlot: res.occupiedSlot,
        bookedSlot: res.bookedSlot,
        lockedSlot: res.lockedSlot,
      });
    } finally {
      setLoading(false);
    }
  };

  // ===========================
  // 🔥 SOCKET REALTIME (NO REFRESH)
  // ===========================
  useEffect(() => {
    fetchRealtimeStatus();

    const socket = getSocket();

    socket.on('connect', () => {
      console.log('✅ Socket connected:', socket.id);
    });

    socket.on('parkingStatus', (payload: ParkingSocketPayload) => {
      if (payload?.action !== 'updateParking') return;

      const { spotId, status } = payload.data;

      setData((prev): ParkingStatus[] =>
        prev.map((spot) => {
          if (spot.id !== spotId) return spot;

          const newStatus: ParkingStatus['status'] = status ? 'AVAILABLE' : 'OCCUPIED';

          return {
            ...spot,
            status: newStatus,
            color: status ? '#86efac' : '#fca5a5',
          };
        })
      );

      setStats((prev) => ({
        ...prev,
        availableSlot: status ? prev.availableSlot + 1 : prev.availableSlot - 1,
        occupiedSlot: status ? prev.occupiedSlot - 1 : prev.occupiedSlot + 1,
      }));
    });

    socket.on('connect_error', (err) => {
      console.error('❌ Socket error:', err);
    });

    return () => {
      socket.off('parkingStatus');
      socket.off('connect');
      socket.off('connect_error');
    };
  }, []);

  // ===========================
  // PAGINATION (FE ONLY)
  // ===========================
  const totalPages = Math.ceil(data.length / PAGE_SIZE);

  const paginatedData = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return data.slice(start, start + PAGE_SIZE);
  }, [data, page]);

  useEffect(() => {
    if (page > totalPages) setPage(1);
  }, [totalPages, page]);

  if (loading) {
    return <Card className="p-6">⏳ Loading realtime parking status...</Card>;
  }

  return (
    <div className="space-y-6">
      {/* ===== HEADER ===== */}
      <div>
        <h1 className="text-2xl font-bold">Parking Monitor Realtime</h1>
        <p className="text-sm text-muted-foreground">
          Event-driven dashboard – zero refresh, zero flicker
        </p>
      </div>

      {/* ===== STATS ===== */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard label="Available" value={stats.availableSlot} color="text-green-600" />
        <StatCard label="Occupied" value={stats.occupiedSlot} color="text-red-600" />
        <StatCard label="Booked" value={stats.bookedSlot} color="text-yellow-600" />
        <StatCard label="Locked" value={stats.lockedSlot} color="text-gray-600" />
      </div>

      {/* ===== MAP GRID ===== */}
      <Card className="p-4">
        <div className="grid grid-cols-6 gap-3">
          {paginatedData.map((spot) => (
            <div
              key={spot.id}
              className={clsx(
                'rounded border p-2 text-center text-xs font-semibold transition-all duration-300'
              )}
              style={{ backgroundColor: spot.color }}
            >
              <div>{spot.position}</div>
              <div className="opacity-80">{spot.vehicleType}</div>
              <div className="uppercase">{spot.status}</div>
            </div>
          ))}
        </div>

        {/* ===== PAGINATION ===== */}
        <div className="mt-4 flex items-center justify-center gap-4">
          <button
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
            className="rounded border px-3 py-1 disabled:opacity-40"
          >
            ◀ Prev
          </button>

          <span className="text-sm">
            Page <strong>{page}</strong> / {totalPages || 1}
          </span>

          <button
            disabled={page === totalPages || totalPages === 0}
            onClick={() => setPage((p) => p + 1)}
            className="rounded border px-3 py-1 disabled:opacity-40"
          >
            Next ▶
          </button>
        </div>
      </Card>
    </div>
  );
}

/* ===== COMPONENT ===== */
function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <Card className="p-4 text-center">
      <div className="text-sm text-muted-foreground">{label}</div>
      <div className={clsx('text-2xl font-bold', color)}>{value}</div>
    </Card>
  );
}
