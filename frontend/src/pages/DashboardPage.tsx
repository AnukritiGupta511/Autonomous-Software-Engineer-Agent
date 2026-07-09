import { Code2, GitBranch, MessageSquare, Activity, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const stats = [
    { label: 'Connected Repos', value: '4', icon: GitBranch, color: 'text-violet-500' },
    { label: 'Agent Workflows', value: '12', icon: Activity, color: 'text-cyan-500' },
    { label: 'Chat Sessions', value: '28', icon: MessageSquare, color: 'text-emerald-500' },
    { label: 'Lines Analyzed', value: '142k', icon: Code2, color: 'text-amber-500' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2 tracking-tight">Welcome back, Developer</h1>
        <p className="text-[var(--color-text-secondary)]">Here's what your AI Agents have been up to.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <div key={i} className="glass-card p-6 rounded-2xl relative overflow-hidden group cursor-pointer">
            <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] opacity-10 rounded-full blur-2xl group-hover:opacity-20 transition-opacity"></div>
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[var(--color-text-secondary)] text-sm font-medium mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-white tracking-tight">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-xl bg-white/5 ${stat.color}`}>
                <stat.icon size={24} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Recent Activity */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Recent Workflows</h2>
            <Link to="/workflows" className="text-sm text-[var(--color-accent)] hover:underline flex items-center gap-1">
              View all <ArrowRight size={14} />
            </Link>
          </div>
          
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-[var(--color-border)] hover:bg-[var(--color-surface-hover)] transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--color-success)] animate-pulse"></span>
                  <span className="font-semibold text-white">Feature Generation: Auth API</span>
                </div>
                <span className="text-xs text-[var(--color-text-secondary)]">2 mins ago</span>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)]">Agent generated 4 files and updated documentation.</p>
            </div>
            <div className="p-6 border-b border-[var(--color-border)] hover:bg-[var(--color-surface-hover)] transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--color-warning)] animate-pulse"></span>
                  <span className="font-semibold text-white">Code Review: PR #42</span>
                </div>
                <span className="text-xs text-[var(--color-text-secondary)]">Running...</span>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)]">Code Reviewer agent is analyzing complexity.</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          <h2 className="text-xl font-bold">Quick Actions</h2>
          <div className="space-y-4">
            <button className="w-full text-left p-4 rounded-xl border border-[var(--color-primary)]/30 bg-[var(--color-primary)]/10 hover:bg-[var(--color-primary)]/20 transition-all group relative overflow-hidden">
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-[var(--color-primary)]/0 via-[var(--color-primary)]/20 to-[var(--color-primary)]/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              <div className="flex items-center gap-3">
                <GitBranch className="text-[var(--color-primary)]" />
                <span className="font-medium text-[var(--color-primary-100)]">Connect Repository</span>
              </div>
            </button>
            
            <button className="w-full text-left p-4 rounded-xl border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/10 hover:bg-[var(--color-accent)]/20 transition-all">
              <div className="flex items-center gap-3">
                <MessageSquare className="text-[var(--color-accent)]" />
                <span className="font-medium">New AI Chat</span>
              </div>
            </button>
            
            <button className="w-full text-left p-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] hover:bg-[var(--color-surface-hover)] transition-all">
              <div className="flex items-center gap-3">
                <Activity className="text-[var(--color-text-secondary)]" />
                <span className="font-medium text-[var(--color-text-secondary)] group-hover:text-white transition-colors">Start Workflow</span>
              </div>
            </button>
          </div>
        </div>
        
      </div>
    </div>
  );
}
