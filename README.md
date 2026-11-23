
# ReceiptWise — Verified Receipt-to-Expense Workflow

ReceiptWise is a receipt-processing and expense-management system designed to convert receipt images into structured expense records.

The system combines Optical Character Recognition (OCR), structured data extraction, financial validation, human verification, and expense-policy checks to support a reliable expense approval workflow.

## Project Objectives

- Extract relevant information from uploaded receipts.
- Identify key fields such as merchant, date, receipt number, tax, and total amount.
- Display extracted information with supporting image evidence.
- Allow users to review and correct OCR results.
- Validate receipt totals and financial calculations.
- Detect potential duplicate receipts.
- Apply configurable expense policies.
- Support review, approval, rejection, and expense reporting.

## Technology Stack

| Component | Planned Technology |
|---|---|
| Frontend | React and TypeScript |
| Backend | Python and FastAPI |
| Database | PostgreSQL |
| Baseline OCR | Tesseract |
| Improved OCR | PaddleOCR |
| Image Processing | OpenCV and Pillow |
| AI Integration | Gemini API (optional) |
| Testing | Pytest |
| Containerization | Docker and Docker Compose |
| Version Control | Git and GitHub |

## Project Structure

```text
ReceiptWise/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── security/
│   ├── tests/
│   └── requirements.txt
├── frontend/
├── ml/
│   ├── data_preparation/
│   ├── baseline/
│   ├── improved/
│   ├── evaluation/
│   └── notebooks/
├── docs/
│   └── diagrams/
├── sample_data/
├── evaluation/
├── .env.example
├── .gitignore
├── PROGRESS.md
└── README.md
```

## Development Status

The project is currently in its initial documentation and setup phase.

See [PROGRESS.md](PROGRESS.md) for completed activities and upcoming milestones.

## Dataset

The project plans to use the CORD v2 receipt dataset for OCR and information-extraction experiments.

Dataset: https://huggingface.co/datasets/naver-clova-ix/cord-v2

Review the dataset's license and terms before downloading or redistributing any data.

## Security

- Credentials and API keys must be stored in environment variables.
- Real secrets must never be committed to GitHub.
- Access to expense records will be controlled through role-based permissions.
- Original receipt images and extracted information must be handled securely.

## Team

This project is being developed by a three-member team.

Team member names and assigned responsibilities will be maintained in the project proposal.

## License

A project license will be selected and added before public release.
