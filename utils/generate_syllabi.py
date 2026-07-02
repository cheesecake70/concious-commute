from reportlab.pdfgen import canvas
import os

def create_pdf(filename, title, modules):
    path = os.path.join("data", "syllabi", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, title)
    
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, "Mumbai University Course Syllabus")
    c.drawString(50, 715, "-" * 80)
    
    y = 680
    for mod_title, topics in modules.items():
        if y < 100:
            c.showPage()
            y = 750
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, mod_title)
        y -= 20
        
        for topic in topics:
            if y < 100:
                c.showPage()
                y = 750
            c.setFont("Helvetica", 10)
            c.drawString(70, y, f"- {topic}")
            y -= 15
        y -= 10
        
    c.save()
    print(f"Created syllabus PDF: {path}")

# Define syllabus modules/chapters for the 6 new courses
syllabi_data = {
    "corporate_finance.pdf": (
        "Corporate Finance",
        {
            "Module 1: Introduction to Corporate Finance": [
                "Definition, scope, and objectives of Corporate Finance",
                "Profit Maximization vs. Wealth Maximization goals",
                "Risk-Return Tradeoff and agency problems in financial management"
            ],
            "Module 2: Time Value of Money": [
                "Concepts of future value, present value, and annuities",
                "Compounding and discounting techniques",
                "Applications to bond and stock valuation"
            ],
            "Module 3: Capital Budgeting Decisions": [
                "Capital budgeting process and significance",
                "Non-Discounting methods: Payback Period, Accounting Rate of Return",
                "Discounting methods: Net Present Value (NPV), Internal Rate of Return (IRR), Profitability Index"
            ],
            "Module 4: Cost of Capital & WACC": [
                "Computation of cost of individual components: equity, debt, preference shares",
                "Weighted Average Cost of Capital (WACC) and marginal cost of capital",
                "Capital structure determinants and theories"
            ],
            "Module 5: Working Capital Management": [
                "Operating cycle and cash cycle concepts",
                "Estimating working capital requirements",
                "Management of Cash, Receivables, Payables, and Inventory"
            ],
            "Module 6: Dividend Policy and Decisions": [
                "Determinants of dividend payouts",
                "Walter's model, Gordon's model, and Miller-Modigliani (MM) hypothesis",
                "Types of dividends: cash dividend, stock dividend (bonus shares)"
            ]
        }
    ),
    "financial_accounting.pdf": (
        "Financial Accounting",
        {
            "Module 1: Accounting Principles and Bookkeeping": [
                "Generally Accepted Accounting Principles (GAAP) and Accounting Standards",
                "Double-Entry bookkeeping system, journalizing, and posting to ledger",
                "Trial Balance preparation and rectification of accounting errors"
            ],
            "Module 2: Preparation of Financial Statements": [
                "Trading Account and Profit and Loss Account preparation",
                "Balance Sheet formulation with standard adjusting entries",
                "Treatment of depreciation, outstanding expenses, and closing stock"
            ],
            "Module 3: Depreciation and Inventory Valuation": [
                "Depreciation methods: Straight Line Method (SLM) and Written Down Value (WDV)",
                "Inventory valuation models: FIFO, LIFO, and Weighted Average Cost (WAC)",
                "Impact of valuation methods on financial performance"
            ],
            "Module 4: Partnership Accounts": [
                "Partnership deed, profit sharing ratios, and capital accounts",
                "Accounting for admission, retirement, and death of partners",
                "Dissolution of partnership firms and piecemeal distribution"
            ],
            "Module 5: Company Accounts": [
                "Issue of equity shares, share application, allotment, and calls",
                "Forfeiture and reissue of shares",
                "Issue and redemption of preference shares and debentures"
            ],
            "Module 6: Financial Statement Ratio Analysis": [
                "Liquidity ratios: Current Ratio, Quick Ratio",
                "Profitability ratios: Gross Profit Ratio, Net Profit Ratio, ROCE",
                "Solvency and activity ratios, Cash Flow Statement basics"
            ]
        }
    ),
    "marketing_management.pdf": (
        "Marketing Management",
        {
            "Module 1: Introduction to Marketing & 4Ps": [
                "Core marketing concepts, needs, wants, demands, and transactions",
                "Marketing vs. Selling philosophies",
                "The 4 Ps of the Marketing Mix: Product, Price, Place, Promotion"
            ],
            "Module 2: Consumer Buying Behavior": [
                "Factors influencing consumer behavior: cultural, social, personal, psychological",
                "Consumer buying decision process steps",
                "Types of buying decision behavior"
            ],
            "Module 3: Market Segmentation, Targeting & Positioning (STP)": [
                "Bases for segmenting consumer and business markets",
                "Evaluation and selection of target market segments",
                "Developing and communicating a positioning strategy"
            ],
            "Module 4: Product Life Cycle and Pricing Strategies": [
                "Product classifications and Product Mix decisions",
                "Product Life Cycle (PLC) stages and marketing strategies",
                "Pricing objectives and pricing methods: cost-based, value-based, competition-based"
            ],
            "Module 5: Distribution Channels and Promotion": [
                "Role of distribution channels, direct vs. indirect marketing channels",
                "Retailing, wholesaling, and physical logistics management",
                "Integrated Marketing Communications (IMC): advertising, personal selling, sales promotion, PR"
            ],
            "Module 6: Digital & Social Media Marketing": [
                "E-commerce marketing, SEO, and search engine marketing (SEM)",
                "Social media platforms and content marketing strategies",
                "Mobile marketing, analytics, and ethical issues in digital marketing"
            ]
        }
    ),
    "human_resource_management.pdf": (
        "Human Resource Management",
        {
            "Module 1: HRM Foundations and Strategic HRM": [
                "HRM definition, functions, scope, and objectives",
                "Difference between Personnel Management and HRM",
                "Strategic HRM and the role of HR in business strategy"
            ],
            "Module 2: HR Planning and Job Analysis": [
                "Human Resource Planning (HRP) process and forecasting",
                "Job Analysis: Job Description (JD) and Job Specification (JS)",
                "Job design, enlargement, enrichment, and rotation"
            ],
            "Module 3: Recruitment, Selection & Induction": [
                "Internal and external sources of recruitment",
                "Selection process, types of interviews, and tests",
                "Induction, orientation, and social integration of new employees"
            ],
            "Module 4: Training & Management Development": [
                "Identifying training needs (TNA)",
                "On-the-job and off-the-job training methods",
                "Evaluating training effectiveness, management development programs"
            ],
            "Module 5: Performance Appraisal & Compensation Planning": [
                "Performance appraisal objectives and traditional vs. modern methods (MBO, 360-degree)",
                "Appraisal bias and performance feedback",
                "Job evaluation, wage structures, fringe benefits, and incentive systems"
            ],
            "Module 6: Industrial Relations & Employee Welfare": [
                "Industrial dispute causes, prevention, and settlement machinery",
                "Trade unions role, collective bargaining process",
                "Employee safety, health, and welfare statutory provisions"
            ]
        }
    ),
    "macroeconomics.pdf": (
        "Macroeconomics",
        {
            "Module 1: National Income Accounting": [
                "Key macroeconomic variables: GDP, GNP, NDP, NNP",
                "Methods of measuring National Income: Product, Income, Expenditure",
                "Circular flow of income in two, three, and four sector models"
            ],
            "Module 2: Keynesian Demand Side Economics": [
                "Classical vs. Keynesian views of employment and output",
                "Consumption function, savings function, and marginal propensity to consume (MPC)",
                "Investment multiplier concept and aggregate demand determination"
            ],
            "Module 3: Money Supply, Banking & Monetary Policy": [
                "Functions of money and measures of money supply (M1, M2, M3, M4)",
                "Credit creation by commercial banks",
                "Central Bank functions, monetary policy instruments: CRR, SLR, Repo Rate, Open Market Operations"
            ],
            "Module 4: Public Finance and Fiscal Policy": [
                "Public finance scope, public expenditure principles",
                "Taxation types: direct vs. indirect taxes, GST framework",
                "Fiscal Policy objectives, government deficit types, and public debt"
            ],
            "Module 5: Business Cycles and Economic Growth": [
                "Phases of business cycles: expansion, peak, contraction, trough",
                "Causes and consequences of inflation and unemployment",
                "Economic growth vs. economic development, Harrod-Domar growth model"
            ],
            "Module 6: International Trade and Balance of Payments": [
                "Theories of international trade: Absolute and Comparative Advantage",
                "Balance of Payments (BOP) structure: Current Account and Capital Account",
                "Exchange rate determination: fixed, floating, and managed floats"
            ]
        }
    ),
    "business_law.pdf": (
        "Business Law",
        {
            "Module 1: Indian Contract Act 1872": [
                "Essential elements of a valid contract, proposal, and acceptance",
                "Capacity to contract, free consent, and consideration",
                "Void agreements, breach of contract, and remedies for breach"
            ],
            "Module 2: Indemnity, Guarantee, Pledge & Agency": [
                "Contracts of Indemnity and Guarantee, rights of surety",
                "Bailment and Pledge definition and duties of parties",
                "Agency creation, ratification, termination, and agent authority"
            ],
            "Module 3: Sale of Goods Act 1930": [
                "Contract of sale, sale vs. agreement to sell",
                "Conditions and Warranties, transfer of ownership (passing of property)",
                "Rights of an unpaid seller against goods and the buyer"
            ],
            "Module 4: Negotiable Instruments Act 1881": [
                "Definition and characteristics of Promissory Notes, Bills of Exchange, and Cheques",
                "Negotiation, endorsement, and holder in due course",
                "Dishonour of cheques due to insufficiency of funds (Section 138)"
            ],
            "Module 5: Companies Act 2013": [
                "Definition, characteristics, and classification of companies",
                "Company incorporation process, Memorandum (MoA) and Articles (AoA)",
                "Prospectus, shares, directors appointment, and board meetings"
            ],
            "Module 6: Consumer Protection Act 2019": [
                "Definition of consumer, consumer rights, and unfair trade practices",
                "Consumer Dispute Redressal Commissions (District, State, National)",
                "Mediation process, product liability, and offenses/penalties"
            ]
        }
    )
}

if __name__ == "__main__":
    for filename, (title, modules) in syllabi_data.items():
        create_pdf(filename, title, modules)
