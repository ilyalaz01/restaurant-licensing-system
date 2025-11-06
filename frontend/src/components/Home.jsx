import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Restaurant Licensing Assessment System
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Get a personalized AI-powered report on the licensing requirements
            for your restaurant business in Israel
          </p>
          <button
            onClick={() => navigate('/questionnaire')}
            className="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
          >
            Start Assessment
            <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">📋</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Simple Questionnaire
            </h3>
            <p className="text-gray-600">
              Answer a few questions about your business size, capacity, and features
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              AI-Powered Analysis
            </h3>
            <p className="text-gray-600">
              Advanced AI processes regulations and generates a personalized report
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">✅</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Clear Action Plan
            </h3>
            <p className="text-gray-600">
              Get specific requirements, documents needed, and next steps
            </p>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-blue-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold text-lg mb-2">Fill Questionnaire</h3>
              <p className="text-gray-600 text-sm">Provide your business details</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold text-lg mb-2">AI Analysis</h3>
              <p className="text-gray-600 text-sm">System matches regulations</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold text-lg mb-2">Get Report</h3>
              <p className="text-gray-600 text-sm">Receive personalized report</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h3 className="font-semibold text-lg mb-2">Take Action</h3>
              <p className="text-gray-600 text-sm">Follow clear next steps</p>
            </div>
          </div>
        </div>
      </div>

      {/* What You'll Get */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          What You'll Get
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Applicable Regulations</h4>
              <p className="text-gray-600 text-sm">All regulations relevant to your specific business</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Required Documents</h4>
              <p className="text-gray-600 text-sm">Complete list of documents you need to prepare</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Priority Levels</h4>
              <p className="text-gray-600 text-sm">Know which requirements are critical vs optional</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Next Steps</h4>
              <p className="text-gray-600 text-sm">Clear action plan with step-by-step guidance</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">AI Insights</h4>
              <p className="text-gray-600 text-sm">Personalized analysis of your business situation</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="text-2xl mr-4">✓</div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Printable Report</h4>
              <p className="text-gray-600 text-sm">Download and print for your records</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 py-16">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Takes only 5 minutes to complete the assessment
          </p>
          <button
            onClick={() => navigate('/questionnaire')}
            className="inline-flex items-center px-8 py-4 bg-white text-blue-600 text-lg font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
          >
            Start Your Assessment Now
            <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm text-gray-400">
            Restaurant Licensing Assessment System - AI-Powered Regulatory Analysis
          </p>
          <p className="text-xs text-gray-500 mt-2">
            This tool provides guidance based on Israeli business licensing regulations
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
