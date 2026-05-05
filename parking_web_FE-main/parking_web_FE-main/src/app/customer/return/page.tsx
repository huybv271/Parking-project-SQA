'use client';

import { useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useToast } from '@/hooks/use-toast';

export default function CustomerPaymentReturnPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    const rspCode = searchParams.get('RspCode');

    const timer = setTimeout(() => {
      if (rspCode === '00') {
        toast({
          title: 'Thanh toán thành công 🎉',
          description: 'Đơn hàng đã được xác nhận',
        });

        router.replace('/customer/dashboard');
      } else {
        toast({
          title: 'Thanh toán thất bại ❌',
          description: 'Vui lòng thử lại hoặc liên hệ hỗ trợ',
          variant: 'destructive',
        });

        router.replace('/customer/dashboard');
      }
    }, 800);

    return () => clearTimeout(timer);
  }, [searchParams, router, toast]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="rounded-xl bg-white p-6 text-center shadow-md">
        <h2 className="text-lg font-semibold">Đang xử lý kết quả thanh toán…</h2>
        <p className="mt-2 text-gray-600">Vui lòng chờ trong giây lát 🚀</p>
      </div>
    </div>
  );
}
