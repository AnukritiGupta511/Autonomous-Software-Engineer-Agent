import { Activity, Play, CheckCircle2, XCircle, Clock, ArrowRight } from 'lucide-react';

export default function WorkflowsPage() {
  const mockWorkflows = [
    {
      id: 'wf-1',
      name: 'Refactor Authentication Module',
      agent: 'Code Refactorer',
      status: 'running',
      progress: 65,
      timeElapsed: '14m 20s',
      repo: 'ecommerce-platform'
    },
    {
      id: 'wf-2',
      name: 'Analyze Architecture & Generate Docs',
      agent: 'Repo Analyzer',
      status: 'completed',
      progress: 100,
      timeElapsed: '3m 45s',
      repo: 'autonomous-ai-agent'
    },
    {
      id: 'wf-3',
      name: 'Fix memory leak in background worker',
      agent: 'Bug Fixer',
      status: 'failed',
      progress: 42,
      timeElapsed: '8m 10s',
      repo: 'marketing-site-nextjs'
    }
  ];

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'running': return <Activity size={18} className="text-[var(--color-accent)] animate-pulse" />;
      case 'completed': return <CheckCircle2 size={18} className="text-[var(--color-success)]" />;
      case 'failed': return <XCircle size={18} className="text-[var(--color-error)]" />;
      default: return <Clock size={18} className="text-[var(--color-text-secondary)]" />;
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-2 tracking-tight flex items-center gap-3">
            <Activity className="text-[var(--color-accent)]" size={32} />
            Agent Workflows
          </h1>
          <p className="text-[var(--color-text-secondary)]">Monitor and manage autonomous AI tasks.</p>
        </div>
        
        <button className="px-5 py-2.5 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] rounded-xl font-medium shadow-lg hover:shadow-[var(--color-primary)]/25 transition-all flex items-center gap-2">
          <Play size={18} fill="currentColor" />
          <span>New Workflow</span>
        </button>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden">
        <div className="grid grid-cols-12 gap-4 p-4 border-b border-[var(--color-border)] text-sm font-medium text-[var(--color-text-secondary)] uppercase tracking-wider">
          <div className="col-span-4">Workflow</div>
          <div className="col-span-2">Agent Type</div>
          <div className="col-span-2">Repository</div>
          <div className="col-span-3">Progress</div>
          <div className="col-span-1 text-right">Action</div>
        </div>

        <div className="divide-y divide-[var(--color-border)]">
          {mockWorkflows.map((workflow) => (
            <div key={workflow.id} className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-[var(--color-surface-hover)] transition-colors group cursor-pointer">
              
              {/* Name & Status */}
              <div className="col-span-4 flex items-center gap-3">
                <div className={`p-2 rounded-lg bg-[var(--color-surface)] border border-[var(--color-border)]`}>
                  {getStatusIcon(workflow.status)}
                </div>
                <div>
                  <h3 className="font-semibold text-white truncate w-full">{workflow.name}</h3>
                  <p className="text-xs text-[var(--color-text-secondary)]">{workflow.timeElapsed}</p>
                </div>
              </div>

              {/* Agent */}
              <div className="col-span-2">
                <span className="text-sm px-2.5 py-1 rounded-md bg-[var(--color-primary)]/10 text-[var(--color-primary-100)] border border-[var(--color-primary)]/20 inline-block">
                  {workflow.agent}
                </span>
              </div>

              {/* Repository */}
              <div className="col-span-2">
                <span className="text-sm text-[var(--color-text-secondary)] truncate block">
                  {workflow.repo}
                </span>
              </div>

              {/* Progress */}
              <div className="col-span-3 pr-4">
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="capitalize text-[var(--color-text-secondary)]">{workflow.status}</span>
                  <span className="font-mono text-[var(--color-text-secondary)]">{workflow.progress}%</span>
                </div>
                <div className="h-1.5 w-full bg-[var(--color-surface)] rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${workflow.status === 'failed' ? 'bg-[var(--color-error)]' : workflow.status === 'completed' ? 'bg-[var(--color-success)]' : 'bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)]'}`} 
                    style={{ width: `${workflow.progress}%` }}
                  />
                </div>
              </div>

              {/* Actions */}
              <div className="col-span-1 flex justify-end">
                <button className="text-[var(--color-text-secondary)] hover:text-white transition-colors opacity-0 group-hover:opacity-100">
                  <ArrowRight size={20} />
                </button>
              </div>

            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
