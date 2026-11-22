# ReceiptWise: Verified Receipt-to-Expense Workflow

**Project Proposal**

| Project information | Details |
|---|---|
| Project name | ReceiptWise |
| Project type | AI-powered document processing and expense management |
| Project category | Software Engineering / Artificial Intelligence |
| Development duration | 8 weeks |
| Team size | 3 members |
| Repository | GitHub – ReceiptWise |
| Version | 0.1 – Initial Proposal |
| Status | Proposed |

## 1. Problem Statement

Organizations frequently process employee expenses using manually reviewed receipts. This process can be time-consuming and vulnerable to transcription errors, incorrect financial calculations, duplicate submissions and inconsistent approval decisions.

Receipt photographs contain important purchase information, including merchant names, dates, item descriptions, quantities, prices, taxes and totals. However, extracting this information accurately from photographed receipts can be challenging because of poor image quality, rotation, different layouts and language variations.

Furthermore, extracting information from a receipt does not establish whether an expense complies with an organization's internal policies. Expense approval requires additional business rules, authorization permissions and a controlled review process.

ReceiptWise proposes an integrated application that uses Optical Character Recognition (OCR), structured information extraction, deterministic financial validation and a simulated expense approval workflow to transform photographed receipts into verified expense records.

The project will evaluate document extraction separately from policy processing and compare machine-extracted records with human-corrected and verified records.

## 2. Project Objectives

The main objectives are to:

1. Develop an application that accepts photographed and scanned receipts.
2. Extract structured purchase information using OCR and document processing.
3. Identify merchants, dates, currencies, line items, quantities, prices, taxes and totals where available.
4. Preserve bounding-box provenance and extraction confidence for extracted fields.
5. Implement deterministic arithmetic, currency, duplicate and mandatory-field validation.
6. Provide a human correction and verification interface.
7. Develop an independently configurable fictional expense policy engine.
8. Implement a complete draft, review, correction, submission, approval and rejection workflow.
9. Provide search, reporting and CSV/JSON export functionality.
10. Evaluate extraction accuracy, policy enforcement, workflow integrity and human review effort.

## 3. Intended Users

ReceiptWise will support four user roles.

- **Employee:** Uploads receipts, verifies extracted information, corrects fields and submits expenses.
- **Reviewer:** Examines receipt information, adds comments and requests corrections.
- **Approver:** Approves or rejects eligible expenses according to assigned permissions.
- **Administrator:** Manages users, roles, expense categories, policy limits and reporting.

Backend authorization will ensure that users can only perform actions permitted by their assigned roles.

## 4. Functional Requirements

The application will provide the following capabilities.

### 4.1 Receipt Management

- Upload individual receipt images.
- Upload multiple receipts in batches.
- Validate file types, file sizes and image readability.
- Preserve original receipt images.
- Support draft expense records.
- Maintain receipt and expense ownership.

### 4.2 OCR and Information Extraction

- Extract receipt text using OCR.
- Identify merchants, purchase dates and currencies.
- Extract available line items, quantities and prices.
- Identify subtotal, tax, discounts and total amounts where labeled.
- Return structured JSON records.
- Preserve bounding-box coordinates for extracted values.
- Record confidence scores and extraction methods.
- Mark missing or uncertain values as unknown.

### 4.3 Financial Validation

- Check subtotal and line-item arithmetic.
- Validate totals, taxes and discounts where sufficient information exists.
- Validate currency formats.
- Detect duplicate receipts using image hashes and similarity checks.
- Identify missing mandatory information.
- Maintain separate validation results for extraction uncertainty and financial inconsistencies.

### 4.4 Human Review

- Display original receipt images alongside extracted fields.
- Highlight the source regions of extracted values.
- Allow reviewers to edit extracted fields.
- Preserve original and corrected values.
- Record reviewer identity and correction timestamps.
- Provide reviewer comments and correction history.

### 4.5 Expense Policy Management

Administrators will be able to configure fictional expense policies containing:

- Expense categories.
- Maximum spending limits.
- Required supporting evidence.
- Authorized approver roles.
- Exception and escalation rules.

Policy decisions will be deterministic and independent of AI prompts or LLM-generated recommendations.

### 4.6 Expense Approval Workflow

The application will implement:

Draft → Review → Correction → Submission → Approval or Rejection.

It will enforce permitted state transitions, role-based permissions, atomic status updates and immutable status history.

### 4.7 Reporting and Export

