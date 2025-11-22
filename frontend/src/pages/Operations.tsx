import { useState, useEffect } from 'react';
import { Package, ArrowRightLeft, TruckIcon, AlertCircle, Plus } from 'lucide-react';
import axios from 'axios';
import OperationModal from '../components/OperationModal';
import { updateTransactionStatus } from '../api';

const API_BASE = 'http://localhost:8000';

interface Transaction {
  id: number;
  product_name: string;
  warehouse_name: string;
  transaction_type: string;
  quantity: number;
  reference: string;
  notes: string | null;
  status: string;
  timestamp: string;
}

const Operations = () => {
  const [activeTab, setActiveTab] = useState<'receipt' | 'delivery' | 'transfer' | 'adjustment'>('receipt');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  const operationTypes = [
    { id: 'receipt', label: 'Receipts', icon: Package, color: 'bg-green-100 text-green-600' },
    { id: 'delivery', label: 'Deliveries', icon: TruckIcon, color: 'bg-blue-100 text-blue-600' },
    { id: 'transfer', label: 'Transfers', icon: ArrowRightLeft, color: 'bg-purple-100 text-purple-600' },
    { id: 'adjustment', label: 'Adjustments', icon: AlertCircle, color: 'bg-red-100 text-red-600' },
  ];

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/operations/recent/`);
      setTransactions(response.data);
    } catch (err) {
      console.error('Error fetching transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOperationSuccess = () => {
    fetchTransactions();
  };

  const getFilteredTransactions = () => {
    return transactions.filter((t) => {
      if (activeTab === 'receipt') return t.transaction_type === 'receipt';
      if (activeTab === 'delivery') return t.transaction_type === 'delivery';
      if (activeTab === 'transfer') return t.transaction_type === 'transfer_in' || t.transaction_type === 'transfer_out';
      if (activeTab === 'adjustment') return t.transaction_type === 'adjustment';
      return false;
    });
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const getQuantityDisplay = (quantity: number, type: string) => {
    const sign = quantity > 0 ? '+' : '';
    let colorClass = 'text-gray-600';
    
    if (type === 'receipt' || type === 'transfer_in') colorClass = 'text-green-600';
    else if (type === 'delivery' || type === 'transfer_out') colorClass = 'text-blue-600';
    else if (type === 'adjustment') colorClass = quantity > 0 ? 'text-green-600' : 'text-red-600';
    
    return <span className={`${colorClass} font-semibold`}>{sign}{quantity} units</span>;
  };

  const getStatusBadge = (status: string, type: string) => {
    // For transfers and adjustments, show static badges
    if (type === 'transfer_in' || type === 'transfer_out') 
      return <span className="px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded">Completed</span>;
    if (type === 'adjustment') 
      return <span className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded">Adjusted</span>;
    
    // For receipts and deliveries, show current status
    const statusColors: Record<string, string> = {
      'ORDER_PLACED': 'bg-yellow-100 text-yellow-700',
      'IN_TRANSIT': 'bg-blue-100 text-blue-700',
      'COMPLETED': 'bg-green-100 text-green-700',
      'ORDER_RECEIVED': 'bg-yellow-100 text-yellow-700',
      'SHIPPING': 'bg-blue-100 text-blue-700',
      'SHIPPED': 'bg-green-100 text-green-700',
    };
    
    const colorClass = statusColors[status] || 'bg-gray-100 text-gray-700';
    const displayText = status.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
    
    return <span className={`px-2 py-1 text-xs ${colorClass} rounded`}>{displayText}</span>;
  };

  const handleStatusChange = async (transactionId: number, newStatus: string) => {
    try {
      await updateTransactionStatus(transactionId, newStatus);
      // Refresh the transactions list
      await fetchTransactions();
      // Show success message
      const transaction = transactions.find(t => t.id === transactionId);
      if (transaction) {
        alert(`Status updated to ${newStatus.replace(/_/g, ' ')}`);
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to update status');
    }
  };

  const renderStatusControl = (transaction: Transaction) => {
    const { transaction_type, status, id } = transaction;
    
    // Only show dropdowns for receipts and deliveries
    if (transaction_type === 'receipt') {
      return (
        <select
          value={status}
          onChange={(e) => handleStatusChange(id, e.target.value)}
          className="px-2 py-1 text-xs border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        >
          <option value="ORDER_PLACED">Order Placed</option>
          <option value="IN_TRANSIT">In Transit</option>
          <option value="COMPLETED">Completed</option>
        </select>
      );
    } else if (transaction_type === 'delivery') {
      return (
        <select
          value={status}
          onChange={(e) => handleStatusChange(id, e.target.value)}
          className="px-2 py-1 text-xs border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        >
          <option value="ORDER_RECEIVED">Order Received</option>
          <option value="SHIPPING">Shipping</option>
          <option value="SHIPPED">Shipped</option>
        </select>
      );
    }
    
    // For other types, show static badge
    return getStatusBadge(status, transaction_type);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Operations</h2>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center hover:bg-blue-700"
        >
          <Plus className="w-5 h-5 mr-2" />
          New Operation
        </button>
      </div>

      {/* Operation Type Tabs */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {operationTypes.map((type) => {
          const Icon = type.icon;
          return (
            <button
              key={type.id}
              onClick={() => setActiveTab(type.id as any)}
              className={`p-4 rounded-lg border-2 transition-all ${
                activeTab === type.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-center mb-2">
                <div className={`p-3 rounded-full ${type.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
              <div className="text-center font-semibold text-gray-700">{type.label}</div>
            </button>
          );
        })}
      </div>

      {/* Active Tab Content */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 capitalize">
          {activeTab} Operations
        </h3>
        
        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading operations...</div>
        ) : getFilteredTransactions().length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No {activeTab} operations found. Create one using the "New Operation" button!
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Product</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Warehouse</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Quantity</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Reference</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {getFilteredTransactions().map((transaction) => (
                  <tr key={transaction.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-600">{formatDate(transaction.timestamp)}</td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{transaction.product_name}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{transaction.warehouse_name}</td>
                    <td className="px-4 py-3 text-sm">{getQuantityDisplay(transaction.quantity, transaction.transaction_type)}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{transaction.reference}</td>
                    <td className="px-4 py-3">{renderStatusControl(transaction)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Operation Modal */}
      <OperationModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSuccess={handleOperationSuccess}
      />
    </div>
  );
};

export default Operations;
