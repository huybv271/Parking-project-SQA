'use client';

import { useState, useEffect, useRef } from 'react';
import { staffTicketAPI } from '@/lib/api/staff/staffTicketAPI';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';

export default function CheckoutTicketPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [stream, setStream] = useState<MediaStream | null>(null);
  const [loading, setLoading] = useState(false);
  const [bill, setBill] = useState<any>(null);
  const [plate, setPlate] = useState<any>(null);

  const { toast } = useToast();
  const router = useRouter();

  // ======================
  // START CAMERA
  // ======================
  useEffect(() => {
    const startCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' },
        });

        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
        setStream(mediaStream);
      } catch (err) {
        toast({
          title: 'Camera error',
          description: 'Không thể mở camera',
          variant: 'destructive',
        });
      }
    };

    startCamera();

    return () => {
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  // ======================
  // CAPTURE & CHECKOUT
  // ======================
  const handleCheckout = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    try {
      setLoading(true);
      setBill(null);

      const video = videoRef.current;
      const canvas = canvasRef.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const blob: Blob | null = await new Promise((resolve) =>
        canvas.toBlob(resolve, 'image/jpeg')
      );

      if (!blob) throw new Error('Capture failed');

      const file = new File([blob], 'checkout.jpg', { type: 'image/jpeg' });

      const data = await staffTicketAPI.checkoutImage(file);

      setBill(data.bill);
      setPlate(data.plate);

      toast({
        title: 'Checkout thành công',
        description: `Xe ${data.plate} đã checkout`,
      });
    } catch (err: any) {
      toast({
        title: 'Checkout failed',
        description: err?.response?.data?.message || 'Lỗi checkout',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  // ======================
  // AUTO REDIRECT
  // ======================
  useEffect(() => {
    if (bill) {
      const timer = setTimeout(() => {
        router.push('/staff/dashboard');
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [bill]);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-6 text-3xl font-bold text-green-700">🏁 Checkout Xe (Camera)</h1>

        <div className="rounded bg-white p-6 shadow">
          <video ref={videoRef} autoPlay playsInline className="mb-4 w-full rounded border" />

          <canvas ref={canvasRef} className="hidden" />

          <button
            onClick={handleCheckout}
            disabled={loading}
            className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:bg-blue-300"
          >
            {loading ? 'Đang xử lý...' : '📸 Quét & Checkout'}
          </button>

          <button
            onClick={() => router.push('/staff/dashboard')}
            className="mt-4 rounded bg-indigo-600 px-4 py-2 text-white"
          >
            ⬅️ Quay lại
          </button>

          {/* ================= BILL RESULT ================= */}

          {bill && (
            <div className="mt-6 rounded border border-green-300 bg-green-50 p-4">
              <h3 className="mb-2 flex items-center gap-2 text-lg font-semibold text-green-800">
                ✔️ Checkout thành công!
              </h3>

              <div className="space-y-1 text-gray-700">
                <p>
                  <strong>Biển số:</strong> {plate}
                </p>
                <p>
                  <strong>Bắt đầu:</strong> {bill.startTime}
                </p>
                <p>
                  <strong>Kết thúc:</strong> {bill.finishTime}
                </p>
                <p>
                  <strong>Đã thanh toán online:</strong> {bill.payedMoney}đ
                </p>
                <p>
                  <strong>Phí cần trả thêm:</strong> {bill.totalPrice}đ
                </p>
              </div>

              <div className="mt-5 flex gap-4">
                <div>
                  <p className="text-sm text-gray-600">Ảnh check-in</p>
                  <img
                    src={bill.urlCloudinaryCheckIn}
                    alt="Check-in"
                    className="w-32 rounded shadow"
                  />
                </div>

                <div>
                  <p className="text-sm text-gray-600">Ảnh check-out</p>
                  <img
                    src={bill.urlCloudinaryCheckOut}
                    alt="Check-out"
                    className="w-32 rounded shadow"
                  />
                </div>
              </div>

              <p className="mt-3 text-sm text-gray-500">Sẽ tự động quay lại trong 10 giây...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
