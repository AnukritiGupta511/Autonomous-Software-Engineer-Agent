import { GitBranch, Plus, Search, ExternalLink, RefreshCw, FolderGit2 } from 'lucide-react';

export default function RepositoriesPage() {
  const mockRepos = [
    {
      id: 1,
      name: 'autonomous-ai-agent',
      owner: 'developer',
      branch: 'main',
      tech: ['Python', 'TypeScript', 'Docker'],
      status: 'indexed',
      lastSync: '2 hours ago'
    },
    {
      id: 2,
      name: 'ecommerce-platform-microservices',
      owner: 'developer',
      branch: 'develop',
      tech: ['Java', 'Spring Boot', 'React'],
      status: 'indexing',
      lastSync: 'Just now'
    },
    {
      id: 3,
      name: 'marketing-site-nextjs',
      owner: 'acme-corp',
      branch: 'main',
      tech: ['Next.js', 'Tailwind CSS'],
      status: 'indexed',
      lastSync: '3 days ago'
    }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-2 tracking-tight flex items-center gap-3">
            <FolderGit2 className="text-[var(--color-primary)]" size={32} />
            Repositories
          </h1>
          <p className="text-[var(--color-text-secondary)]">Manage your connected codebases for AI analysis.</p>
        </div>
        
        <button className="px-5 py-2.5 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] rounded-xl font-medium shadow-lg hover:shadow-[var(--color-primary)]/25 transition-all flex items-center gap-2">
          <Plus size={18} />
          <span>Connect Repository</span>
        </button>
      </div>

      <div className="relative max-w-md">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search size={18} className="text-[var(--color-text-secondary)]" />
        </div>
        <input 
          type="text" 
          placeholder="Search repositories..." 
          className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-[var(--color-primary)] transition-colors text-white placeholder-[var(--color-text-secondary)]"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {mockRepos.map((repo) => (
          <div key={repo.id} className="glass-card p-6 rounded-2xl flex flex-col justify-between group hover:border-[var(--color-primary)]/30 transition-all">
            <div>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-[var(--color-surface-hover)] rounded-lg text-[var(--color-text-secondary)]">
                    <GitBranch size={20} />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg leading-tight truncate w-48" title={repo.name}>{repo.name}</h3>
                    <p className="text-sm text-[var(--color-text-secondary)]">{repo.owner}</p>
                  </div>
                </div>
                <a href="#" className="text-[var(--color-text-secondary)] hover:text-white transition-colors">
                  <ExternalLink size={18} />
                </a>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-6">
                {repo.tech.map((t, i) => (
                  <span key={i} className="text-xs px-2.5 py-1 bg-[var(--color-surface-hover)] border border-[var(--color-border)] rounded-md text-[var(--color-text-secondary)]">
                    {t}
                  </span>
                ))}
              </div>
            </div>
            
            <div className="flex items-center justify-between pt-4 border-t border-[var(--color-border)]">
              <div className="flex items-center gap-2">
                {repo.status === 'indexing' ? (
                  <RefreshCw size={14} className="text-[var(--color-warning)] animate-spin" />
                ) : (
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)]" />
                )}
                <span className="text-sm text-[var(--color-text-secondary)] capitalize">{repo.status}</span>
              </div>
              <span className="text-xs text-[var(--color-text-secondary)]">{repo.lastSync}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
