'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AdminStaffAPI } from '@/lib/api/admin/staffAPI';

export default function CreateStaffPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: '',
    date: '',
    username: '',
    password: '',
  });

  const handleSubmit = async () => {
    if (!form.name || !form.date || !form.username || !form.password) {
      alert('Vui lòng nhập đầy đủ thông tin');
      return;
    }

    try {
      setLoading(true);
      await AdminStaffAPI.createStaff(form);
      router.push('/admin/staffs/list');
    } catch (err) {
      console.error(err);
      alert('Tạo staff thất bại');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl">
      <Card>
        <CardHeader>
          <CardTitle>Create Staff</CardTitle>
          <CardDescription>Tạo tài khoản nhân viên mới cho hệ thống</CardDescription>
        </CardHeader>

        <CardContent className="space-y-5">
          {/* NAME */}
          <div className="space-y-1">
            <label className="text-sm font-medium">Tên nhân viên</label>
            <input
              className="w-full rounded-md border px-3 py-2"
              placeholder="Nhập tên"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </div>

          {/* DATE */}
          <div className="space-y-1">
            <label className="text-sm font-medium">Ngày tạo</label>
            <input
              type="date"
              className="w-full rounded-md border px-3 py-2"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
            />
          </div>

          {/* USERNAME */}
          <div className="space-y-1">
            <label className="text-sm font-medium">Username</label>
            <input
              className="w-full rounded-md border px-3 py-2"
              placeholder="Nhập username"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
          </div>

          {/* PASSWORD */}
          <div className="space-y-1">
            <label className="text-sm font-medium">Mật khẩu</label>
            <input
              type="password"
              className="w-full rounded-md border px-3 py-2"
              placeholder="Nhập mật khẩu"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>

          {/* ACTIONS */}
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="outline" onClick={() => router.back()}>
              Cancel
            </Button>
            <Button onClick={handleSubmit} disabled={loading}>
              {loading ? 'Creating...' : 'Create Staff'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
