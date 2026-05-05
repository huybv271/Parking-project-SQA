'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Button } from './ui/button';

export interface SidebarItem {
  href: string;
  label: string;
  icon?: string;
}

export interface SidebarProps {
  menu: SidebarItem[];
  user?: any;
  onLogout?: () => void;
}

export default function Sidebar({ menu, user, onLogout }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="flex w-64 flex-col border-r bg-white">
      <div className="px-6 py-6 text-xl font-bold">
        <span className="text-indigo-600">LICHT</span>-PARKING
      </div>

      <nav className="flex-1 space-y-1 px-4">
        {menu.map((item) => {
          const active =
            pathname === item.href ||
            pathname.startsWith(item.href + '/') ||
            // highlight Reservation khi đang ở confirm
            (item.href === '/customer/reservation' && pathname === '/customer/confirm');

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-4 py-2 text-sm font-medium transition-all',
                active ? 'bg-indigo-600 text-white shadow' : 'text-gray-700 hover:bg-gray-100'
              )}
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t bg-gray-50 px-4 py-6">
        <p className="text-sm text-gray-700">Welcome back,</p>
        <p className="font-medium">{user?.name ?? 'Guest'}</p>
      </div>

      {onLogout && (
        <Button variant="destructive" className="w-full" onClick={onLogout}>
          🚪 Đăng xuất
        </Button>
      )}
    </aside>
  );
}
