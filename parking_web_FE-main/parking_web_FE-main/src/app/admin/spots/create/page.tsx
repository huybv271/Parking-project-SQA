'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { AdminSpotAPI, CreateSpotPayload } from '@/lib/api/admin/spotAPI';
import { useToast } from '@/hooks/use-toast';

export default function CreateSpotPage() {
  const { toast } = useToast();
  const router = useRouter();

  const [form, setForm] = useState<CreateSpotPayload>({
    area: '',
    slotNumber: 1,
    vehicleType: 'CAR',
    slotType: 'ONLINE',
  });

  const handleSubmit = async () => {
    try {
      await AdminSpotAPI.createSpot(form);
      toast({ title: 'Tạo spot thành công' });
      router.push('/admin/spots/A');
    } catch (err: any) {
      toast({
        title: 'Lỗi',
        description: err?.response?.data?.message || 'Không thể tạo spot',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card className="max-w-2xl">
      <CardHeader>
        <CardTitle>Create Spot</CardTitle>
        <CardDescription>Tạo vị trí đỗ xe mới cho hệ thống</CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Area */}
        <div className="space-y-2">
          <Label>Khu vực (Area)</Label>
          <Input
            placeholder="Ví dụ: A, B, C..."
            value={form.area}
            onChange={(e) => setForm({ ...form, area: e.target.value })}
          />
        </div>

        {/* Slot number */}
        <div className="space-y-2">
          <Label>Số lượng slot</Label>
          <Input
            type="number"
            min={1}
            value={form.slotNumber}
            onChange={(e) => setForm({ ...form, slotNumber: Number(e.target.value) })}
          />
        </div>

        {/* Vehicle type */}
        <div className="space-y-2">
          <Label>Loại xe</Label>
          <Select
            value={form.vehicleType}
            onValueChange={(value) =>
              setForm({ ...form, vehicleType: value as 'CAR' | 'MOTORBIKE' })
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Chọn loại xe" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="CAR">Ô tô</SelectItem>
              <SelectItem value="MOTORBIKE">Xe máy</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Slot type */}
        <div className="space-y-2">
          <Label>Kiểu slot</Label>
          <Select
            value={form.slotType}
            onValueChange={(value) => setForm({ ...form, slotType: value as 'ONLINE' | 'OFFLINE' })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Chọn kiểu slot" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ONLINE">Online</SelectItem>
              <SelectItem value="OFFLINE">Offline</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3 pt-4">
          <Button variant="outline" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button onClick={handleSubmit}>Create Spot</Button>
        </div>
      </CardContent>
    </Card>
  );
}
