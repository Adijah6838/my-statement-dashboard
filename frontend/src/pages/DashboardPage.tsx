import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getBalance, getStatements } from '../api/dashboard';
import type { Statement, BalanceResponse } from '../api/dashboard';

export default function DashboardPage() {
  const { logout } = useAuth();
  
  const [data, setData] = useState<BalanceResponse | null>(null);
  const [statements, setStatements] = useState<Statement[]>([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(5);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [hideBalance, setHideBalance] = useState(() => {
    return localStorage.getItem('hideBalance') === 'true';
  });

  const toggleBalance = () => {
    const newValue = !hideBalance;
    setHideBalance(newValue);
    localStorage.setItem('hideBalance', String(newValue));
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [balanceData, statementsData] = await Promise.all([
          getBalance(),
          getStatements(skip, limit)
        ]);
        setData(balanceData);
        setStatements(statementsData.items);
        setTotal(statementsData.total);
      } catch (err: any) {
        console.error("Dashboard Error:", err);
        const detail = err.response?.data?.detail || err.message || 'Unknown Network Error';
        const status = err.response?.status || 'No Status';
        setError(`Failed to load: ${detail} (Status: ${status})`);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [skip, limit]);

  if (loading && !data) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        
        <header className="flex justify-between items-center bg-white p-6 rounded-lg shadow-sm">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">My Statement</h1>
            <p className="text-gray-500">Welcome back, {data?.full_name}</p>
          </div>
          <button
            onClick={logout}
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 transition-colors"
          >
            Logout
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-600">Current Balance</h2>
              <button 
                onClick={toggleBalance}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                {hideBalance ? '👁️ Show' : '🙈 Hide'}
              </button>
            </div>
            <p className="text-4xl font-bold text-gray-900">
              {hideBalance ? '••••••' : `$${data?.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold text-gray-600 mb-4">Total Transactions</h2>
            <p className="text-4xl font-bold text-gray-900">{total}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800">Recent Statements</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 text-gray-600 text-sm uppercase tracking-wider">
                  <th className="p-4 font-medium">Description</th>
                  <th className="p-4 font-medium">Date</th>
                  <th className="p-4 font-medium">Type</th>
                  <th className="p-4 font-medium text-right">Amount</th>
                  <th className="p-4 font-medium text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {statements.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="p-8 text-center text-gray-500">No statements found.</td>
                  </tr>
                ) : (
                  statements.map((stmt) => (
                    <tr key={stmt.id} className="hover:bg-gray-50 transition-colors">
                      <td className="p-4 text-gray-800">{stmt.description}</td>
                      <td className="p-4 text-gray-600">{new Date(stmt.date).toLocaleDateString()}</td>
                      <td className="p-4"><span className="capitalize text-gray-600">{stmt.transaction_type}</span></td>
                      <td className={`p-4 text-right font-medium ${
                        stmt.transaction_type === 'withdrawal' || (stmt.transaction_type === 'transfer' && stmt.sender_name) 
                        ? 'text-red-600' : 'text-green-600'
                      }`}>
                        {stmt.transaction_type === 'withdrawal' ? '-' : '+'}${stmt.amount.toFixed(2)}
                      </td>
                      <td className="p-4 text-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 capitalize">
                          {stmt.status}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <div className="p-4 border-t border-gray-200 flex items-center justify-between bg-gray-50">
            <span className="text-sm text-gray-600">
              Showing {statements.length > 0 ? skip + 1 : 0} to {Math.min(skip + limit, total)} of {total} records
            </span>
            <div className="flex space-x-2">
              <button
                onClick={() => setSkip(Math.max(0, skip - limit))}
                disabled={skip === 0}
                className="px-4 py-2 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={() => setSkip(skip + limit)}
                disabled={skip + limit >= total}
                className="px-4 py-2 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
