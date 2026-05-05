'use client';

import { useEffect, useRef, useState } from 'react';
import { staffTicketAPI } from '@/lib/api/staff/staffTicketAPI';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';

export default function CreateTicketPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const { toast } = useToast();
  const router = useRouter();

  // =====================
  // OPEN CAMERA
  // =====================
  useEffect(() => {
    const openCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }, // camera sau
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        toast({
          title: 'Camera error',
          description: 'Không thể mở camera',
          variant: 'destructive',
        });
      }
    };

    openCamera();
  }, [toast]);

  // =====================
  // CAPTURE FRAME
  // =====================
  const handleScan = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const file = new File([blob], 'plate.jpg', { type: 'image/jpeg' });

      try {
        setLoading(true);
        const data = await staffTicketAPI.checkInImage(file);
        setResult(data);
      } catch (error: any) {
        toast({
          title: 'Check-in failed',
          description: error?.response?.data?.message || 'Không thể nhận diện biển số',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg');
  };

  // =====================
  // AUTO REDIRECT
  // =====================
  useEffect(() => {
    if (result) {
      const timer = setTimeout(() => {
        router.push('/staff/dashboard');
      }, 8000);
      return () => clearTimeout(timer);
    }
  }, [result, router]);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto max-w-3xl rounded bg-white p-6 shadow">
        <h1 className="mb-4 text-2xl font-bold text-green-700">🅿️ Check-in bằng Camera</h1>

        {/* VIDEO */}
        <video ref={videoRef} autoPlay playsInline className="mb-4 w-full rounded border" />

        {/* HIDDEN CANVAS */}
        <canvas ref={canvasRef} className="hidden" />

        <button
          onClick={handleScan}
          disabled={loading}
          className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:bg-blue-300"
        >
          {loading ? 'Đang quét...' : '📸 Quét biển số'}
        </button>

        <button
          onClick={() => router.push('/staff/dashboard')}
          className="mt-5 rounded bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
        >
          ⬅️ Quay lại
        </button>

        {result && (
          <div className="mt-6 rounded border border-green-300 bg-green-50 p-4">
            <h3 className="mb-2 font-semibold text-green-800">✔️ Tạo vé thành công</h3>
            <p>
              <strong>Biển số:</strong> {result.plate}
            </p>
            <p>
              <strong>Khu vực:</strong> {result.area}
            </p>
            <p>
              <strong>Vị trí:</strong> {result.position}
            </p>
            <p>
              <strong>Loại xe:</strong> {result.type}
            </p>
            <p className="mt-2 text-sm text-gray-500">Tự động quay lại sau 8 giây...</p>
          </div>
        )}
      </div>
    </div>
  );
}
