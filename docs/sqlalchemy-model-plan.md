# ReceiptWise – SQLAlchemy Model Implementation Plan

## 1. Purpose

This document maps the 13 ReceiptWise database tables to SQLAlchemy 2.0 model classes.

The purpose is to establish a consistent implementation plan before creating Python database models or connecting the application to PostgreSQL.

## 2. Technology and implementation standards

- ORM: SQLAlchemy 2.0
- Mapping style: Declarative mapping
- Python typing: `Mapped` and `mapped_column`
- Database: PostgreSQL
- Database driver: Psycopg 3
- Primary keys: UUID
- Monetary values: `NUMERIC(12,2)`
- Timestamps: timezone-aware `TIMESTAMPTZ`
- Structured metadata: PostgreSQL JSONB
- Schema migrations: Alembic
- Relationships: Explicit SQLAlchemy relationships and foreign keys

## 3. Database table-to-model mapping

| Database table | SQLAlchemy class | Purpose |
|---|---|---|
| users | User | Stores application users |
| roles | Role | Defines user roles and permissions |
| user_roles | UserRole | Connects users to assigned roles |
| receipts | Receipt | Stores uploaded receipt metadata |
| extraction_runs | ExtractionRun | Records OCR and extraction attempts |
| extracted_fields | ExtractedField | Stores extracted receipt information |
| field_corrections | FieldCorrection | Records human corrections |
| expenses | Expense | Stores structured expense records |
| expense_policy_rules | ExpensePolicyRule | Defines expense approval policies |
| approval_decisions | ApprovalDecision | Records approval and rejection decisions |
| audit_events | AuditEvent | Records important application activities |
| financial_validations | FinancialValidation | Stores financial validation attempts |
| policy_evaluations | PolicyEvaluation | Stores policy evaluation history |

## 4. Primary keys and data types

All 13 models will use UUID primary keys.

Recommended SQLAlchemy types:

- UUID: `Uuid(as_uuid=True)`
- Text: `String` or `Text`
- Monetary values: `Numeric(12, 2)`
- Date and time: `DateTime(timezone=True)`
- Boolean: `Boolean`
- Structured JSON data: PostgreSQL `JSONB`
- Currency: `String(3)`

Financial calculations must use decimal values rather than Python floating-point numbers.

## 5. Relationships and foreign keys

### User and role management

- User has a one-to-many relationship with Receipt.
- User and Role have a many-to-many relationship through UserRole.
- UserRole will be implemented as an association model with its own UUID primary key and foreign keys to User and Role.

### Receipt processing

- Receipt belongs to one User through its uploader relationship.
- Receipt can have multiple ExtractionRun records.
- Receipt can reference another Receipt through `duplicate_of_receipt_id`.
- Each ExtractionRun can have multiple ExtractedField records.
- Each ExtractedField can have multiple FieldCorrection records.

### Expense processing

- Each Expense references one Receipt.
- `expenses.receipt_id` must have a UNIQUE constraint to enforce one expense per receipt in the initial project scope.
- Each Expense can have multiple FinancialValidation records.
- Each Expense can have multiple PolicyEvaluation records.
- Each Expense can have multiple ApprovalDecision records.

### Policy management

- Each PolicyEvaluation references the ExpensePolicyRule used for evaluation.
- Each ExpensePolicyRule references the Role responsible for approval, where applicable.
- PolicyEvaluation stores the policy version used at evaluation time.

### Audit management

- AuditEvent records important activities performed by users or system processes.
- Its actor reference may be nullable for automated system events.

## 6. Important constraints and indexes

The implementation should include:

1. UUID primary keys on all models.
2. Foreign-key constraints for all relationships.
3. UNIQUE constraint on `expenses.receipt_id`.
4. UNIQUE constraints on appropriate user and role identifiers.
5. Indexes on frequently queried foreign keys.
6. Indexes on receipt status, upload time and duplicate fingerprints.
7. Indexes on expense status, submission time and category.
8. Indexes on financial validation and policy evaluation history.
9. Timezone-aware timestamps.
10. Numeric monetary fields with two decimal places.

## 7. Auditability and historical records

ReceiptWise must preserve the history of important operations.

- ExtractionRun records must not be overwritten when a new OCR attempt occurs.
- FieldCorrection records must preserve original and corrected values.
- FinancialValidation records must preserve previous validation attempts.
- PolicyEvaluation records must preserve the policy version and evaluation result.
- ApprovalDecision records must preserve each decision and its actor.
- AuditEvent records must preserve relevant user and system activities.

Ordinary application users must not be allowed to modify or delete historical audit records.

## 8. SQLAlchemy project structure

The planned model files will be organized as follows:

```text
backend/
└── app/
    ├── models/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── user.py
    │   ├── role.py
    │   ├── user_role.py
    │   ├── receipt.py
    │   ├── extraction_run.py
    │   ├── extracted_field.py
    │   ├── field_correction.py
    │   ├── expense.py
    │   ├── expense_policy_rule.py
    │   ├── approval_decision.py
    │   ├── audit_event.py
    │   ├── financial_validation.py
    │   └── policy_evaluation.py
    └── database/
        ├── __init__.py
        ├── session.py
        └── dependencies.py
```

This is the planned structure. The files will be created during the implementation steps, not all at once.

## 9. Implementation sequence

The actual model implementation will follow this order:

1. Create the shared SQLAlchemy declarative Base.
2. Implement User, Role and UserRole.
3. Implement Receipt.
4. Implement ExtractionRun, ExtractedField and FieldCorrection.
5. Implement Expense.
6. Implement ExpensePolicyRule.
7. Implement FinancialValidation and PolicyEvaluation.
8. Implement ApprovalDecision and AuditEvent.
9. Configure relationships and constraints.
10. Test model imports and metadata registration.

## 10. Important design decisions

- Use SQLAlchemy 2.0 typed declarative models.
- Keep database models separate from Pydantic request and response schemas.
- Use PostgreSQL JSONB for structured OCR output and validation details.
- Store receipt image files outside the database, retaining only controlled storage references and metadata in the Receipt model.
- Do not store passwords in plaintext; store securely hashed passwords.
- Do not overwrite extraction, correction, validation or policy evaluation history.
- Use Alembic for future database schema migrations.
- Keep financial validation independent of expense policy evaluation.

## 11. Completion criteria

The model implementation plan is complete when:

- All 13 database tables are mapped to SQLAlchemy classes.
- All primary keys and foreign-key relationships are identified.
- Important UNIQUE constraints and indexes are documented.
- Financial validation and policy evaluation remain separate.
- Historical records and auditability are addressed.
- The planned Python file structure is documented.