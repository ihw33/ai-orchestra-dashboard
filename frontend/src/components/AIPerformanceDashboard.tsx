import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Activity, AlertCircle, CheckCircle, Clock, Cpu, HardDrive } from 'lucide-react';

interface SessionMetrics {
  agent: string;
  status: 'idle' | 'working' | 'thinking' | 'error';
  currentTask: string | null;
  tasksCompleted: number;
  averageTime: number;
  successRate: number;
  lastActivity: Date;
  cpuUsage: number;
  memoryUsage: number;
}

interface Notification {
  id: string;
  type: 'task_stuck' | 'high_error_rate' | 'slow_response' | 'task_completed';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  timestamp: Date;
}

export const AIPerformanceDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<SessionMetrics[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // WebSocket 연결
    const websocket = new WebSocket('ws://localhost:8001/ws/metrics');
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'metrics') {
        setMetrics(data.payload);
      } else if (data.type === 'notification') {
        setNotifications(prev => [data.payload, ...prev].slice(0, 10));
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'idle': return 'bg-gray-500';
      case 'working': return 'bg-blue-500';
      case 'thinking': return 'bg-yellow-500';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'info': return 'text-blue-600';
      case 'warning': return 'text-yellow-600';
      case 'critical': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* AI 에이전트 상태 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric) => (
          <Card key={metric.agent} className="relative">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-center">
                <CardTitle className="text-lg">{metric.agent}</CardTitle>
                <Badge className={getStatusColor(metric.status)}>
                  {metric.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {/* 현재 작업 */}
              {metric.currentTask && (
                <div className="text-sm">
                  <span className="text-gray-500">Current Task:</span>
                  <p className="font-medium truncate">{metric.currentTask}</p>
                </div>
              )}

              {/* 성능 지표 */}
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-gray-500">Completed:</span>
                  <p className="font-bold">{metric.tasksCompleted}</p>
                </div>
                <div>
                  <span className="text-gray-500">Avg Time:</span>
                  <p className="font-bold">{Math.round(metric.averageTime)}s</p>
                </div>
              </div>

              {/* 성공률 */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-500">Success Rate</span>
                  <span className="font-medium">{metric.successRate}%</span>
                </div>
                <Progress value={metric.successRate} className="h-2" />
              </div>

              {/* 리소스 사용량 */}
              <div className="grid grid-cols-2 gap-2">
                <div className="flex items-center gap-1 text-sm">
                  <Cpu className="w-4 h-4 text-gray-500" />
                  <span>{metric.cpuUsage}%</span>
                </div>
                <div className="flex items-center gap-1 text-sm">
                  <HardDrive className="w-4 h-4 text-gray-500" />
                  <span>{metric.memoryUsage}%</span>
                </div>
              </div>

              {/* 마지막 활동 */}
              <div className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="w-3 h-3" />
                <span>
                  Last active: {new Date(metric.lastActivity).toLocaleTimeString()}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 실시간 알림 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Real-time Notifications
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {notifications.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No notifications yet</p>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className="flex items-start gap-2 p-3 bg-gray-50 rounded-lg"
                >
                  {notification.severity === 'critical' ? (
                    <AlertCircle className="w-5 h-5 text-red-500 mt-0.5" />
                  ) : notification.type === 'task_completed' ? (
                    <CheckCircle className="w-5 h-5 text-green-500 mt-0.5" />
                  ) : (
                    <Activity className="w-5 h-5 text-blue-500 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p className={`text-sm ${getSeverityColor(notification.severity)}`}>
                      {notification.message}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(notification.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIPerformanceDashboard;