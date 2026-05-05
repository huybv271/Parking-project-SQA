'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { AdminStaffAPI, Staff } from '@/lib/api/admin/staffAPI';
import { Button } from '@/components/ui/button';

export default function StaffListPage() {
  const [staffs, setStaffs] = useState<Staff[]>([]);
  const [loading, setLoading] = useState(true);

  const loadStaffs = async () => {
    try {
      setLoading(true);
      const res = await AdminStaffAPI.getAllStaffs();
      setStaffs(res.staffs);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (username: string) => {
    if (!confirm('Bạn chắc chắn muốn xoá staff này?')) return;
    await AdminStaffAPI.deleteStaff(username);
    loadStaffs();
  };

  useEffect(() => {
    loadStaffs();
  }, []);

  if (loading) return <p>Đang tải danh sách staff...</p>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between">
        <h1 className="text-2xl font-bold">👥 Staff List</h1>
      </div>

      <table className="w-full border text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Username</th>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Status</th>
            <th className="px-4 py-2 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          {staffs.map((s) => (
            <tr key={s.username} className="border-t">
              <td className="px-4 py-2">{s.username}</td>
              <td className="px-4 py-2">{s.name}</td>
              <td className="px-4 py-2">{s.status === 1 ? 'Active' : 'Inactive'}</td>
              <td className="px-4 py-2 text-center">
                <Link href={`/admin/staffs/${s.username}`}>
                  <Button size="sm" variant="outline" className="mr-5">
                    View
                  </Button>
                </Link>
                <Button size="sm" variant="destructive" onClick={() => handleDelete(s.username)}>
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
