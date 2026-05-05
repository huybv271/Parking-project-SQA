import { staffClient } from '../staff/staffClient';

export interface TrafficFlowResponse {
  message: string;
  checkInNumbers: number[];
  checkOutNumbers: number[];
}

export const TrafficFlowAPI = {
  async getTrafficFlow(date?: string): Promise<TrafficFlowResponse> {
    const today = new Date().toISOString().split('T')[0];
    const { data } = await staffClient.post<TrafficFlowResponse>('/admin/traffic-flow', {
      date: date || today,
    });
    return data;
  },
};