- Search expenses by merchant, category and date.
- Filter approved expenses.
- Export approved records to CSV and JSON.
- Generate printable expense review summaries.
- Maintain audit logs of important actions.

## 5. Non-Functional Requirements

### Security and Privacy
- Secure authentication and password hashing.
- Backend role-based access control.
- Restricted access to receipt images.
- Secure storage of configuration secrets.
- Protection against unauthorized approval attempts.

### Reliability
- Explicit handling of unreadable and low-quality images.
- Recoverable OCR and processing failures.
- Input validation and useful error messages.
- Database transactions for workflow changes.
- Preservation of original receipt images.

### Auditability
- Immutable original receipt storage.
- Source-coordinate provenance.
- Machine-extracted versus manually corrected value tracking.
- Timestamped reviewer actions.
- Immutable status and approval history.

### Performance and Cost
- Support CPU-based OCR or affordable external APIs.
- Avoid unnecessary GPU training.
- Measure processing time and resource consumption.
- Document API usage and cost assumptions.

### Maintainability
- Modular backend architecture.
- Automated component and integration tests.
- Version-controlled development.
- Reproducible local installation using Docker Compose.

## 6. Dataset and Licensing

The project will use the CORD v2 (Consolidated Receipt Dataset) hosted on Hugging Face.

Dataset URL:

https://huggingface.co/datasets/naver-clova-ix/cord-v2

Dataset characteristics:

- Total: 1,000 receipt examples.
- Training: 800 examples.
- Validation: 100 examples.
- Testing: 100 examples.
- Domain: Primarily Indonesian photographed receipts.
- License listed by the repository: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Approximate dataset size: 2.31 GB.

The dataset contains receipt images and structured annotations useful for OCR and post-OCR information extraction.

The public labels have limitations, including omitted store/payment information categories as identified in the project brief. Consequently, the project will not assume that every application field has corresponding ground-truth annotations.

The team will:

1. Review the dataset structure and annotations.
2. Preserve attribution to the original dataset creators.
3. Use the training split for development.
4. Use validation examples for development decisions.
5. Reserve the test split for final evaluation.
6. Avoid test-data leakage.
7. Avoid committing restricted or large dataset copies to GitHub.

Additional independently prepared synthetic receipts will be used for testing application-specific requirements not covered by CORD.

## 7. Proposed System Architecture

ReceiptWise will use a modular client-server architecture.
### Architecture Diagram

The proposed system architecture and data flow are documented in:

[ReceiptWise Architecture Diagram](diagrams/architecture.mmd)

### Technology Stack

| Component | Technology |
|---|---|
| Frontend | React and TypeScript |
| Backend | Python and FastAPI |
| Database | PostgreSQL |
| Baseline OCR | Tesseract |
| Improved OCR | PaddleOCR |
| Image processing | OpenCV and Pillow |
| Field extraction | Python-based parsing and structured extraction |
| Optional AI assistance | Gemini API |
| Authentication | JWT and secure password hashing |
| Automated testing | Pytest and React Testing Library |
| Version control | Git and GitHub |
| Deployment | Docker Compose |

### Architecture and Data Flow

1. Employees upload receipt photographs through the React interface.
2. FastAPI validates the uploaded files and stores the original images.
3. Image processing handles rotation and image enhancement.
4. OCR extracts text and source coordinates.
5. Field extraction converts OCR output into structured receipt records.
6. Confidence and provenance information are stored.
7. A deterministic validation engine checks financial consistency and duplicates.
8. Human reviewers correct uncertain information.
9. The policy engine evaluates expenses against fictional company rules.
10. The workflow engine enforces submission and approval permissions.
11. Approved expenses become available for reporting and export.
12. PostgreSQL stores users, receipts, extracted fields, expenses, policies, reviews and audit records.

The AI extraction service, financial validation engine and expense policy engine will remain separate components.

No LLM will have authority to approve or reject an expense.
### Architecture Diagram


## 8. Baseline and Improved Approaches

The project will compare at least two extraction approaches.

### Baseline

Tesseract OCR combined with regular expressions and rule-based field extraction.

The baseline will extract available receipt text and identify structured fields using predefined parsing rules.

### Improved Approach

PaddleOCR combined with image preprocessing, layout-aware field extraction, confidence assessment and bounding-box provenance.

The improved approach will be evaluated using the same held-out examples as the baseline.

### Human-Verified Approach

The improved extraction results will be presented to users for manual correction and verification.

This approach will be evaluated separately to establish whether human review reduces final expense errors and how much additional review time is required.

