import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';

const Questionnaire = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    business_name: '',
    owner_name: '',
    email: '',
    phone: '',
    size_sqm: '',
    seating_capacity: '',
    features: [],
    location_city: '',
    planned_opening_date: '',
    existing_business: false,
    previous_license: false,
  });

  const totalSteps = 5;

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleFeatureToggle = (feature) => {
    setFormData(prev => ({
      ...prev,
      features: prev.features.includes(feature)
        ? prev.features.filter(f => f !== feature)
        : [...prev.features, feature]
    }));
  };

  const validateStep = (step) => {
    switch (step) {
      case 1:
        return formData.business_name.length >= 2 && formData.owner_name.length >= 2;
      case 2:
        return formData.size_sqm > 0 && formData.size_sqm <= 500 && 
               formData.seating_capacity >= 0 && formData.seating_capacity <= 500;
      case 3:
        return true; // Features are optional
      case 4:
        return true; // Additional info is optional
      case 5:
        return true; // Review step
      default:
        return false;
    }
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, totalSteps));
      setError(null);
    } else {
      setError('Please fill in all required fields correctly');
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
    setError(null);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Convert string numbers to actual numbers
      const submissionData = {
        ...formData,
        size_sqm: parseFloat(formData.size_sqm),
        seating_capacity: parseInt(formData.seating_capacity),
      };

      const response = await apiService.submitQuestionnaire(submissionData);
      
      if (response.success) {
        // Navigate to report page with report ID
        navigate(`/report/${response.report_id}`);
      } else {
        throw new Error(response.message || 'Submission failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to submit questionnaire. Please try again.');
      setIsSubmitting(false);
    }
  };

  const renderStepIndicator = () => (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        {[1, 2, 3, 4, 5].map((step) => (
          <div key={step} className="flex-1 flex items-center">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold
              ${currentStep >= step 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-600'}`}>
              {step}
            </div>
            {step < 5 && (
              <div className={`flex-1 h-1 mx-2
                ${currentStep > step ? 'bg-blue-600' : 'bg-gray-200'}`} />
            )}
          </div>
        ))}
      </div>
      <div className="mt-4 text-center">
        <span className="text-sm text-gray-600">
          Step {currentStep} of {totalSteps}: {getStepTitle(currentStep)}
        </span>
      </div>
    </div>
  );

  const getStepTitle = (step) => {
    const titles = {
      1: 'Basic Information',
      2: 'Size & Capacity',
      3: 'Business Features',
      4: 'Additional Details',
      5: 'Review & Submit'
    };
    return titles[step];
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Basic Information</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Business Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          name="business_name"
          value={formData.business_name}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., The Golden Fork Restaurant"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Owner Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          name="owner_name"
          value={formData.owner_name}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., John Doe"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Email
        </label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="owner@restaurant.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Phone Number
        </label>
        <input
          type="tel"
          name="phone"
          value={formData.phone}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="050-1234567"
        />
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Size & Capacity</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Business Size (Square Meters) <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          name="size_sqm"
          value={formData.size_sqm}
          onChange={handleInputChange}
          min="1"
          max="500"
          step="0.1"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., 80"
          required
        />
        <p className="mt-2 text-sm text-gray-500">
          Enter the total floor area accessible to customers (1-500 sqm)
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Seating Capacity <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          name="seating_capacity"
          value={formData.seating_capacity}
          onChange={handleInputChange}
          min="0"
          max="500"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., 40"
          required
        />
        <p className="mt-2 text-sm text-gray-500">
          Maximum number of people that can be seated (0-500)
        </p>
      </div>

      {formData.size_sqm && (
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Size Category:</strong> {
              formData.size_sqm <= 50 ? 'Small (≤50 sqm)' :
              formData.size_sqm <= 100 ? 'Medium (50-100 sqm)' :
              'Large (>100 sqm)'
            }
          </p>
        </div>
      )}

      {formData.seating_capacity && (
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="text-sm text-green-800">
            <strong>Seating Category:</strong> {
              formData.seating_capacity <= 20 ? 'Intimate (≤20 seats)' :
              formData.seating_capacity <= 50 ? 'Standard (20-50 seats)' :
              'Large (>50 seats)'
            }
          </p>
        </div>
      )}
    </div>
  );

  const renderStep3 = () => {
    const features = [
      { id: 'alcohol', label: 'Serving Alcoholic Beverages', icon: '🍷' },
      { id: 'delivery', label: 'Food Delivery Service', icon: '🚗' },
      { id: 'outdoor', label: 'Outdoor Seating Area', icon: '🌳' },
      { id: 'kitchen_gas', label: 'Kitchen Uses Gas', icon: '🔥' },
      { id: 'live_music', label: 'Live Music/Entertainment', icon: '🎵' },
    ];

    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Business Features</h2>
        <p className="text-gray-600 mb-6">
          Select all features that apply to your business. These affect which licenses you'll need.
        </p>
        
        <div className="space-y-3">
          {features.map((feature) => (
            <label
              key={feature.id}
              className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all
                ${formData.features.includes(feature.id)
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'}`}
            >
              <input
                type="checkbox"
                checked={formData.features.includes(feature.id)}
                onChange={() => handleFeatureToggle(feature.id)}
                className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              />
              <span className="ml-4 text-2xl">{feature.icon}</span>
              <span className="ml-3 text-gray-900 font-medium">{feature.label}</span>
            </label>
          ))}
        </div>

        {formData.features.length > 0 && (
          <div className="p-4 bg-yellow-50 rounded-lg">
            <p className="text-sm text-yellow-800">
              <strong>Selected Features:</strong> {formData.features.length} feature(s) selected.
              Additional regulations may apply.
            </p>
          </div>
        )}
      </div>
    );
  };

  const renderStep4 = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Additional Details</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Location (City)
        </label>
        <input
          type="text"
          name="location_city"
          value={formData.location_city}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., Tel Aviv"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Planned Opening Date
        </label>
        <input
          type="date"
          name="planned_opening_date"
          value={formData.planned_opening_date}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div className="space-y-4 pt-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            name="existing_business"
            checked={formData.existing_business}
            onChange={handleInputChange}
            className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
          />
          <span className="ml-3 text-gray-900">This is an existing business (not a new opening)</span>
        </label>

        <label className="flex items-center">
          <input
            type="checkbox"
            name="previous_license"
            checked={formData.previous_license}
            onChange={handleInputChange}
            className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
          />
          <span className="ml-3 text-gray-900">I have held a business license before</span>
        </label>
      </div>
    </div>
  );

  const renderStep5 = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Review Your Information</h2>
      
      <div className="bg-gray-50 rounded-lg p-6 space-y-4">
        <div>
          <h3 className="font-semibold text-gray-700 mb-2">Basic Information</h3>
          <p><strong>Business:</strong> {formData.business_name}</p>
          <p><strong>Owner:</strong> {formData.owner_name}</p>
          {formData.email && <p><strong>Email:</strong> {formData.email}</p>}
          {formData.phone && <p><strong>Phone:</strong> {formData.phone}</p>}
        </div>

        <div className="border-t pt-4">
          <h3 className="font-semibold text-gray-700 mb-2">Size & Capacity</h3>
          <p><strong>Size:</strong> {formData.size_sqm} sqm</p>
          <p><strong>Seating:</strong> {formData.seating_capacity} seats</p>
        </div>

        <div className="border-t pt-4">
          <h3 className="font-semibold text-gray-700 mb-2">Features</h3>
          {formData.features.length > 0 ? (
            <ul className="list-disc list-inside">
              {formData.features.map(f => (
                <li key={f} className="capitalize">{f.replace('_', ' ')}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No special features selected</p>
          )}
        </div>

        {(formData.location_city || formData.planned_opening_date) && (
          <div className="border-t pt-4">
            <h3 className="font-semibold text-gray-700 mb-2">Additional Details</h3>
            {formData.location_city && <p><strong>Location:</strong> {formData.location_city}</p>}
            {formData.planned_opening_date && <p><strong>Opening Date:</strong> {formData.planned_opening_date}</p>}
            {formData.existing_business && <p>✓ Existing business</p>}
            {formData.previous_license && <p>✓ Previous license holder</p>}
          </div>
        )}
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          By submitting this questionnaire, you confirm that the information provided is accurate.
          Our AI will generate a personalized licensing report based on your business details.
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {renderStepIndicator()}

          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}
          {currentStep === 4 && renderStep4()}
          {currentStep === 5 && renderStep5()}

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <div className="mt-8 flex justify-between">
            <button
              onClick={prevStep}
              disabled={currentStep === 1}
              className={`px-6 py-3 rounded-lg font-medium transition-colors
                ${currentStep === 1
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
            >
              ← Previous
            </button>

            {currentStep < totalSteps ? (
              <button
                onClick={nextStep}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Next →
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className={`px-8 py-3 rounded-lg font-medium transition-colors
                  ${isSubmitting
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700'} text-white`}
              >
                {isSubmitting ? 'Submitting...' : 'Submit & Generate Report'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Questionnaire;
