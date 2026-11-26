
# ReceiptWise Database Schema Design

## 1. Database Overview

ReceiptWise will use PostgreSQL as its primary relational database.

The database will support:

- User accounts and role-based access control.
- Receipt upload and processing.
- OCR extraction and source provenance.
- Human verification and corrections.
- Expense records and financial validation.
- Expense policy evaluation.
- Approval decisions.
- Audit logging.

Primary keys will use UUID identifiers. Date and time fields will use timezone-aware timestamps. Monetary values will use NUMERIC rather than floating-point types.

## 2. Proposed Database Tables

### 2.1 users

Stores registered system users.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| full_name | VARCHAR(150) | User's full name |
| email | VARCHAR(255) | Unique email address |
| password_hash | TEXT | Secure password hash |
| is_active | BOOLEAN | Account status |
| created_at | TIMESTAMPTZ | Account creation time |

### 2.2 roles

Stores the available system roles.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR(50) | Unique role name |
| description | TEXT | Role description |

Initial roles: Employee, Reviewer, Approver and Administrator.

### 2.3 user_roles

Associates users with one or more roles.

| Column | Type | Description |
|---|---|---|
| user_id | UUID | Foreign key to users |
| role_id | UUID | Foreign key to roles |

Composite primary key: user_id and role_id.

### 2.4 receipts

Stores uploaded receipt metadata.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| uploaded_by | UUID | Foreign key to users |
| original_filename | VARCHAR(255) | Original filename |
| storage_key | TEXT | File storage reference |
| mime_type | VARCHAR(100) | Image or document type |
| file_size | BIGINT | File size in bytes |
| sha256_hash | VARCHAR(64) | File fingerprint |
| processing_status | VARCHAR(40) | Current processing status |
| duplicate_of_receipt_id | UUID | Optional reference to another receipt |
| uploaded_at | TIMESTAMPTZ | Upload timestamp |

Receipt hashes will support duplicate detection. They will not automatically prohibit uploads because identical files may sometimes require investigation.

### 2.5 extraction_runs

Records each OCR processing attempt.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| receipt_id | UUID | Foreign key to receipts |
| engine_name | VARCHAR(100) | OCR engine |
| engine_version | VARCHAR(50) | Engine version |
| processing_status | VARCHAR(40) | Processing result |
| raw_output | JSONB | Original OCR response |
| created_at | TIMESTAMPTZ | Processing timestamp |

A receipt may have multiple extraction runs.

### 2.6 extracted_fields

Stores the fields extracted from each OCR run.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| extraction_run_id | UUID | Foreign key to extraction_runs |
| field_name | VARCHAR(100) | Field identifier |
| raw_text | TEXT | Original extracted text |
| normalized_value | TEXT | Normalized extracted value |
| confidence | NUMERIC(5,4) | OCR confidence |
| bounding_box | JSONB | Source image coordinates |
| source_page | INTEGER | Source page number |
| created_at | TIMESTAMPTZ | Creation timestamp |

Example fields: merchant, receipt_date, receipt_number, subtotal, tax, total and currency.

### 2.7 field_corrections

Maintains the history of human corrections.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| extracted_field_id | UUID | Foreign key to extracted_fields |
| previous_value | TEXT | Previous value |
| corrected_value | TEXT | Corrected value |
| corrected_by | UUID | Foreign key to users |
| correction_reason | TEXT | Optional explanation |
| created_at | TIMESTAMPTZ | Correction timestamp |

Original OCR values must never be overwritten by human corrections.

### 2.8 expenses

Stores normalized expense information associated with a receipt.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| receipt_id | UUID | Unique foreign key to receipts |
| employee_id | UUID | Foreign key to users |
| merchant | VARCHAR(255) | Merchant name |
| expense_date | DATE | Expense date |
| category | VARCHAR(100) | Expense category |
| currency | CHAR(3) | Currency code |
| subtotal | NUMERIC(12,2) | Subtotal |
| tax | NUMERIC(12,2) | Tax amount |
| total | NUMERIC(12,2) | Total amount |
| validation_status | VARCHAR(40) | Financial validation result |
| workflow_status | VARCHAR(40) | Expense workflow status |
| created_at | TIMESTAMPTZ | Creation timestamp |

The initial workflow will use one expense record per receipt.

### 2.9 expense_policy_rules

