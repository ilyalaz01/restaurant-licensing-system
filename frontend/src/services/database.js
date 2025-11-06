// Firebase Realtime Database operations
import { 
  ref, 
  set, 
  get, 
  push, 
  update, 
  remove,
  onValue,
  off,
  query,
  orderByChild,
  limitToLast,
  equalTo
} from 'firebase/database';
import { database, DB_PATHS, generateId } from './config';

class DatabaseService {
  // ============= BUSINESSES =============
  
  /**
   * Save business details to database
   */
  async saveBusiness(businessData) {
    try {
      const businessId = generateId();
      const businessRef = ref(database, `${DB_PATHS.BUSINESSES}/${businessId}`);
      
      const dataToSave = {
        ...businessData,
        id: businessId,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        status: 'active'
      };
      
      await set(businessRef, dataToSave);
      return { success: true, businessId, data: dataToSave };
    } catch (error) {
      console.error('Error saving business:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get business by ID
   */
  async getBusiness(businessId) {
    try {
      const businessRef = ref(database, `${DB_PATHS.BUSINESSES}/${businessId}`);
      const snapshot = await get(businessRef);
      
      if (snapshot.exists()) {
        return { success: true, data: snapshot.val() };
      } else {
        return { success: false, error: 'Business not found' };
      }
    } catch (error) {
      console.error('Error getting business:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Update business details
   */
  async updateBusiness(businessId, updates) {
    try {
      const businessRef = ref(database, `${DB_PATHS.BUSINESSES}/${businessId}`);
      
      const dataToUpdate = {
        ...updates,
        updatedAt: Date.now()
      };
      
      await update(businessRef, dataToUpdate);
      return { success: true, businessId };
    } catch (error) {
      console.error('Error updating business:', error);
      return { success: false, error: error.message };
    }
  }

  // ============= REPORTS =============
  
  /**
   * Save generated report
   */
  async saveReport(reportData, businessId) {
    try {
      const reportId = generateId();
      const reportRef = ref(database, `${DB_PATHS.REPORTS}/${reportId}`);
      
      const dataToSave = {
        ...reportData,
        id: reportId,
        businessId,
        generatedAt: Date.now(),
        version: '1.0',
        aiGenerated: true
      };
      
      await set(reportRef, dataToSave);
      
      // Also update business with latest report ID
      await this.updateBusiness(businessId, { latestReportId: reportId });
      
      return { success: true, reportId, data: dataToSave };
    } catch (error) {
      console.error('Error saving report:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get report by ID
   */
  async getReport(reportId) {
    try {
      const reportRef = ref(database, `${DB_PATHS.REPORTS}/${reportId}`);
      const snapshot = await get(reportRef);
      
      if (snapshot.exists()) {
        return { success: true, data: snapshot.val() };
      } else {
        return { success: false, error: 'Report not found' };
      }
    } catch (error) {
      console.error('Error getting report:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get all reports for a business
   */
  async getBusinessReports(businessId) {
    try {
      const reportsRef = ref(database, DB_PATHS.REPORTS);
      const reportsQuery = query(reportsRef, orderByChild('businessId'), equalTo(businessId));
      const snapshot = await get(reportsQuery);
      
      if (snapshot.exists()) {
        const reports = [];
        snapshot.forEach((childSnapshot) => {
          reports.push(childSnapshot.val());
        });
        return { success: true, data: reports };
      } else {
        return { success: true, data: [] };
      }
    } catch (error) {
      console.error('Error getting business reports:', error);
      return { success: false, error: error.message };
    }
  }

  // ============= REGULATIONS =============
  
  /**
   * Save regulations data (admin function)
   */
  async saveRegulations(regulationsData) {
    try {
      const regulationsRef = ref(database, DB_PATHS.REGULATIONS);
      await set(regulationsRef, regulationsData);
      return { success: true };
    } catch (error) {
      console.error('Error saving regulations:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get all regulations
   */
  async getRegulations() {
    try {
      const regulationsRef = ref(database, DB_PATHS.REGULATIONS);
      const snapshot = await get(regulationsRef);
      
      if (snapshot.exists()) {
        return { success: true, data: snapshot.val() };
      } else {
        // Return default regulations if none exist
        return { success: true, data: this.getDefaultRegulations() };
      }
    } catch (error) {
      console.error('Error getting regulations:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get default regulations (fallback)
   */
  getDefaultRegulations() {
    return {
      categories: {
        general_definitions: {
          name: "General Definitions",
          description: "Basic terms and requirements"
        },
        cross_sectional: {
          name: "Cross-Sectional Conditions",
          description: "Conditions that apply to all businesses"
        }
      },
      items: []
    };
  }

  // ============= ANALYTICS =============
  
  /**
   * Track analytics event
   */
  async trackEvent(eventType, eventData = {}) {
    try {
      const analyticsRef = ref(database, `${DB_PATHS.ANALYTICS}/events`);
      const newEventRef = push(analyticsRef);
      
      await set(newEventRef, {
        type: eventType,
        data: eventData,
        timestamp: Date.now(),
        userAgent: navigator.userAgent,
        screenSize: `${window.innerWidth}x${window.innerHeight}`
      });
      
      return { success: true };
    } catch (error) {
      console.error('Error tracking event:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Update daily statistics
   */
  async updateDailyStats(statType) {
    try {
      const today = new Date().toISOString().split('T')[0];
      const statsRef = ref(database, `${DB_PATHS.ANALYTICS}/daily/${today}/${statType}`);
      
      const snapshot = await get(statsRef);
      const currentValue = snapshot.exists() ? snapshot.val() : 0;
      
      await set(statsRef, currentValue + 1);
      return { success: true };
    } catch (error) {
      console.error('Error updating stats:', error);
      return { success: false, error: error.message };
    }
  }

  // ============= REAL-TIME LISTENERS =============
  
  /**
   * Listen to report updates
   */
  listenToReport(reportId, callback) {
    const reportRef = ref(database, `${DB_PATHS.REPORTS}/${reportId}`);
    
    const unsubscribe = onValue(reportRef, (snapshot) => {
      if (snapshot.exists()) {
        callback(snapshot.val());
      }
    });
    
    return unsubscribe;
  }

  /**
   * Listen to business updates
   */
  listenToBusiness(businessId, callback) {
    const businessRef = ref(database, `${DB_PATHS.BUSINESSES}/${businessId}`);
    
    const unsubscribe = onValue(businessRef, (snapshot) => {
      if (snapshot.exists()) {
        callback(snapshot.val());
      }
    });
    
    return unsubscribe;
  }
}

// Export singleton instance
export const dbService = new DatabaseService();
export default dbService;
