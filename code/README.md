# Rule of 72 Multi-Agent Demo (AWS Bedrock + Llama 3)

This project is a simple **multi-agent console prototype** that demonstrates the Rule of 72 financial concept using **AWS Bedrock** as the LLM backend (Meta Llama 3 model).  

The system features two cooperating agents:
- **TeacherAgent** — explains financial math using natural language (via Bedrock Llama 3)
- **CalculatorAgent** — performs Rule of 72 calculations and optional growth chart plotting

---

## Installation

### 1. Clone or copy project files

```
agents.py
tools.py
requirement.txt
```

### 2. Install dependencies

You can use Anaconda or a virtual environment.

```bash
pip install -r requirement.txt
```

Or install manually:

```bash
pip install boto3 matplotlib
```

### 3. (Optional) Configure AWS Bedrock credentials

Ensure your AWS credentials are properly set up:

```bash
aws configure
```

Or manually set environment variables:

```bash
set AWS_ACCESS_KEY_ID=your_key
set AWS_SECRET_ACCESS_KEY=your_secret
set AWS_DEFAULT_REGION=us-east-1
```

---

## Architecture & Workflow

```
User Input
   │
   ▼
TeacherAgent ──► AWS Bedrock (Llama 3) for text explanations
   │
   ▼
CalculatorAgent ──► Rule of 72 calculation / growth plot
```

### Agent Roles & Workflow

#### TeacherAgent
- Parses user input
- Requests explanation from Bedrock (Llama 3)
- Returns final summary and math result

#### CalculatorAgent
- Handles numeric computations and chart generation
- Implements the Rule of 72 formula

### Workflow
1. The user asks a question (e.g., "At 8%?")
2. → TeacherAgent detects rate
3. → CalculatorAgent computes result
4. → Bedrock (Llama 3) generates a clear explanation

---

## Running the Demo

```bash
python agents.py
```

### Example console session

```
=== Rule of 72 Bedrock Multi-Agent Demo ===

You: At 8%
Teacher Summary:
Your money will double in about 9 years at an 8% annual rate.

Math / steps:
T = 72 / 8.0 = 9.00 years
```

---

## Example Conversations

### Example 1: Given Interest Rate
```
You: At 8%

Teacher Summary:
The Rule of 72 says that at 8% interest, your investment will double in about 9 years.

Math / steps:
T = 72 / 8.0 = 9.00 years
```

### Example 2: Given Time to Double
```
You: double in 5 years

Teacher Summary:
To double your money in 5 years, you need an interest rate of about 14.4%.

Math / steps:
R = 72 / 5.0 = 14.40%
```

### Example 3: Growth Chart Generation
```
You: plot Growth 6000 at 8%

Teacher Summary:
A growth chart for principal 6000 at 8.0% for 10 years has been saved as 'growth_6000_8.0pct.png'.
```

---

## LLM Platform Used

This system uses **AWS Bedrock** with **Meta Llama 3 Instruct (8B)** model  
(`meta.llama3-8b-instruct-v1:0`) as the backend for generating financial explanations.

Bedrock ensures a secure, managed environment and fits within AWS's free-tier trial limits.

---

## Project Structure

```
.
├── agents.py          # Main multi-agent system
├── tools.py           # Rule of 72 calculations and plotting
├── requirement.txt    # Python dependencies
└── README.md          # This file
```

---

## Features

- Rule of 72 calculations (rate → time, time → rate)
- Natural language explanations via AWS Bedrock (Llama 3)
- Growth chart visualization with matplotlib
- Multi-agent architecture (Teacher + Calculator)
- Interactive console interface

---

## Notes

- Ensure your AWS account has access to Bedrock and the Llama 3 model
- The system uses a simple regex-based parser for user input
- Charts are saved as PNG files in the current directory

---

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'boto3'`  
**Solution**: Run `pip install -r requirement.txt`

**Issue**: AWS credentials error  
**Solution**: Configure AWS CLI with `aws configure` or set environment variables

**Issue**: Bedrock model access denied  
**Solution**: Ensure your AWS account has enabled the Llama 3 model in Bedrock console

---

## License

This is a demo project for educational purposes.