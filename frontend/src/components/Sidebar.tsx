import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, GitBranch, MessageSquare, Activity, LogOut } from 'lucide-react';

export default function Sidebar() {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Repositories', path: '/repos', icon: GitBranch },
    { name: 'AI Chat', path: '/chat', icon: MessageSquare },
    { name: 'Workflows', path: '/workflows', icon: Activity },
  ];

  return (
    <div className="w-64 h-screen bg-[var(--color-surface)] border-r border-[var(--color-border)] flex flex-col fixed left-0 top-0">
      
      {/* Header */}
      <div className="p-6 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center">
          <span className="text-sm font-bold text-white">🤖</span>
        </div>
        <span className="font-bold text-lg text-white">Agent Engineer</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path || 
                          (item.path !== '/' && location.pathname.startsWith(item.path));
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive 
                  ? 'bg-gradient-to-r from-[var(--color-primary)]/20 to-transparent text-[var(--color-accent)] border-l-2 border-[var(--color-primary)]' 
                  : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-hover)] hover:text-white'
              }`}
            >
              <item.icon size={20} className={isActive ? 'text-[var(--color-accent)]' : ''} />
              <span className="font-medium text-sm">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer / User Profile */}
      <div className="p-4 border-t border-[var(--color-border)]">
        <div className="flex items-center gap-3 px-2 py-2 rounded-xl hover:bg-[var(--color-surface-hover)] cursor-pointer transition-colors text-[var(--color-text-secondary)] hover:text-white">
          <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
            <span className="text-xs font-bold text-white">JD</span>
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="text-sm font-medium truncate text-white">John Doe</p>
            <p className="text-xs truncate">john@example.com</p>
          </div>
          <LogOut size={16} />
        </div>
      </div>
    </div>
  );
}