Stores configurable expense policy requirements.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| category | VARCHAR(100) | Expense category |
| maximum_amount | NUMERIC(12,2) | Maximum permitted amount |
| currency | CHAR(3) | Policy currency |
| evidence_required | BOOLEAN | Supporting evidence requirement |
| approver_role_id | UUID | Foreign key to roles |
| is_active | BOOLEAN | Rule activation status |
| version | INTEGER | Policy version |
| created_at | TIMESTAMPTZ | Creation timestamp |

### 2.10 approval_decisions

Records expense review and approval decisions.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| expense_id | UUID | Foreign key to expenses |
| decided_by | UUID | Foreign key to users |
| decision | VARCHAR(30) | Approved, rejected or returned |
| comments | TEXT | Reviewer comments |
| decided_at | TIMESTAMPTZ | Decision timestamp |

### 2.11 audit_events

Records important system activities.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| actor_id | UUID | Optional foreign key to users |
| entity_type | VARCHAR(100) | Affected record type |
| entity_id | UUID | Affected record identifier |
| action | VARCHAR(100) | Action performed |
| before_data | JSONB | Previous state where applicable |
| after_data | JSONB | New state where applicable |
| created_at | TIMESTAMPTZ | Event timestamp |

Audit records should be append-only for normal application users.

### 2.12 financial_validations

Stores the results of independent financial arithmetic checks.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| expense_id | UUID | Foreign key to expenses |
| subtotal_calculated | NUMERIC(12,2) | Calculated subtotal |
| tax_calculated | NUMERIC(12,2) | Calculated tax |
| expected_total | NUMERIC(12,2) | Expected total |
| extracted_total | NUMERIC(12,2) | Total obtained from receipt |
| discrepancy | NUMERIC(12,2) | Difference between expected and extracted total |
| validation_status | VARCHAR(40) | Passed or failed |
| validation_details | JSONB | Detailed validation results |
| validated_at | TIMESTAMPTZ | Validation timestamp |

Each validation attempt should be preserved rather than overwritten.

### 2.13 policy_evaluations

Stores the results of expense-policy checks.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| expense_id | UUID | Foreign key to expenses |
| policy_rule_id | UUID | Foreign key to expense_policy_rules |
| policy_version | INTEGER | Version of the evaluated policy |
| expense_amount | NUMERIC(12,2) | Amount evaluated |
| currency | CHAR(3) | Expense currency |
| evaluation_result | VARCHAR(40) | Passed, failed or requires review |
| evaluation_details | JSONB | Explanation of the decision |
| evaluated_at | TIMESTAMPTZ | Evaluation timestamp |

Policy evaluations must remain separate from OCR extraction and financial arithmetic validation.

## 3. Key Relationships

- One user can upload multiple receipts.
- One user can have multiple roles.
- One receipt can have multiple OCR extraction runs.
- One extraction run can contain multiple extracted fields.
- One extracted field can have multiple correction records.
- One receipt is associated with one expense in the initial workflow.
- One expense can have multiple approval decisions.
- One policy rule identifies the role responsible for approval.
- Audit events record activities across the system.

- One expense can have multiple financial validation attempts.
- One expense can have multiple policy evaluation records.
- Each policy evaluation references the exact policy rule used.
- Policy evaluation records preserve the policy version and result.
- Financial validation results must not automatically determine policy approval.

## 4. Data Integrity and Security

- Use UUID primary keys and foreign-key constraints.
- Use unique constraints for user email addresses and role names.
- Use NUMERIC for monetary values.
- Use appropriate indexes on frequently searched fields.
- Validate financial arithmetic independently of OCR.
- Preserve original extracted values.
- Restrict access using role-based permissions.
- Store passwords as secure password hashes.
- Keep receipt images in controlled file storage.
- Never commit private receipts or application secrets to GitHub.

## 5. Implementation Strategy

The database will be implemented using:

- PostgreSQL as the database engine.
- SQLAlchemy as the Python ORM.
- Psycopg as the PostgreSQL driver.
- Pydantic for request and response validation.

Database migrations will be introduced using Alembic before the schema is deployed to a shared environment.

## 6. Future Extensions

The schema may later be extended to support:

- Multiple receipts per expense claim.
- Multiple currencies and exchange rates.
- Policy evaluation history.
- Reimbursement tracking.
- Advanced duplicate detection.
- Department-level approval workflows.