The comparison will include performance, limitations, processing time and computational/API costs.

## 9. Financial Validation and Policy Processing

The financial validation engine will implement deterministic rules.

For example:

Subtotal = Sum of extracted line-item totals.

Expected Total = Subtotal + Tax + Other Charges − Discounts.

The calculated amount will be compared with the receipt's extracted total, taking account of available receipt fields and applicable rounding rules.

Validation will identify:

- Missing mandatory fields.
- Invalid currency values.
- Incorrect arithmetic.
- Missing or inconsistent tax information.
- Duplicate receipts.
- Invalid monetary values.
- Unreadable receipt images.

A separate fictional policy engine will define expense limits, evidence requirements and approver permissions.

Expenses exceeding configured limits will be directed to an appropriate exception or escalation process.

All approval actions will require authorization and valid workflow states.

## 10. Initial Fictional Expense Policy

The following example policies will be used for demonstration and testing.

| Category | Maximum amount | Required evidence | Approver |
|---|---:|---|---|
| Meals | €50 | Receipt | Manager |
| Transport | €100 | Receipt | Manager |
| Accommodation | €200 | Receipt | Finance |
| Office supplies | €150 | Receipt | Manager |
| Equipment | €500 | Receipt and justification | Finance |

These are fictional rules and will be configurable through the administrative interface.

## 11. End-to-End User Journeys

The initial product will be designed around five principal user journeys.

### Journey 1: Receipt Upload and Extraction

An employee logs in, uploads a receipt, and the application extracts available purchase information. The employee reviews the extracted fields and saves the record as a draft.

**Expected result:** A structured draft expense with preserved source evidence and extraction provenance.

### Journey 2: Receipt Correction

An employee opens an extracted receipt, identifies an incorrect amount or merchant name, edits the field and saves the correction.

**Expected result:** The corrected value is saved while the original extracted value and correction history remain available.

### Journey 3: Duplicate Receipt Detection

An employee uploads a receipt that already exists in the system. The application identifies the duplicate and flags it for review.

**Expected result:** The duplicate cannot proceed as a separate approved expense without authorized resolution.

### Journey 4: Missing Total and Recovery

An employee uploads an unreadable or incomplete receipt. OCR fails to identify the total. The application sends the record to a manual review queue and allows the employee to upload a clearer image or correct the missing value.

**Expected result:** The system does not fabricate missing financial information and allows recovery through human verification.

### Journey 5: Expense Review, Rejection and Export

An employee submits a verified expense. A reviewer checks the evidence, and an authorized approver evaluates the expense against the configured policy. The approver rejects an expense with a recorded reason. Other eligible approved expenses can subsequently be searched and exported.

**Expected result:** Authorized workflow decisions, preserved status history and correct CSV/JSON export of approved expenses.

## 12. Evaluation Plan and Success Criteria

The project will evaluate document extraction, financial validation, policy processing and complete workflow performance separately.

### 12.1 Extraction Evaluation

The held-out CORD test split will be used to calculate:

- Field-level precision, recall and F1.
- Merchant and date extraction performance.
- Line-item extraction F1.
- Amount exact-match accuracy.
- Subtotal, tax and total exact-match accuracy.
- Arithmetic validation accuracy.

The team will compare the baseline and improved extraction pipelines using the same evaluation examples.

### 12.2 Human Verification Evaluation

The team will compare machine-extracted records against corrected and verified records.

Measurements will include:

- Final field error rate.
- Number of manual corrections.
- Average review time per receipt.
- Missing-field recovery.
- Arithmetic error reduction.

### 12.3 Policy and Workflow Evaluation

The team will prepare:

- At least 30 synthetic policy test cases.
- At least 15 invalid or duplicated receipt cases.
- Unauthorized approval attempts.
- Invalid workflow transition attempts.

Target results:

| Metric | Target |
|---|---:|
| Unauthorized approvals | 0 |
| Workflow integrity violations | 0 |
| Synthetic policy tests | 30/30 passed |
| Mandatory validation tests | 100% passed |
| Exact duplicate detection recall | 100% on prepared exact-duplicate cases |

### 12.4 Product Acceptance Evaluation

The integrated application will be tested against at least five end-to-end user journeys, including failure and recovery.

The team will also demonstrate:

- Batch upload.
- Receipt correction.
- Duplicate detection.
- Missing total recovery.
- Denied approval.
- Approved expense export.

### 12.5 Usability Evaluation

