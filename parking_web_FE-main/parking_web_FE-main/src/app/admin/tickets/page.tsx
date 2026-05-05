'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { AdminTicketAPI, Ticket } from '@/lib/api/admin/ticketAPI';
import { Input } from '@/components/ui/input';

export default function TicketsPage() {
  const today = new Date().toISOString().split('T')[0];

  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>(today);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTickets = async (date: string) => {
    try {
      setLoading(true);
      setError(null);

      const res = await AdminTicketAPI.getAllTickets(date);
      setTickets(res.tickets);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch tickets.');
    } finally {
      setLoading(false);
    }
  };

  // 🚀 fetch mặc định hôm nay
  useEffect(() => {
    fetchTickets(selectedDate);
  }, [selectedDate]);

  return (
    <Card className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">🎟️ Tickets</h2>

        {/* 📅 DATE PICKER */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Date:</span>
          <Input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="w-[160px]"
          />
        </div>
      </div>

      {loading && <p className="text-sm text-gray-500">Loading tickets...</p>}
      {error && <p className="text-sm text-red-500">{error}</p>}

      {!loading && !error && (
        <table className="w-full border border-gray-200 text-center text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">ID</th>
              <th className="p-2">Plate</th>
              <th className="p-2">Vehicle</th>
              <th className="p-2">Time In</th>
              <th className="p-2">Time Out</th>
              <th className="p-2">Status</th>
            </tr>
          </thead>

          <tbody>
            {tickets.length === 0 && (
              <tr>
                <td colSpan={6} className="p-4 text-gray-500">
                  No tickets found
                </td>
              </tr>
            )}

            {tickets.map((t) => (
              <tr key={t.id} className="border-t">
                <td className="p-2">{t.id}</td>
                <td className="p-2">{t.plate}</td>
                <td className="p-2">{t.vehicleType}</td>
                <td className="p-2">{t.TimeIn}</td>
                <td className="p-2">{t.TimeOut || '-'}</td>
                <td className="p-2 font-semibold" style={{ color: t.colorCode }}>
                  {t.status.toUpperCase()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  );
}
