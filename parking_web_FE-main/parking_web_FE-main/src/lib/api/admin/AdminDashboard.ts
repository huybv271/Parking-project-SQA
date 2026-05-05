import { staffClient } from '../staff/staffClient';

export interface NowRevenueResponse {
  message: string;
  sum: number;
}

export interface MonthlyRevenueResponse {
  message: string;
  year: number;
  chartData: {
    labels: string[];
    data: number[];
  };
}

export interface RatioVehicleResponse {
  message: string;
  onlineCarRate: number;
  onlineMotorRate: number;
  offlineCarRate: number;
  offlineMotorRate: number;
}

export interface ParkingRate {
  vehicleType: string;
  unitPrice: number;
  currency: string;
  ticketType: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

export interface ParkingRateResponse {
  message: string;
  parkingRate: ParkingRate[];
}

export const AdminDashboardAPI = {
  async getNowRevenue(): Promise<NowRevenueResponse> {
    const { data } = await staffClient.post<NowRevenueResponse>('/admin/nowRevenue');
    return data;
  },

  async getMonthlyRevenue(): Promise<MonthlyRevenueResponse> {
    const { data } = await staffClient.get<MonthlyRevenueResponse>('/admin/MonthlyRevenue');
    return data;
  },

  async getRatioVehicle(): Promise<RatioVehicleResponse> {
    const { data } = await staffClient.get<RatioVehicleResponse>('/admin/vehicleRatio');
    return data;
  },

  async getParkingRate(): Promise<ParkingRateResponse> {
    const { data } = await staffClient.get<ParkingRateResponse>('/admin/ParkingRate');
    return data;
  },

  async createNewParkingRate(payload: {
    vehicleType: string;
    unitPrice: number;
    ticketType: string;
  }): Promise<{ message: string }> {
    const { data } = await staffClient.post('/admin/newParkingRateType', payload);
    return data;
  },
};
