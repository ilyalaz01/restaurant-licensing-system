import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiService from '../services/api';

const Report = () => {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReport();
  }, [reportId]);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const response = await apiService.getReport(reportId);
      
      if (response.success) {
        setReport(response.report);
      } else {
        throw new Error('Report not found');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleStartNew = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-700">Generating your report...</p>
          <p className="text-sm text-gray-500 mt-2">AI is analyzing your business requirements</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Report</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={handleStartNew}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Start New Assessment
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-xl text-gray-700">Report not found</p>
      </div>
    );
  }

  const getPriorityColor = (priority) => {
    const colors = {
      critical: 'bg-red-100 text-red-800 border-red-300',
      high: 'bg-orange-100 text-orange-800 border-orange-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-green-100 text-green-800 border-green-300',
    };
    return colors[priority] || colors.low;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header Actions */}
        <div className="mb-6 flex justify-between items-center print:hidden">
          <button
            onClick={handleStartNew}
            className="px-4 py-2 text-blue-600 hover:text-blue-800 font-medium"
          >
            ← New Assessment
          </button>
          <button
            onClick={handlePrint}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            🖨️ Print Report
          </button>
        </div>

        {/* Report Container */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Report Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8">
            <h1 className="text-3xl font-bold mb-2">Restaurant Licensing Assessment Report</h1>
            <p className="text-blue-100">
              Generated on {new Date().toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>

          {/* Business Information */}
          {report.business && (
            <div className="p-8 border-b">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Business Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Business Name</p>
                  <p className="font-semibold text-gray-900">{report.business.business_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Owner</p>
                  <p className="font-semibold text-gray-900">{report.business.owner_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Size</p>
                  <p className="font-semibold text-gray-900">{report.business.size_sqm} sqm</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Seating Capacity</p>
                  <p className="font-semibold text-gray-900">{report.business.seating_capacity} seats</p>
                </div>
                {report.business.features && report.business.features.length > 0 && (
                  <div className="md:col-span-2">
                    <p className="text-sm text-gray-600 mb-2">Features</p>
                    <div className="flex flex-wrap gap-2">
                      {report.business.features.map((feature, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                        >
                          {feature.replace('_', ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* AI Summary */}
          {report.summary && (
            <div className="p-8 border-b bg-blue-50">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">🤖 AI Analysis Summary</h2>
              <div className="prose max-w-none text-gray-700">
                <p className="text-lg leading-relaxed whitespace-pre-wrap">{report.summary}</p>
              </div>
            </div>
          )}

          {/* Matched Regulations */}
          {report.matched_regulations && report.matched_regulations.length > 0 && (
            <div className="p-8 border-b">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">📋 Applicable Regulations</h2>
              <div className="space-y-4">
                {report.matched_regulations.map((regulation, index) => (
                  <div
                    key={index}
                    className={`border-2 rounded-lg p-5 ${getPriorityColor(regulation.priority)}`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-bold text-lg">{regulation.title || regulation.name}</h3>
                      <span className="px-3 py-1 rounded-full text-xs font-bold uppercase">
                        {regulation.priority || 'Medium'}
                      </span>
                    </div>
                    
                    {regulation.description && (
                      <p className="text-sm mb-3">{regulation.description}</p>
                    )}

                    {regulation.requirements && regulation.requirements.length > 0 && (
                      <div className="mt-3">
                        <p className="font-semibold text-sm mb-2">Requirements:</p>
                        <ul className="list-disc list-inside space-y-1 text-sm">
                          {regulation.requirements.map((req, idx) => (
                            <li key={idx}>{req}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {regulation.authority && (
                      <p className="mt-3 text-xs font-semibold">
                        Authority: {regulation.authority}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Required Documents */}
          {report.required_documents && report.required_documents.length > 0 && (
            <div className="p-8 border-b">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">📄 Required Documents</h2>
              <ul className="space-y-2">
                {report.required_documents.map((doc, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span className="text-gray-700">{doc}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Next Steps */}
          {report.next_steps && report.next_steps.length > 0 && (
            <div className="p-8 border-b">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">🎯 Next Steps</h2>
              <ol className="space-y-3">
                {report.next_steps.map((step, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold mr-3">
                      {index + 1}
                    </span>
                    <span className="text-gray-700 pt-1">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* Important Notes */}
          <div className="p-8 bg-yellow-50">
            <h2 className="text-xl font-bold text-gray-900 mb-3">⚠️ Important Notes</h2>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>• This report is AI-generated and should be verified with official authorities</li>
              <li>• Regulations may change - always check for the most current requirements</li>
              <li>• Additional conditions may apply based on your specific location</li>
              <li>• Consult with a certified professional before submitting applications</li>
            </ul>
          </div>

          {/* Footer */}
          <div className="p-6 bg-gray-100 text-center text-sm text-gray-600">
            <p>Report ID: {reportId}</p>
            <p className="mt-1">Restaurant Licensing Assessment System - AI-Powered</p>
          </div>
        </div>

        {/* Print Hidden Actions */}
        <div className="mt-6 text-center print:hidden">
          <button
            onClick={handleStartNew}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Start New Assessment
          </button>
        </div>
      </div>
    </div>
  );
};

export default Report;
