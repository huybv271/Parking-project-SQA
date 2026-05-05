// 'use client';

// import { useEffect, useState } from 'react';
// import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
// import { userReservationAPI } from '@/lib/api/customer/customerReservationAPI';

// function StatusBadge({ status, color }: { status: string; color: string }) {
//   const labelMap: Record<string, string> = {
//     PENDING: 'Chờ xác nhận',
//     CONFIRMED: 'Sắp tới',
//     CHECKIN: 'Đang hoạt động',
//     CHECKOUT: 'Đã xong',
//   };

//   return (
//     <span
//       className="rounded-full px-2 py-1 text-xs font-semibold text-white"
//       style={{ backgroundColor: color }}
//     >
//       {labelMap[status] || status}
//     </span>
//   );
// }

// export default function CustomerHistoryPage() {
//   const { user, loading } = useCustomerAuth();
//   const username = user?.username;

//   const [reservations, setReservations] = useState<any[]>([]);
//   // const [loadingRes, setLoadingRes] = useState(true);

//   useEffect(() => {
//     if (!user?.username) return;

//     const username: string = user.username;

//     async function fetchHistory() {
//       const res = await userReservationAPI.getReservationHistory(username);
//       setReservations(res.reservations);
//       console.log(res.reservations);
//     }

//     fetchHistory();
//   }, [user?.username]);

//   if (loading) {
//     return <div className="p-8">Loading...</div>;
//   }

//   if (!username) {
//     return <div className="p-8 text-red-500">Not authenticated</div>;
//   }

//   return (
//     <div className="p-8">
//       <h1 className="mb-6 text-2xl font-bold">📜 Lịch sử đặt chỗ</h1>

//       {reservations.length === 0 ? (
//         <p className="text-gray-600">Chưa có lịch sử đặt chỗ.</p>
//       ) : (
//         <div className="rounded-lg bg-white shadow">
//           <table className="w-full">
//             <thead className="bg-gray-100">
//               <tr>
//                 <th className="p-3 text-left">Ngày</th>
//                 <th className="p-3 text-left">Giờ</th>
//                 <th className="p-3 text-left">Biển số</th>
//                 <th className="p-3 text-left">Vị trí</th>
//                 <th className="p-3 text-left">Loại xe</th>
//                 <th className="p-3 text-left">Trạng thái</th>
//               </tr>
//             </thead>
//             <tbody>
//               {reservations.map((r) => (
//                 <tr key={r.id} className="border-t">
//                   <td className="p-3">{new Date(r.dateIn).toLocaleDateString()}</td>

//                   <td className="p-3">
//                     {r.startBlock}h – {r.startBlock + r.blockCount}h
//                   </td>

//                   <td className="p-3 font-medium">{r.plate}</td>

//                   <td className="p-3">
//                     {r.area}-{r.position}
//                   </td>

//                   <td className="p-3">{r.vehicleType}</td>

//                   <td className="flex items-center gap-2 p-3">
//                     <StatusBadge status={r.status} color={r.color} />
//                     <span className="text-sm text-gray-700">{r.status}</span>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// }

'use client';

import { useEffect, useState } from 'react';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { userReservationAPI } from '@/lib/api/customer/customerReservationAPI';
import { useRouter } from 'next/navigation';

/* =======================
   Color → Label mapping
======================= */
const COLOR_LABEL_MAP: Record<string, string> = {
  '#F59E0B': 'Chờ xác nhận',
  '#10B981': 'Sắp tới',
  '#0EA5E9': 'Đang hoạt động',
  '#ca4126ff': 'Đã xong',
};

/* =======================
   Status Badge
======================= */
function StatusBadge({ color }: { color: string }) {
  const label = COLOR_LABEL_MAP[color] ?? 'Không xác định';

  return (
    <span
      className="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium text-white shadow-sm"
      style={{ backgroundColor: color }}
    >
      <span className="h-2 w-2 rounded-full bg-white/80" />
      {label}
    </span>
  );
}

/* =======================
   Page
======================= */
export default function CustomerHistoryPage() {
  const { user, loading } = useCustomerAuth();
  const username = user?.username;

  const [reservations, setReservations] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (!user?.username) return;

    const username: string = user.username;

    async function fetchHistory() {
      const res = await userReservationAPI.getReservationHistory(username);
      setReservations(res.reservations);
      console.log(res.reservations);
    }

    fetchHistory();
  }, [user?.username]);

  if (loading) {
    return <div className="p-8 text-gray-600">Loading...</div>;
  }

  if (!username) {
    return <div className="p-8 text-red-500">Not authenticated</div>;
  }

  return (
    <div className="p-8">
      <h1 className="mb-6 text-2xl font-bold">📜 Lịch sử đặt chỗ</h1>

      {reservations.length === 0 ? (
        <p className="text-gray-600">Chưa có lịch sử đặt chỗ.</p>
      ) : (
        <div className="overflow-hidden rounded-xl bg-white shadow">
          <table className="w-full border-separate border-spacing-y-2">
            <thead className="bg-gray-100 text-sm font-semibold text-gray-700">
              <tr>
                <th className="p-4 text-left">Ngày</th>
                <th className="p-4 text-left">Giờ</th>
                <th className="p-4 text-left">Biển số</th>
                <th className="p-4 text-left">Vị trí</th>
                <th className="p-4 text-left">Loại xe</th>
                <th className="p-4 text-left">Trạng thái</th>
              </tr>
            </thead>

            <tbody>
              {reservations.map((r) => (
                <tr key={r.id} className="rounded-lg bg-white transition hover:bg-gray-50">
                  <td className="p-4 text-sm text-gray-700">
                    {new Date(r.dateIn).toLocaleDateString()}
                  </td>

                  <td className="p-4 text-sm text-gray-700">
                    {r.startBlock}h – {r.startBlock + r.blockCount}h
                  </td>

                  <td className="p-4 font-medium text-gray-900">{r.plate}</td>

                  <td className="p-4 text-sm text-gray-700">
                    {r.area}-{r.position}
                  </td>

                  <td className="p-4 text-sm text-gray-700">{r.vehicleType}</td>

                  <td className="p-4">
                    <StatusBadge color={r.color} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <button
        onClick={() => router.push('/customer/dashboard')}
        className="mt-10 rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
      >
        ⬅️ Quay lại
      </button>
    </div>
  );
}
