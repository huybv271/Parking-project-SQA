'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';

type BarConfig = {
  key: string;
  label: string;
  color: string;
};

interface GenericBarChartProps {
  data: any[];
  xKey: string;
  bars: BarConfig[];
  yTickFormatter?: (v: number) => string;
  tooltipFormatter?: (value: any) => string;
}

export function GenericBarChart({
  data,
  xKey,
  bars,
  yTickFormatter,
  tooltipFormatter,
}: GenericBarChartProps) {
  return (
    <div className="h-[360px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} />
          <YAxis tickFormatter={yTickFormatter} />
          <Tooltip formatter={tooltipFormatter} />
          <Legend />

          {bars.map((bar) => (
            <Bar
              key={bar.key}
              dataKey={bar.key}
              name={bar.label}
              fill={bar.color}
              radius={[6, 6, 0, 0]}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
