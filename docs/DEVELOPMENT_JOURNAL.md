# 📔 DEVELOPMENT JOURNAL

## Restaurant Licensing Assessment System

---

## PROJECT TIMELINE

**Total Development Time:** 3 days  
**Date:** November 2024  
**Development Approach:** AI-assisted development with Claude

---

## CHALLENGES ENCOUNTERED & SOLUTIONS

### **Challenge 1: Understanding the Domain**

**Context:**  
When I started this project, I had no prior experience with business licensing or Israeli regulatory law. The project requirement was to build a system about something serious and professional - business licensing requirements in Israel.

**The Problem:**
- Initial unfamiliarity with licensing terminology
- Difficulty understanding which regulations apply to which businesses
- Confusion about priority levels and dependencies
- Legal language was complex and domain-specific

**How I Solved It:**
1. Read through the licensing PDF document multiple times
2. Looked through the pdf document of Israeli licensing 
3. Used AI (Claude) to explain complex regulations in simple terms
4. Gradually built understanding while implementing the matching logic
5. Realized that threshold-based logic (size >50 sqm) makes more sense than abstract categories

**Time Spent:** First day - approximately 4-5 hours of reading , understanding , and creating API keys + project skeleton

**Key Insight:**  
Taking time to understand the domain deeply before coding saves debugging time later. Don't rush into implementation without understanding the business requirements.

---

### **Challenge 2: Data Extraction from PDF**

**Context:**  
The project required converting a 60-page Hebrew licensing PDF into structured JSON format.

**The Problem:**
I initially tried using Python PDF extraction libraries:

```python
# Attempted approaches:
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader

# Problems encountered:
# 1. Hebrew text came out reversed (RTL language issues)
# 2. Section numbers were mixed up (4.1 appeared before 2.1, 6 after 7)
# 3. Tables were extracted as messy strings
# 4. Formatting was completely lost
```

**After Hours of Struggle:**
- Tried multiple PDF libraries
- Attempted text preprocessing to fix Hebrew direction
- Tried regex patterns to extract structured data
- Nothing worked reliably

**The Solution:**
Instead of fighting with PDF extraction, I used Google Gemini Pro:

1. Uploaded the PDF directly to Gemini Pro
2. Asked it to convert to structured JSON with specific format
3. Manually verified the accuracy of 30 regulations
4. Refined the structure to work with matching_engine.py

**Prompt Used:**
```
Convert this Israeli restaurant licensing document to JSON.
Extract regulations with: ID, title (Hebrew & English), 
requirements, costs, timelines, and applicable conditions.
Preserve Hebrew formatting and section order.
```

**Result:**  
Clean, accurate JSON in 20 minutes vs. hours of failed PDF parsing.

**Time Saved:** ~6-8 hours

**Lesson Learned:**  
Sometimes the "smart" solution (AI) is better than the "technical" solution (writing complex parsing code). Use the right tool for the job.

---

### **Challenge 3: Initial Development Confusion & Deployment Hurdles**

**Context:**  
As I built the system, my understanding of the requirements evolved daily. What started as a simple matching tool became a complex estimation and deployment challenge.

**The Problem:**
- Started coding the frontend before fully understanding the backend matching logic.
- Had to rewrite the matching engine multiple times as complexity became clear.
- Feature Creep: Initially wanted to add everything, but was unclear what was truly essential versus "nice-to-have."
- Data Underestimation: I wasn't using the rich data (cost/time) already present in the JSON files.
- Deployment Failures: The backend failed to deploy on Vercel, blocking any real-world testing.

**Evolution of Understanding:**

**Day 1 Initial Build & First Reversal:**  
"I need to build a licensing system... let me start coding the questionnaire." 
→ Built a basic frontend questionnaire without a clear plan for how the matching logic would work. 
→ "Wait, how do regulations actually match to businesses?" 
→ Quickly refactored the system to use simple, hard-coded category matching (e.g., "Small", "Medium", "Large"). This was the first major reversal.
→ (Evening - Deployment Wall): "The logic is finally working locally, but the backend won't deploy on Vercel." 
→ Began debugging a wall of failures: module import errors, path resolution issues, and CORS problems. 
→ After numerous failed redeploys, Vercel restricted my account for exceeding the daily deployment limit. 
→ This problem continued, forcing me to stop and analyze official documentation (which led to the fix by adjusting vercel.json and the ASGI entry point).

**Day 2:**  
"I woke up and realized the category matching from Day 1 was still completely wrong." 
→ (Morning - Logic Refactor): Rewrote the matching engine again to use specific numerical thresholds (e.g., sqm > 50, seats > 300). 
→ (Mid-day - Logic Refactor 2): Realized I needed AND/OR logic for rules like Sprinklers (needs AND) and Fire Detection (needs AND). Refactored the engine and JSON structure to support this. 
→ (Afternoon - Data Refactor): Realized the hard-coded "2-4 month" timeline was useless. 
→ I completely refactored the service to: 1. Sum Costs: Read the estimated_cost (e.g., "5,000-15,000 ILS") from every matched regulation to calculate a total cost range.
→ 2. Tier Timelines: Base the total timeline on complexity (e.g., needing sprinklers = "8-12 months"), not a simple guess.

**Lesson Learned:**  
It's okay not to understand everything at the start. Build iteratively, and don't be afraid to refactor when you learn something new. Document your decisions.

---

### **Challenge 4: The Tedious Work of Manually Auditing AI-Generated Content**

