'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';
import { AdminStaffAPI } from '@/lib/api/admin/staffAPI';
import type { Staff } from '@/lib/api/admin/staffAPI';

export default function TrashStaffPage() {
  const router = useRouter();
  const [staffs, setStaffs] = useState<Staff[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDeletedStaffs = async () => {
    try {
      const res = await AdminStaffAPI.getDeletedStaffs();
      setStaffs(res.staffs);
      console.log(res.staffs);
    } catch (error) {
      console.error('Fetch trash staffs failed', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestore = async (username: string) => {
    await AdminStaffAPI.restoreStaff(username);
    fetchDeletedStaffs();
  };

  useEffect(() => {
    fetchDeletedStaffs();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🗑️ Deleted Staffs</h1>

      {loading && <p className="text-sm text-muted-foreground">Loading data...</p>}

      {!loading && staffs.length === 0 && (
        <p className="text-sm text-muted-foreground">Không có staff nào trong thùng rác</p>
      )}

      <div className="space-y-3">
        {staffs.map((staff) => (
          <div
            key={staff.username}
            className="flex items-center justify-between rounded-xl border p-4 shadow-sm"
          >
            <div>
              <p className="font-medium">{staff.name}</p>
              <p className="text-sm text-muted-foreground">{staff.role}</p>
            </div>

            <Button variant="outline" onClick={() => handleRestore(staff.username)}>
              ♻️ Restore
            </Button>
          </div>
        ))}
      </div>

      <Button
        onClick={() => router.push('/admin/staffs/list')}
        className="mt-10 rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
      >
        ⬅️ Quay lại
      </Button>
    </div>
  );
}
