class ConsciousCommuteAPI {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
  }

  async fetchSyllabi() {
    try {
      const response = await fetch(`${this.baseUrl}/api/syllabi`);
      if (!response.ok) {
        throw new Error("Failed to fetch syllabi subjects.");
      }
      return await response.json();
    } catch (e) {
      console.error("API Error (fetchSyllabi):", e);
      return [];
    }
  }

  async generateStudyPlan(source, destination, subject, isPeak = false, module = "any module") {
    try {
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source,
          destination,
          subject,
          is_peak: isPeak,
          module: module
        })
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate study plan.");
      }
      
      return data;
    } catch (e) {
      console.error("API Error (generateStudyPlan):", e);
      throw e;
    }
  }

  async getModules(subject) {
    try {
      const response = await fetch(`${this.baseUrl}/api/modules?subject=${encodeURIComponent(subject)}`);
      if (!response.ok) {
        throw new Error("Failed to fetch modules.");
      }
      return await response.json();
    } catch (e) {
      console.error("API Error (getModules):", e);
      return [];
    }
  }
}
