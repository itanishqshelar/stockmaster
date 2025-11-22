import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Package } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

interface Transaction {
  id: number;
  product_name: string;
  warehouse_name: string;
  transaction_type: string;
  quantity: number;
  reference: string;
  status: string;
  timestamp: string;
}

interface Product {
  id: number;
  name: string;
  quantity: number;
}

const Dashboard = () => {
  const [recentActivity, setRecentActivity] = useState<Transaction[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    // Poll for updates every 5 seconds
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [activityRes, productsRes] = await Promise.all([
        axios.get(`${API_BASE}/operations/recent/?limit=10`),
        axios.get(`${API_BASE}/products/`)
      ]);
      setRecentActivity(activityRes.data);
      setProducts(productsRes.data);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const totalProducts = products.length;
  const lowStockItems = products.filter(p => p.quantity < 10).length;
  const pendingReceipts = recentActivity.filter(
    t => t.transaction_type === 'receipt' && t.status !== 'COMPLETED'
  ).length;
  const pendingDeliveries = recentActivity.filter(
    t => t.transaction_type === 'delivery' && t.status !== 'SHIPPED'
  ).length;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'receipt': return '📦';
      case 'delivery': return '🚚';
      case 'transfer_in':
      case 'transfer_out': return '🔄';
      case 'adjustment': return '⚠️';
      default: return '📋';
    }
  };

  const getStatusBadge = (status: string) => {
    const statusConfig: Record<string, { color: string; text: string }> = {
      'ORDER_PLACED': { color: 'bg-yellow-100 text-yellow-700', text: 'Order Placed' },
      'IN_TRANSIT': { color: 'bg-blue-100 text-blue-700', text: 'In Transit' },
      'COMPLETED': { color: 'bg-green-100 text-green-700', text: 'Completed' },
      'ORDER_RECEIVED': { color: 'bg-yellow-100 text-yellow-700', text: 'Order Received' },
      'SHIPPING': { color: 'bg-blue-100 text-blue-700', text: 'Shipping' },
      'SHIPPED': { color: 'bg-green-100 text-green-700', text: 'Shipped' },
      'DONE': { color: 'bg-green-100 text-green-700', text: 'Done' },
    };

    const config = statusConfig[status] || { color: 'bg-gray-100 text-gray-700', text: status };
    return (
      <span className={`px-2 py-1 text-xs ${config.color} rounded font-medium`}>
        {config.text}
      </span>
    );
  };

  const getActivityDescription = (transaction: Transaction) => {
    const qty = Math.abs(transaction.quantity);
    switch (transaction.transaction_type) {
      case 'receipt':
        return `Received ${qty} units of ${transaction.product_name}`;
      case 'delivery':
        return `Delivered ${qty} units of ${transaction.product_name}`;
      case 'transfer_in':
        return `Transferred ${qty} units of ${transaction.product_name} to ${transaction.warehouse_name}`;
      case 'transfer_out':
        return `Transferred ${qty} units of ${transaction.product_name} from ${transaction.warehouse_name}`;
      case 'adjustment':
        return `Adjusted ${transaction.product_name} quantity`;
      default:
        return transaction.reference;
    }
  };

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h2>
      
      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Products</p>
              <p className="text-2xl font-bold text-gray-800">{totalProducts}</p>
            </div>
            <div className="p-3 bg-blue-50 rounded-full text-blue-600">
              <Package className="w-6 h-6" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Low Stock Items</p>
              <p className="text-2xl font-bold text-red-600">{lowStockItems}</p>
            </div>
            <div className="p-3 bg-red-50 rounded-full text-red-600">
              <AlertTriangle className="w-6 h-6" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Pending Receipts</p>
              <p className="text-2xl font-bold text-green-600">{pendingReceipts}</p>
            </div>
            <div className="p-3 bg-green-50 rounded-full text-green-600">
              <TrendingUp className="w-6 h-6" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Pending Deliveries</p>
              <p className="text-2xl font-bold text-orange-600">{pendingDeliveries}</p>
            </div>
            <div className="p-3 bg-orange-50 rounded-full text-orange-600">
              <TrendingDown className="w-6 h-6" />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h3>
        {loading ? (
          <div className="text-gray-500 text-center py-8">Loading...</div>
        ) : recentActivity.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No recent activity to show.
          </div>
        ) : (
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-start gap-4 p-4 hover:bg-gray-50 rounded-lg transition-colors">
                <div className="text-2xl">{getActivityIcon(activity.transaction_type)}</div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">
                    {getActivityDescription(activity)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {activity.warehouse_name} • {formatDate(activity.timestamp)}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  {getStatusBadge(activity.status)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
