// 'use client';

// import { useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
// import { useStaffAuth } from '@/contexts/StaffAuthContext';
// import { io } from 'socket.io-client';
// import { parkingAPI } from '@/lib/api/user';

// export default function HomePage() {
//   const router = useRouter();

//   const { isAuthenticated: isCustomerAuth, loading: loadingCustomer, user } = useCustomerAuth();
//   const { isAuthenticated: isStaffAuth, loading: loadingStaff, staff } = useStaffAuth();
//   const loading = loadingCustomer || loadingStaff;

//   const [slots, setSlots] = useState({
//     car: 0,
//     motorbike: 0,
//   });

//   // ===========================
//   //  LOAD  DATA
//   // ===========================
//   useEffect(() => {
//     async function load() {
//       try {
//         const data = await parkingAPI.getSlotStatus();
//         setSlots({
//           car: data.carNumbers,
//           motorbike: data.motorNumbers,
//         });
//         console.log(data);
//       } catch (e) {
//         console.log('Load slot error:', e);
//       }
//     }
//     load();
//   }, []); // ← MUST HAVE []

//   // ===========================
//   // 🔥 REALTIME SOCKET (#2)
//   // ===========================
//   useEffect(() => {
//     const socket = io('http://localhost:8080');

//     socket.emit('get-current-slots');

//     socket.on('slotStatus', (payload) => {
//       if (payload?.data) {
//         setSlots({
//           car: payload.data.carNumbers,
//           motorbike: payload.data.motorNumbers,
//         });
//       }
//     });

//     return () => {
//       socket.disconnect(); // ✔ CHỈ RETURN 1 HÀM cleanup
//     };
//   }, []);

//   // ===========================
//   // 🔥 REDIRECT NẾU ĐÃ LOGIN
//   // ===========================
//   useEffect(() => {
//     if (loading) return;

//     if (isStaffAuth && staff) {
//       router.replace('/staff/dashboard');
//       return;
//     }

//     if (isCustomerAuth && user) {
//       router.replace('/customer/dashboard');
//       return;
//     }
//   }, [loading, isCustomerAuth, isStaffAuth, router, user, staff]);

//   // ===========================
//   // LOADING
//   // ===========================
//   if (loading) {
//     return (
//       <div className="flex min-h-screen items-center justify-center">
//         <div className="text-center">
//           <div className="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
//           <p className="mt-4 text-gray-600">Đang tải...</p>
//         </div>
//       </div>
//     );
//   }

//   // ===========================
//   // HOMEPAGE UI
//   // ===========================
//   return (
//     <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
//       <div className="w-full max-w-4xl rounded-2xl bg-white p-10 shadow-xl">
//         <h1 className="text-center text-3xl font-bold text-indigo-700">Xin chào!</h1>
//         <p className="mt-2 text-center text-lg text-gray-600">
//           Chào mừng đến hệ thống đặt chỗ xe thông minh <strong>LICHT-PARKING</strong>
//         </p>

//         {/* SLOT CARD */}
//         <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
//           <div className="rounded-xl border bg-indigo-50 p-6 text-center shadow">
//             <div className="mb-2 text-4xl">🚗</div>
//             <div className="text-xl font-semibold">
//               <span className="text-green-600">{slots.car}</span> /{' '}
//             </div>
//             <p className="mt-1 text-gray-600">Remaining Car Slots</p>
//           </div>

//           <div className="rounded-xl border bg-indigo-50 p-6 text-center shadow">
//             <div className="mb-2 text-4xl">🏍️</div>
//             <div className="text-xl font-semibold">
//               <span className="text-green-600">{slots.motorbike}</span> /{' '}
//             </div>
//             <p className="mt-1 text-gray-600">Remaining Motorbike Slots</p>
//           </div>
//         </div>

//         <div className="mt-10 flex justify-center gap-4">
//           <a
//             href="/auth/login"
//             className="rounded-lg bg-indigo-600 px-5 py-3 text-white shadow hover:bg-indigo-700"
//           >
//             🔐 Đăng nhập
//           </a>
//         </div>
//       </div>
//     </div>
//   );
// }

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCustomerAuth } from '@/contexts/CustomerAuthContext';
import { useStaffAuth } from '@/contexts/StaffAuthContext';
import { parkingAPI } from '@/lib/api/user';
import { getSocket } from '@/lib/socket';

export default function HomePage() {
  const router = useRouter();

  const { isAuthenticated: isCustomerAuth, loading: loadingCustomer, user } = useCustomerAuth();
  const { isAuthenticated: isStaffAuth, loading: loadingStaff, staff } = useStaffAuth();
  const loading = loadingCustomer || loadingStaff;

  const [slots, setSlots] = useState({
    car: 0,
    motorbike: 0,
  });

  // ===========================
  // LOAD INIT DATA (REST)
  // ===========================
  useEffect(() => {
    async function load() {
      try {
        const data = await parkingAPI.getSlotStatus();
        setSlots({
          car: data.carNumbers,
          motorbike: data.motorNumbers,
        });
      } catch (e) {
        console.log('Load slot error:', e);
      }
    }
    load();
  }, []);

  // ===========================
  // 🔥 REALTIME SOCKET (SINGLETON)
  // ===========================
  useEffect(() => {
    const socket = getSocket();

    socket.emit('get-current-slots');

    const handleSlotUpdate = (payload: any) => {
      if (payload?.data) {
        setSlots({
          car: payload.data.carNumbers,
          motorbike: payload.data.motorNumbers,
        });
      }
    };

    socket.on('slotStatus', handleSlotUpdate);

    return () => {
      socket.off('slotStatus', handleSlotUpdate);
      // ❌ không disconnect – để socket dùng chung toàn app
    };
  }, []);

  // ===========================
  // REDIRECT
  // ===========================
  useEffect(() => {
    if (loading) return;

    if (isStaffAuth && staff) {
      router.replace('/staff/dashboard');
      return;
    }

    if (isCustomerAuth && user) {
      router.replace('/customer/dashboard');
      return;
    }
  }, [loading, isCustomerAuth, isStaffAuth, router, user, staff]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Đang tải...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="w-full max-w-4xl rounded-2xl bg-white p-10 shadow-xl">
        <h1 className="text-center text-3xl font-bold text-indigo-700">Xin chào!</h1>
        <p className="mt-2 text-center text-lg text-gray-600">
          Chào mừng đến hệ thống đặt chỗ xe thông minh <strong>LICHT-PARKING</strong>
        </p>

        {/* SLOT CARD */}
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div className="rounded-xl border bg-indigo-50 p-6 text-center shadow">
            <div className="mb-2 text-4xl">🚗</div>
            <div className="text-xl font-semibold">
              <span className="text-green-600">{slots.car}</span>
            </div>
            <p className="mt-1 text-gray-600">Remaining Car Slots</p>
          </div>

          <div className="rounded-xl border bg-indigo-50 p-6 text-center shadow">
            <div className="mb-2 text-4xl">🏍️</div>
            <div className="text-xl font-semibold">
              <span className="text-green-600">{slots.motorbike}</span>
            </div>
            <p className="mt-1 text-gray-600">Remaining Motorbike Slots</p>
          </div>
        </div>

        <div className="mt-10 flex justify-center gap-4">
          <a
            href="/auth/login"
            className="rounded-lg bg-indigo-600 px-5 py-3 text-white shadow hover:bg-indigo-700"
          >
            🔐 Đăng nhập
          </a>
        </div>
      </div>
    </div>
  );
}
