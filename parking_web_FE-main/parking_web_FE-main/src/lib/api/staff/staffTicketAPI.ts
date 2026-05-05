import { staffClient } from './staffClient';

const STAFF_BASE = process.env.NEXT_PUBLIC_STAFF_BASE || '/staff';

export interface CheckinResponse {
  area: string;
  position: string;
  plate: string;
  type: string;
}

export interface CheckoutBill {
  channel: string;
  payedMoney: number;
  startTime: string;
  finishTime: string;
  totalPrice: number;
  urlCloudinaryCheckIn: string;
  urlCloudinaryCheckOut: string;
}

export interface CheckoutResponse {
  message: string;
  bill: CheckoutBill;
  plate: string;
}

export const staffTicketAPI = {
  async checkInImage(file: File): Promise<CheckinResponse> {
    const form = new FormData();
    form.append('image', file);

    const { data } = await staffClient.post<CheckinResponse>(`${STAFF_BASE}/ticket-entry`, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },

  async checkoutImage(file: File): Promise<CheckoutResponse> {
    const form = new FormData();
    form.append('image', file);

    const { data } = await staffClient.post<CheckoutResponse>(`${STAFF_BASE}/free-endtry`, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },
};
