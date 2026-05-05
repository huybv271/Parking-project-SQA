'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AdminStaffAPI } from '@/lib/api/admin/staffAPI';
import { useRouter } from 'next/navigation';

export default function StaffDetailPage() {
  const { username } = useParams<{ username: string }>();
  const [staff, setStaff] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchStaff = async () => {
      try {
        const res = await AdminStaffAPI.getStaff(username);
        setStaff(res.staff);
        console.log(res.staff);
      } finally {
        setLoading(false);
      }
    };

    fetchStaff();
  }, [username]);

  if (loading) return <p>Loading...</p>;
  if (!staff) return <p>Staff not found</p>;

  return (
    <div className="max-w-xl">
      <Card>
        <CardHeader>
          <CardTitle>👤 Staff Detail</CardTitle>
        </CardHeader>

        <CardContent className="space-y-3">
          <div>
            <span className="font-semibold">Username:</span> {staff.username}
          </div>

          <div>
            <span className="font-semibold">Name:</span> {staff.name}
          </div>

          <div>
            <span className="font-semibold">Date:</span> {staff.date}
          </div>

          <div>
            <span className="font-semibold">Status:</span>{' '}
            <span
              className={
                staff.status === true ? 'font-medium text-green-600' : 'font-medium text-red-600'
              }
            >
              {staff.status === true ? 'Active' : 'Inactive'}
            </span>
          </div>
        </CardContent>
      </Card>
      <Button
        onClick={() => router.push('/admin/staffs/list')}
        className="mt-10 rounded-lg bg-gray-200 px-4 py-2 text-sm text-gray-800 hover:bg-gray-300"
      >
        ⬅️ Quay lại
      </Button>
    </div>
  );
}
