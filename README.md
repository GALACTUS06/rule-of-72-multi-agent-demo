# Rule of 72 Multi-Agent Financial Education Demo

A small multi-agent console application that explains the Rule of 72 through AWS Bedrock and Meta Llama 3.

## Project Overview

The demo combines two cooperating agents:

- `TeacherAgent` interprets natural-language questions and asks Bedrock for a clear explanation.
- `CalculatorAgent` performs the financial calculations and can compare rates or generate growth charts.

Supported interactions include:

- `At 8%` -> estimated doubling time
- `double in 5 years` -> estimated annual rate
- `compare 6%, 8%, 10%` -> side-by-side estimates
- `plot Growth 6000 at 8%` -> a compound-growth PNG chart

The Rule of 72 is an approximation: doubling years are estimated as `72 / annual rate`.

## Repository Structure

```text
.
├── code/
│   ├── agents.py       # Bedrock wrapper and Teacher/Calculator agents
│   ├── tools.py        # Rule of 72 math and growth plotting
│   └── __init__.py
├── ScreenShot/         # Demo screenshots
├── Report.pdf          # Project report
├── .env.example        # Optional configuration template
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10+
- AWS account with access to Amazon Bedrock
- Access enabled for the Meta Llama 3 model in your AWS region

## Installation

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## AWS Configuration

The project never stores AWS credentials in source code. Configure credentials using the standard AWS credential chain:

```powershell
aws configure
```

Optional environment variables:

- `AWS_REGION` or `AWS_DEFAULT_REGION`
- `BEDROCK_MODEL`

Example values are shown in `.env.example`. Do not put real credentials in that file or commit them to GitHub.

## Run the Demo

From the project root:

```powershell
python -m code.agents
```

Then enter a question at the `You:` prompt. Type `exit` or `quit` to stop.

You can also run the script directly:

```powershell
python code\agents.py
```

## Example Session

```text
=== Rule of 72 Bedrock Multi-Agent Demo ===

You: At 8%

Teacher Summary:
Your money will double in about 9 years at an 8% annual rate.

Math / steps:
T = 72 / 8.0 = 9.00 years
```

## Validation Without AWS

The calculation utilities do not require AWS credentials:

```powershell
python -c "from code.tools import rule_of_72; print(rule_of_72(rate=8))"
```

## Security Notes

- No AWS access keys, secret keys, or tokens are included.
- Keep real credentials in AWS CLI configuration, environment variables, or an IAM role.
- Generated growth charts are ignored by Git so local experiments do not clutter the repository.
- This is an educational demonstration, not financial advice.

## License

MIT. See [LICENSE](LICENSE).

## GitHub Attribution

This project is associated with the following GitHub accounts:

- [@GALACTUS06](https://github.com/GALACTUS06)
- [@XinchenLi-01](https://github.com/XinchenLi-01)
