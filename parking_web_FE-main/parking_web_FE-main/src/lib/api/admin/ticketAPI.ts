import { staffClient } from '../staff/staffClient';

/* ================= TYPES ================= */

export interface Ticket {
  id: number;
  spotId: number;
  plate: string;
  vehicleType: 'CAR' | 'MOTORBIKE';
  TimeIn: string;
  TimeOut: string | null;
  status: 'active' | 'inactive';
  colorCode: string;
}

export interface TicketResponse {
  message: string;
  tickets: Ticket[];
}

/* ================= API ================= */

export const AdminTicketAPI = {
  async getAllTickets(date?: string): Promise<TicketResponse> {
    const today = date || new Date().toISOString().split('T')[0]; // yyyy-mm-dd
    const { data } = await staffClient.post<TicketResponse>('/admin/allTickets', { date: today });
    return data;
  },
};
