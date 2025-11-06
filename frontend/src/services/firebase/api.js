/**
 * API Service - Connects frontend to backend
 * Backend: https://restaurant-licensing-system-tz3z.vercel.app
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://restaurant-licensing-system-tz3z.vercel.app';

class ApiService {
  /**
   * Submit questionnaire to backend
   */
  async submitQuestionnaire(businessData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/questionnaire/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          business_details: businessData,
          submission_timestamp: new Date().toISOString(),
          session_id: this.getSessionId(),
          user_agent: navigator.userAgent
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting questionnaire:', error);
      throw error;
    }
  }

  /**
   * Get report by ID
   */
  async getReport(reportId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/report/${reportId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching report:', error);
      throw error;
    }
  }

  /**
   * Get regulations data
   */
  async getRegulations() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/regulations`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching regulations:', error);
      throw error;
    }
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }

  /**
   * Get or create session ID
   */
  getSessionId() {
    let sessionId = sessionStorage.getItem('session_id');
    if (!sessionId) {
      sessionId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      sessionStorage.setItem('session_id', sessionId);
    }
    return sessionId;
  }
}

export const apiService = new ApiService();
export default apiService;