Where practical, at least three people outside the development team will test the application.

The team will record task completion, errors, review time, user difficulties and suggested improvements.

At least one usability improvement will be implemented and evaluated again, or a decision not to change the product will be justified.

All final metrics will be based on actual experiments rather than assumed results.

## 13. GitHub Repository and Development Strategy

The team will create the GitHub repository at the beginning of the project.

The repository will contain:

- Complete project proposal.
- Application source code.
- OCR and extraction components.
- Data preparation scripts.
- Automated tests.
- Architecture diagrams.
- Installation and demonstration instructions.
- Evaluation results.
- Weekly progress reports.

Development will be incremental, with meaningful commits, issues and pull requests.

### Required Milestones

**v0.1 – Feasibility and Baseline**
- Repository established.
- Proposal committed.
- Dataset reviewed.
- OCR baseline implemented.
- Initial extraction evaluation completed.

**v0.2 – Integrated Application**
- Frontend and backend integrated.
- Receipt upload and extraction implemented.
- Human correction and validation available.
- Policy and approval workflow implemented.

**v1.0 – Tested Product**
- Complete application integrated.
- Security and workflow tests completed.
- Evaluation report produced.
- Documentation and demonstration completed.

The team will maintain a dated PROGRESS.md at least weekly.

API keys, private receipt information and restricted dataset copies will not be committed.

## 14. Eight-Week Project Milestones

| Week | Main activities | Deliverables |
|---|---|---|
| 1 | Proposal, GitHub, dataset and architecture | v0.1 foundation |
| 2 | OCR baseline and dataset preparation | Baseline results |
| 3 | Improved extraction and provenance | Improved extraction |
| 4 | Database, authentication and review interface | Core application |
| 5 | Arithmetic, duplicate detection and policy engine | Validation components |
| 6 | Approval workflow, export and integration | v0.2 integrated application |
| 7 | Automated tests, evaluation and usability | Test evidence |
| 8 | Final evaluation, documentation and demonstration | v1.0 release |

Weekly progress will be recorded with actual dates, contributors, results, challenges and corresponding GitHub references.

## 15. Team Responsibilities

The project will be developed by three members.

| Team member | Primary responsibility | Main contributions |
|---|---|---|
| Member 1 – Celestine Anyaegbunam Ugwu | Backend and database | FastAPI, PostgreSQL, authentication, policy and workflow services |
| Member 2 – Dheeraj Erpa | AI and document processing | OCR, extraction, provenance, CORD evaluation and financial validation |
| Member 3 – Humphrey Kobi Momanyi | Frontend and testing | React interface, dashboards, human review, integration and usability testing |

All three members will contribute to documentation, integration, testing and final system demonstrations.

Each member must be able to explain the complete architecture and data flow.

## 16. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Poor receipt image quality | Image preprocessing and manual review |
| OCR inaccuracies | Confidence assessment and human correction |
| Language variation | Document dataset limitations and test supported languages |
| Incorrect currency interpretation | Explicit currency normalization |
| False duplicate detection | Exact hashing and similarity-based review |
| Unauthorized approval | Backend RBAC and atomic transactions |
| API cost escalation | Local OCR and controlled API usage |
| Data leakage | Access restrictions and secure storage |
| Integration delays | Incremental development and automated tests |
| Limited dataset coverage | Supplementary synthetic and independently reviewed receipts |

## 17. Expected Outcomes

At completion, the project is expected to deliver:

1. A working web-based receipt-to-expense application.
2. Automated OCR and structured receipt extraction.
3. Source-region highlighting and field-level provenance.
4. Financial validation and duplicate detection.
5. A human correction and review interface.
6. A configurable fictional expense policy engine.
7. A secure, auditable approval and rejection workflow.
8. Searchable approved expenses and CSV/JSON exports.
9. Baseline and improved extraction evaluation.
10. Policy, workflow and usability evaluation evidence.
11. A documented GitHub repository with incremental development history.
12. A reproducible local installation and demonstration.

## 18. Conclusion

ReceiptWise aims to demonstrate how AI-based document processing can be integrated with reliable financial validation, human verification and deterministic business workflows.

By separating document extraction from expense policy decisions, the application will provide an auditable and controlled approach to receipt processing and simulated expense management.

The project will contribute both a functional software product and an experimental evaluation of the accuracy, reliability, efficiency and practical limitations of automated receipt-to-expense processing.

---

**Document status:** Initial project proposal – Version 0.1

**Next review:** Following project architecture and dataset inspection.