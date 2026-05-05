'use client';
import { useState } from 'react';
import {
  userReservationAPI,
  VehicleType,
  FreeSpot,
} from '@/lib/api/customer/customerReservationAPI';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';

/**
 * Tính realTime + 49h và trả về cả datetime, date, hour
 */
function getMin49h() {
  const now = new Date();
  const minDT = new Date(now.getTime() + 49 * 60 * 60 * 1000); // ✅ +49h

  const year = minDT.getFullYear();
  const month = String(minDT.getMonth() + 1).padStart(2, '0');
  const day = String(minDT.getDate()).padStart(2, '0');

  return {
    full: minDT,
    date: `${year}-${month}-${day}`, // yyyy-mm-dd
    hour: minDT.getHours(), // giờ tối thiểu nếu chọn đúng ngày +49h
  };
}

export default function UserReservationPage() {
  const { toast } = useToast();
  const router = useRouter();

  const min49 = getMin49h();
  const minDateIn = min49.date;
  const minHourIn = min49.hour;

  const [vehicleType, setVehicleType] = useState<VehicleType>('MOTORBIKE');
  const [plate, setPlate] = useState('');

  const [dateIn, setDateIn] = useState('');
  const [dateOut, setDateOut] = useState('');

  // ✅ init giờ vào / ra theo minHourIn
  const [timeIn, setTimeIn] = useState<number>(Math.min(minHourIn, 22));
  const [timeOut, setTimeOut] = useState<number>(Math.min(minHourIn + 1, 23));

  const [loading, setLoading] = useState(false);
  const [spots, setSpots] = useState<FreeSpot[]>([]);
  const [searchInfo, setSearchInfo] = useState<any>(null);

  const isSameDay = dateIn === dateOut;

  const minDateOut = dateIn ? dateIn : minDateIn;

  const minTimeOut = isSameDay ? timeIn + 1 : 0;
  const maxTimeOut = 23;
  const maxTimeIn = isSameDay ? 22 : 23;

  // =====================
  // SEARCH AVAILABLE SLOTS
  // =====================
  const handleSearch = async () => {
    if (!dateIn || !dateOut || !plate) {
      toast({
        title: 'Lack of information',
        description: 'Please fill all information!',
        variant: 'destructive',
      });
      return;
    }

    try {
      setLoading(true);
      setSpots([]);
      setSearchInfo(null);

      const data = await userReservationAPI.getAvailableSlots({
        timeIn,
        timeOut,
        dateTimeIn: dateIn,
        dateTimeOut: dateOut,
        vehicleType,
      });

      setSpots(data.freeSpots);
      setSearchInfo(data);

      if (data.freeSpots.length === 0) {
        toast({
          title: 'No slot remains',
          description: 'No slots remain, please change time or date',
          variant: 'destructive',
        });
      } else {
        toast({
          title: 'Slot found',
          description: `Slot found, ${data.freeSpots.length} slots are available`,
          variant: 'default',
        });
      }
    } catch (err: unknown) {
      const anyErr = err as any;
      const msg =
        anyErr?.response?.data?.message || 'Can not find any slot available, please try again!';
      toast({
        title: 'Something went wrong',
        description: msg,
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="mx-auto max-w-3xl">
        {/* Header */}
        <div className="mb-8 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-center text-white shadow-lg">
          <h1 className="text-3xl font-bold">Đặt Chỗ Gửi Xe</h1>
          <p className="mt-1 text-blue-100">Chọn thời gian – Chọn vị trí – Thanh toán online</p>
        </div>

        {/* Form */}
        <div className="space-y-6 rounded-2xl bg-white p-6 shadow-lg">
          {/* DATE */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Ngày vào</label>
              <input
                type="date"
                value={dateIn}
                min={minDateIn}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-600"
                onChange={(e) => {
                  const newDate = e.target.value;
                  setDateIn(newDate);

                  // ✅ Case 1: chọn đúng ngày minDateIn => timeIn >= minHourIn
                  if (newDate === minDateIn) {
                    const nextTimeIn = Math.min(Math.max(timeIn, minHourIn), 22);
                    setTimeIn(nextTimeIn);

                    const nextTimeOut = Math.min(Math.max(timeOut, nextTimeIn + 1), 23);
                    setTimeOut(nextTimeOut);
                    return;
                  }

                  // ✅ Case 2: chọn ngày lớn hơn => reset timeIn = 0, timeOut = 1 (hoặc giữ lớn hơn nếu đang lớn)
                  if (newDate > minDateIn) {
                    const nextTimeIn = 0;
                    setTimeIn(nextTimeIn);

                    const nextTimeOut = Math.min(Math.max(timeOut, nextTimeIn + 1), 23);
                    setTimeOut(nextTimeOut);
                    return;
                  }
                }}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Ngày ra</label>
              <input
                type="date"
                value={dateOut}
                min={minDateOut}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-600"
                onChange={(e) => setDateOut(e.target.value)}
              />
            </div>
          </div>

          {/* TIME */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Giờ vào</label>
              <input
                type="number"
                min={dateIn === minDateIn ? minHourIn : 0}
                max={maxTimeIn}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-600"
                value={timeIn}
                onChange={(e) => {
                  const raw = Number(e.target.value);
                  const value = Number.isFinite(raw) ? raw : 0;

                  // chặn 49h nếu là ngày min
                  if (dateIn === minDateIn && value < minHourIn) {
                    toast({
                      title: 'Invalid time',
                      description: `Giờ vào phải ≥ ${minHourIn}h (đặt trước 49h)`,
                      variant: 'destructive',
                    });
                    return;
                  }

                  const nextTimeIn = Math.min(Math.max(value, 0), maxTimeIn);
                  setTimeIn(nextTimeIn);

                  // chỉ auto ép timeOut nếu cùng ngày
                  if (isSameDay) {
                    const minOut = nextTimeIn + 1;
                    if (timeOut < minOut) setTimeOut(Math.min(minOut, 23));
                  }
                }}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Giờ ra</label>
              <input
                type="number"
                min={minTimeOut}
                max={maxTimeOut}
                value={timeOut}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-600"
                onChange={(e) => {
                  const valueRaw = Number(e.target.value);
                  const value = Number.isFinite(valueRaw) ? valueRaw : minTimeOut;

                  if (value < minTimeOut) {
                    toast({
                      title: 'Invalid time',
                      description: isSameDay
                        ? `Giờ ra phải ≥ ${timeIn + 1}h (cùng ngày)`
                        : 'Giờ ra không hợp lệ',
                      variant: 'destructive',
                    });
                    return;
                  }

                  setTimeOut(Math.min(value, 23));
                }}
              />
            </div>
          </div>

          {/* VEHICLE + PLATE */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Loại xe</label>
              <select
                value={vehicleType}
                onChange={(e) => setVehicleType(e.target.value as VehicleType)}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:ring-2 focus:ring-blue-600"
              >
                <option value="MOTORBIKE">Xe máy</option>
                <option value="CAR">Ô tô</option>
              </select>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Biển số</label>
              <input
                type="text"
                value={plate}
                placeholder="VD: 30G12345"
                className="w-full rounded-lg border px-3 py-2 text-sm uppercase focus:ring-2 focus:ring-blue-600"
                onChange={(e) => setPlate(e.target.value)}
              />
            </div>
          </div>

          {/* Search btn */}
          <button
            onClick={handleSearch}
            disabled={loading}
            className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-700 py-3 font-medium text-white shadow hover:from-blue-700 hover:to-indigo-800 disabled:opacity-50"
          >
            {loading ? 'Đang tìm kiếm...' : '🔍 Tìm chỗ trống'}
          </button>

          {/* Back btn */}
          <button
            onClick={() => router.push('/customer/dashboard')}
            className="rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
          >
            ⬅️ Quay lại
          </button>
        </div>

        {/* Available spots */}
        {spots.length > 0 && (
          <div className="mt-8 rounded-2xl bg-white p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-semibold text-gray-800">Chọn vị trí (ONLINE)</h2>

            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {spots.map((spot) => (
                <button
                  key={spot.id}
                  disabled={loading}
                  onClick={() =>
                    router.push(
                      `/customer/confirm?spotId=${spot.id}&dateIn=${dateIn}&dateOut=${dateOut}&timeIn=${timeIn}&timeOut=${timeOut}&plate=${plate}&vehicleType=${vehicleType}`
                    )
                  }
                  className="rounded-lg border p-3 text-center shadow hover:border-blue-500 hover:bg-blue-50"
                >
                  <div className="text-lg font-bold text-blue-700">
                    {spot.area}-{spot.position}
                  </div>
                  <div className="text-xs text-gray-500">({spot.vehicleType})</div>
                </button>
              ))}
            </div>

            <p className="mt-3 text-sm text-gray-500">
              Sau khi chọn vị trí, hệ thống sẽ tạo reservation và chuyển bạn sang cổng thanh toán
              VNPAY.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
