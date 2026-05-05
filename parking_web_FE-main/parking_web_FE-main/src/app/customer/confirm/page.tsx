// 'use client';
// import { useSearchParams, useRouter } from 'next/navigation';
// import { userReservationAPI, VehicleType } from '@/lib/api/customer/customerReservationAPI';
// import { useState, useEffect } from 'react';
// import { useToast } from '@/hooks/use-toast';

// export default function ConfirmReservationPage() {
//   const search = useSearchParams();
//   const router = useRouter();
//   const { toast } = useToast();

//   // ====== Lấy param và validate ======
//   const spotId = Number(search.get('spotId') ?? NaN);
//   const rawDateIn = search.get('dateIn');
//   const rawDateOut = search.get('dateOut');
//   const rawTimeIn = search.get('timeIn');
//   const rawTimeOut = search.get('timeOut');

//   const plate = search.get('plate') ?? ''; // luôn là string
//   const vehicleType = (search.get('vehicleType') as VehicleType) ?? 'MOTORBIKE';

//   const [loading, setLoading] = useState(false);

//   // Nếu param thiếu → quay lại trang booking
//   useEffect(() => {
//     if (Number.isNaN(spotId) || !rawDateIn || !rawDateOut || !rawTimeIn || !rawTimeOut) {
//       router.push('/customer');
//     }
//   }, []);

//   // parse số đúng cách
//   const timeIn = Number(rawTimeIn);
//   const timeOut = Number(rawTimeOut);
//   const dateIn = rawDateIn!;
//   const dateOut = rawDateOut!;

//   const handleConfirm = async () => {
//     try {
//       setLoading(true);

//       const reservationRes = await userReservationAPI.createReservation({
//         id: spotId,
//         dateTimeIn: dateIn,
//         dateTimeOut: dateOut,
//         timeIn,
//         timeOut,
//         vehicleType,
//         plate: plate.toUpperCase(),
//       });

//       toast({
//         title: 'Reservation Successful',
//         description: reservationRes.message,
//       });

//       const paymentRes = await userReservationAPI.createVnpayPayment(reservationRes.reservation.id);

//       window.location.href = paymentRes.vnpayUrl;
//     } catch (e: any) {
//       toast({
//         title: 'Error',
//         description: e?.response?.data?.message || 'Failed to create reservation!',
//         variant: 'destructive',
//       });
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="flex min-h-screen justify-center bg-gray-100 p-6">
//       <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
//         <h1 className="mb-4 text-center text-xl font-bold">Xác nhận đặt chỗ</h1>

//         <div className="space-y-2 text-gray-700">
//           <p>
//             <strong>Vị trí:</strong> Slot #{spotId}
//           </p>
//           <p>
//             <strong>Ngày vào:</strong> {dateIn}
//           </p>
//           <p>
//             <strong>Giờ vào:</strong> {timeIn}h
//           </p>
//           <p>
//             <strong>Ngày ra:</strong> {dateOut}
//           </p>
//           <p>
//             <strong>Giờ ra:</strong> {timeOut}h
//           </p>
//           <p>
//             <strong>Loại xe:</strong> {vehicleType}
//           </p>
//           <p>
//             <strong>Biển số:</strong> {plate}
//           </p>
//         </div>

//         <div className="mt-6 flex gap-3">
//           <button
//             className="flex-1 rounded-lg border bg-gray-200 py-2"
//             onClick={() => router.back()}
//           >
//             ⬅️ Quay lại
//           </button>

//           <button
//             className="flex-1 rounded-lg bg-blue-600 py-2 text-white"
//             disabled={loading}
//             onClick={handleConfirm}
//           >
//             {loading ? 'Đang xử lý...' : 'Xác nhận & Thanh toán'}
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import { userReservationAPI, VehicleType } from '@/lib/api/customer/customerReservationAPI';
import { useState, useEffect } from 'react';
import { useToast } from '@/hooks/use-toast';

export default function ConfirmReservationPage() {
  const search = useSearchParams();
  const router = useRouter();
  const { toast } = useToast();

  // ===== Params =====
  const spotId = Number(search.get('spotId'));
  const dateIn = search.get('dateIn');
  const dateOut = search.get('dateOut');
  const timeIn = Number(search.get('timeIn'));
  const timeOut = Number(search.get('timeOut'));
  const plate = search.get('plate') ?? '';
  const vehicleType = (search.get('vehicleType') as VehicleType) ?? 'MOTORBIKE';

  const [loading, setLoading] = useState(false);
  const [paymentUrl, setPaymentUrl] = useState<string | null>(null);
  const [reservationId, setReservationId] = useState<number | null>(null);

  // ===== Validate params =====
  useEffect(() => {
    if (
      Number.isNaN(spotId) ||
      !dateIn ||
      !dateOut ||
      Number.isNaN(timeIn) ||
      Number.isNaN(timeOut)
    ) {
      router.replace('/customer');
    }
  }, []);

  // ===== Confirm reservation =====
  const handleConfirm = async () => {
    try {
      setLoading(true);

      const reservationRes = await userReservationAPI.createReservation({
        id: spotId,
        dateTimeIn: dateIn!,
        dateTimeOut: dateOut!,
        timeIn,
        timeOut,
        vehicleType,
        plate: plate.toUpperCase(),
      });

      setReservationId(reservationRes.reservation.id);

      toast({
        title: 'Reservation created ✅',
        description: 'Vui lòng tiến hành thanh toán để xác nhận chỗ',
      });

      const paymentRes = await userReservationAPI.createVnpayPayment(reservationRes.reservation.id);

      setPaymentUrl(paymentRes.vnpayUrl);
    } catch (e: any) {
      toast({
        title: 'Error ❌',
        description: e?.response?.data?.message || 'Không thể tạo reservation',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
        <h1 className="mb-4 text-center text-xl font-bold">Xác nhận đặt chỗ</h1>

        {/* Info */}
        <div className="space-y-2 text-gray-700">
          <p>
            <strong>Slot:</strong> #{spotId}
          </p>
          <p>
            <strong>Ngày vào:</strong> {dateIn}
          </p>
          <p>
            <strong>Giờ vào:</strong> {timeIn}h
          </p>
          <p>
            <strong>Ngày ra:</strong> {dateOut}
          </p>
          <p>
            <strong>Giờ ra:</strong> {timeOut}h
          </p>
          <p>
            <strong>Loại xe:</strong> {vehicleType}
          </p>
          <p>
            <strong>Biển số:</strong> {plate}
          </p>
        </div>

        {/* Actions */}
        {!paymentUrl && (
          <div className="mt-6 flex gap-3">
            <button
              className="flex-1 rounded-lg border bg-gray-200 py-2"
              onClick={() => router.back()}
            >
              ⬅️ Quay lại
            </button>

            <button
              className="flex-1 rounded-lg bg-blue-600 py-2 text-white disabled:opacity-50"
              disabled={loading}
              onClick={handleConfirm}
            >
              {loading ? 'Đang xử lý…' : 'Xác nhận đặt chỗ'}
            </button>
          </div>
        )}

        {/* Payment CTA */}
        {paymentUrl && (
          <div className="mt-6 rounded-lg border border-green-300 bg-green-50 p-4 text-center">
            <p className="mb-3 text-sm text-gray-700">
              Reservation đã được tạo. Hoàn tất thanh toán để xác nhận chỗ 🚀
            </p>

            <a
              href={paymentUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700"
            >
              Thanh toán với VNPAY →
            </a>

            <p className="mt-3 text-xs text-gray-500">
              Sau khi thanh toán xong, bạn sẽ được tự động quay lại hệ thống
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
