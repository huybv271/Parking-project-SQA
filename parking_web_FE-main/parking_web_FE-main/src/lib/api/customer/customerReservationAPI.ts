import { customerClient } from './customerClient';

const USER_BASE = process.env.NEXT_PUBLIC_USER_BASE || '/user';

export type VehicleType = 'CAR' | 'MOTORBIKE';

export interface FreeSpot {
  id: number;
  area: string;
  position: string;
  isActive: boolean;
  vehicleType: VehicleType;
  slotType: 'ONLINE' | 'OFFLINE';
}

export interface AvailableSlotResponse {
  freeSpots: FreeSpot[];
  timeIn: number;
  timeOut: number;
  dateTimeIn: string;
  dateTimeOut: string;
  vehicleType: VehicleType;
}

export interface ReservationSummary {
  id: number;
  date: string;
  timeRange: string;
  blockCount: number;
  plate: string;
  vehicle: VehicleType;
  status: string;
}

export interface ReservationResponse {
  message: string;
  reservation: ReservationSummary;
}

export interface CreateVnpayPaymentResponse {
  reservationId: number;
  paymentId: string;
  amout: string;
  vnpayUrl: string;
}

export interface ReservationHistoryItem {
  id: number;
  dateIn: string;
  dateOut: string;
  startBlock: number;
  blockCount: number;
  plate: string;
  vehicleType: VehicleType;
  area: string | null;
  position: string | null;
}

export interface ReservationHistoryResponse {
  idUser: string;
  message: string;
  reservations: ReservationHistoryItem[];
}

export interface ActiveReservationNumberResponse {
  message: string;
  numbers: number;
}

function normalizeDate(dateStr: string) {
  if (!dateStr) return dateStr;
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr; // fallback nếu string không phải date hợp lệ

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

export const userReservationAPI = {
  async getAvailableSlots(payload: {
    timeIn: number;
    timeOut: number;
    dateTimeIn: string;
    dateTimeOut: string;
    vehicleType: VehicleType;
  }): Promise<AvailableSlotResponse> {
    const { data } = await customerClient.post<AvailableSlotResponse>(
      `${USER_BASE}/parking-lot/available`,
      {
        ...payload,
        dateTimeIn: normalizeDate(payload.dateTimeIn),
        dateTimeOut: normalizeDate(payload.dateTimeOut),
      }
    );
    return data;
  },

  async createReservation(payload: {
    id: number; // spotId
    timeIn: number;
    timeOut: number;
    dateTimeIn: string;
    dateTimeOut: string;
    vehicleType: VehicleType;
    plate: string | null;
  }): Promise<ReservationResponse> {
    const { data } = await customerClient.post<ReservationResponse>(`${USER_BASE}/reservation`, {
      ...payload,
      dateTimeIn: normalizeDate(payload.dateTimeIn),
      dateTimeOut: normalizeDate(payload.dateTimeOut),
      plate: payload.plate ? payload.plate.toUpperCase() : null,
    });
    return data;
  },

  async createVnpayPayment(reservationId: number): Promise<CreateVnpayPaymentResponse> {
    const { data } = await customerClient.post<CreateVnpayPaymentResponse>(
      `${USER_BASE}/payment/vnpay/create`,
      { reservationId }
    );
    return data;
  },

  async getActiveReservationNumber(): Promise<ActiveReservationNumberResponse> {
    const { data } = await customerClient.get<ActiveReservationNumberResponse>(
      `${USER_BASE}/reservations/active/numbers`
    );
    return data;
  },

  async getReservationHistory(idUser: string): Promise<ReservationHistoryResponse> {
    const { data } = await customerClient.get<ReservationHistoryResponse>(
      `${USER_BASE}/reservations`
    );
    return data;
  },
};