**Context:**  
The project was large, with many files and countless small fixes that were changed multiple times. This made it difficult to track all the details.

**The Problem:**
- The AI couldn't grasp all the specific nuances or the history of why certain small things were repeatedly fixed.
- This meant the AI-generated documentation was just a first draft, often missing the subtleties. I could not publish what it wrote directly.
- The real work was the time-consuming and tedious process of manually reading every single page the AI generated.


**How I Managed It: My workflow became a 3-step loop:**
1. I wrote a detailed prompt explaining what I wanted.
2. The AI generated a draft.
3. I had to manually edit and rewrite the AI's output to correct the nuances and ensure it was accurate.

**Note:**
AI is a tool for drafting, not for finishing. The most tedious part is the necessary manual review to ensure all nuances are correct, which takes significant time.


## LESSONS LEARNED

### **Technical Lessons**

**Use AI Smartly**
AI is incredible for:
- Generating boilerplate code quickly
- Explaining complex concepts
- Debugging when you're stuck
- Refactoring based on new understanding

AI is NOT a replacement for:
- Reading documentation
- Understanding business logic
- Testing your code
- Domain knowledge

**Iterate Based on Understanding**
Don't be afraid to rewrite code when you understand requirements better. Keep old versions for reference (not_in_use/ folder).

### **Process Lessons**

**1. Don't Be Lazy with Requirements**
Time spent understanding requirements deeply saves debugging time later. I should have spent more time analyzing the licensing PDF before coding.

**2. Take Your Time**
Rushing leads to mistakes. Taking a step back to understand the full picture prevents costly rewrites.

**3. Document Decisions**
Keep notes on why you made certain choices. Future you will be grateful. I forgot why I structured some files certain ways.

### **Personal Lessons**

**1. Patience with Yourself**
After not programming for a couple of months, I was rusty. That's normal. Don't get discouraged - skills come back quickly.

**2. Documentation Is Important**
Writing this development journal helped me process what I learned. Future projects will benefit from these insights.

**3. Balance Speed and Quality**
AI makes development fast - but you still need to think carefully about architecture and business logic. Speed without thought leads to bugs.

---

## FUTURE IMPROVEMENTS

### **Features to Add**

**1. Dark Mode**
Simple UI enhancement for better user experience.

**2. Email/SMS Notifications**
- Save user email and phone number
- Email PDF report to user
- SMS summary to phone number
- Reminder system for upcoming deadlines

**3. Progress Tracking**
- Let users save their compliance progress
- Check off completed requirements
- See percentage complete
- Set reminders for pending items

**4. Multi-language Reports**
- Arabic support (large Arabic-speaking population in Israel)
- Russian support (significant Russian-speaking community)
- Auto-detect user language preference

**5. Document Upload**
- Users upload existing licenses
- AI analyzes and identifies gaps
- Suggests what's missing

**6. Professional Directory**
- List of certified professionals (architects, engineers, lawyers)
- Connect users with service providers
- Review system

### **Technical Improvements**

**1. Caching Layer**
- Redis for frequent queries
- Reduce AI API calls
- Faster response times

**2. Analytics Dashboard**
- Track common business types
- See most triggered regulations
- Usage statistics

**3. API Rate Limiting**
- Prevent abuse
- Fair usage policies
- Premium tiers

**4. Mobile App**
- Native iOS/Android apps
- Offline report viewing
- Push notifications

---

## STATISTICS

### **Development Time Breakdown**

| Phase | Time Spent | Percentage |
|-------|-----------|------------|
| Understanding Requirements | 3 hours | 13% |
| Data Extraction Attempts | 2 hours | 8% |
| Backend Development | 3 hours | 13% |
| Frontend Development | 2 hours | 8% |
| Vercel Debugging | 6 hours | 26% |
| Testing & Fixes | 3 hours | 13% |
| Development Journal | 4 hours | 17% |

**Total:** ~23 hours over 3 days

### **Code Statistics**

- **Total Lines:** ~3,500
- **AI-Generated:** 85%
- **Manual Edits:** 15%
- **Components:** 3 (Home, Questionnaire, Report)
- **Backend Services:** 3 (Matching, Gemini, Firebase)
- **Regulations:** 30
- **Test Coverage:** 100% (core logic)

### **Learning Metrics**

- **Documentation Pages Read:** 50+
- **AI Conversations:** 100+
- **Bugs Fixed:** 20+
- **Refactors:** 3 major rewrites
- **"Aha!" Moments:** 5

---

## REFLECTION

### **What This Project Taught Me**

**About Development:**
- AI accelerates but doesn't replace thinking
- Documentation reading is essential


**About Myself:**
- I can pick up skills again after breaks
- I enjoy projects that solve real problems

**About the Process:**
- Requirements understanding > rushing to code
- Clean architecture saves debugging time
- Taking breaks helps solve problems

### **Was It Worth It?**

**Absolutely.** 


## FINAL THOUGHTS

This project was challenging, frustrating at times, but ultimately rewarding. After a couple of months away from programming, it felt good to build something meaningful from scratch.

The combination of AI tools and traditional development skills created something useful. The system works, it's deployed, it helps real businesses, and I learned valuable lessons along the way.

Most importantly: **Read the documentation.** Seriously. Just read it.

---

**Project Status:** Complete  
**Deployment:** Live on Vercel  
**Documentation:** Complete  
**Learning:** Significant

**Would Build Again:** 10/10 ✅