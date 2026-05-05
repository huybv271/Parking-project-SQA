'use client';

import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

type VehicleRatio = {
  onlineCarRate: number;
  onlineMotorRate: number;
  offlineCarRate: number;
  offlineMotorRate: number;
};

const COLORS = ['#2563eb', '#22c55e'];

export default function VehicleRatioChart({ data }: { data: VehicleRatio }) {
  const onlineData = [
    { name: 'Car', value: data.onlineCarRate },
    { name: 'Motor', value: data.onlineMotorRate },
  ];

  const offlineData = [
    { name: 'Car', value: data.offlineCarRate },
    { name: 'Motor', value: data.offlineMotorRate },
  ];

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      {/* ONLINE */}
      <div className="h-[260px]">
        <h3 className="mb-2 text-center font-semibold">Online Slots (% over total)</h3>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={onlineData}
              dataKey="value"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={3}
            >
              {onlineData.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value?: number) => (typeof value === 'number' ? `${value}%` : '0%')}
            />

            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* OFFLINE */}
      <div className="h-[260px]">
        <h3 className="mb-2 text-center font-semibold">Offline Slots (% over total)</h3>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={offlineData}
              dataKey="value"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={3}
            >
              {offlineData.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value?: number) => (typeof value === 'number' ? `${value}%` : '0%')}
            />

            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
