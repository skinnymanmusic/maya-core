'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout/AppLayout';
import { Shield, AlertTriangle, Activity, CheckCircle } from 'lucide-react';
import { omegaClient } from '@/lib/api/omega-client';

interface AgentStatus {
  name: string;
  status: 'online' | 'offline' | 'error';
  lastActive: string;
}

export default function DashboardPage() {
  const [agents, setAgents] = useState<AgentStatus[]>([
    { name: 'Maya Sinclair', status: 'online', lastActive: '2 minutes ago' },
    { name: 'Solin MCP', status: 'online', lastActive: 'Just now' },
    { name: 'Sentra Safety', status: 'online', lastActive: '1 minute ago' },
    { name: 'Vita Repair', status: 'online', lastActive: '30 seconds ago' },
  ]);

  const [safeMode, setSafeMode] = useState(false);
  const [stats, setStats] = useState({
    pendingBookings: 0,
    paymentsDue: 0,
    emailsProcessed: 0,
    calendarBlocks: 0,
  });

  // Load stats from backend
  useEffect(() => {
    async function loadStats() {
      try {
        // Try to get stats from backend
        const health = await omegaClient.get('/api/health');
        if (health && health.safe_mode) {
          setSafeMode(true);
        }
        
        // Try to get bookings count
        try {
          const bookings = await omegaClient.get('/api/bookings');
          if (Array.isArray(bookings)) {
            setStats(prev => ({
              ...prev,
              pendingBookings: bookings.filter((b: any) => b.payment_status === 'pending').length,
              paymentsDue: bookings.filter((b: any) => b.payment_status === 'pending').length,
            }));
          }
        } catch (e) {
          // Ignore if bookings endpoint fails
        }
      } catch (error) {
        console.error('Failed to load stats:', error);
      }
    }

    loadStats();
    const interval = setInterval(loadStats, 30000); // Update every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">System overview and status</p>
        </div>

        {/* Safe Mode Alert */}
        {safeMode && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-6 h-6 text-red-500" />
              <div>
                <h3 className="font-semibold text-red-900">Safe Mode Active</h3>
                <p className="text-red-700 text-sm">
                  System operations are paused. Guardian Framework detected an issue.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="Pending Bookings"
            value={stats.pendingBookings}
            icon={Activity}
            color="blue"
          />
          <StatCard
            title="Payments Due"
            value={stats.paymentsDue}
            icon={AlertTriangle}
            color="yellow"
          />
          <StatCard
            title="Emails Processed"
            value={stats.emailsProcessed}
            icon={CheckCircle}
            color="green"
          />
          <StatCard
            title="Calendar Blocks"
            value={stats.calendarBlocks}
            icon={Activity}
            color="purple"
          />
        </div>

        {/* Agent Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Agent Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <div className={`
                    w-3 h-3 rounded-full
                    ${agent.status === 'online' ? 'bg-green-500' : 'bg-gray-400'}
                  `} />
                  <div>
                    <p className="font-medium">{agent.name}</p>
                    <p className="text-sm text-gray-500">{agent.lastActive}</p>
                  </div>
                </div>
                <span className={`
                  px-3 py-1 rounded-full text-xs font-medium min-h-[32px] min-w-[80px] flex items-center justify-center
                  ${agent.status === 'online' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-gray-100 text-gray-800'
                  }
                `}>
                  {agent.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <ActivityItem
              action="Email processed"
              details="Maya responded to John Smith"
              time="2 minutes ago"
            />
            <ActivityItem
              action="Payment received"
              details="$500 deposit from Sarah Johnson"
              time="15 minutes ago"
            />
            <ActivityItem
              action="Calendar blocked"
              details="Wedding - December 15, 2025"
              time="1 hour ago"
            />
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

function StatCard({ title, value, icon: Icon, color }: any) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colors[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}

function ActivityItem({ action, details, time }: any) {
  return (
    <div className="flex items-start gap-3 p-3 border-l-2 border-gray-200 hover:border-yellow-400 transition-colors">
      <div className="flex-1">
        <p className="font-medium">{action}</p>
        <p className="text-sm text-gray-600">{details}</p>
      </div>
      <span className="text-xs text-gray-500">{time}</span>
    </div>
  );
}


