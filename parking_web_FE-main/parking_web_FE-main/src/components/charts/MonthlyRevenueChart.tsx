// 'use client';

// import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

// type MonthlyChart = {
//   labels: string[];
//   data: number[];
// };

// export default function MonthlyRevenueChart({ data }: { data: MonthlyChart }) {
//   const chartData = data.labels.map((label, index) => ({
//     month: label,
//     revenue: data.data[index] || 0,
//   }));

//   return (
//     <div className="h-[360px] w-full">
//       <ResponsiveContainer width="100%" height="100%">
//         <BarChart data={chartData}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis dataKey="month" />
//           <YAxis tickFormatter={(v) => `${(v / 1_000_000).toFixed(0)}M`} />
//           <Tooltip
//             formatter={(value) =>
//               typeof value === 'number' ? `${value.toLocaleString()} VND` : '0 VND'
//             }
//           />

//           <Bar
//             dataKey="revenue"
//             fill="#4f46e5" // indigo-600
//             radius={[6, 6, 0, 0]}
//           />
//         </BarChart>
//       </ResponsiveContainer>
//     </div>
//   );
// }

import { GenericBarChart } from '@/components/charts/GenericBarChart';

type MonthlyChart = {
  labels: string[];
  data: number[];
};

export default function MonthlyRevenueChart({ data }: { data: MonthlyChart }) {
  const chartData = data.labels.map((label, index) => ({
    month: label,
    revenue: data.data[index] || 0,
  }));

  return (
    <GenericBarChart
      data={chartData}
      xKey="month"
      bars={[
        {
          key: 'revenue',
          label: 'Doanh thu',
          color: '#4f46e5',
        },
      ]}
      yTickFormatter={(v) => `${(v / 1_000_000).toFixed(0)}M`}
      tooltipFormatter={(v) => (typeof v === 'number' ? `${v.toLocaleString()} VND` : '0 VND')}
    />
  );
}
