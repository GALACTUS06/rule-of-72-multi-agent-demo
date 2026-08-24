import boto3
import json
import os
import re
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

try:
    from .tools import rule_of_72, compare_rates, plot_growth
except ImportError:
    from tools import rule_of_72, compare_rates, plot_growth


# ---------- Bedrock LLM Wrapper ----------
class BedrockLLM:
    def __init__(self, model=None, region=None):
        """Connect to AWS Bedrock using arguments or environment variables."""
        self.region = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.model = model or os.getenv("BEDROCK_MODEL") or "meta.llama3-8b-instruct-v1:0"
        self.client = boto3.client(service_name="bedrock-runtime", region_name=self.region)

    def generate(self, prompt):
        """Generate an explanation using Llama3 (Bedrock)"""
        system_prompt = (
            "You are a helpful financial education assistant. "
            "Always explain the Rule of 72 as a simple personal finance rule "
            "to estimate how long money takes to double at a given interest rate. "
            "Do NOT mention physics, biology, or climate. "
            "Use clear, short English sentences."
        )

        full_prompt = f"{system_prompt}\n\nUser question: {prompt}"

        body = {
            "prompt": full_prompt,
            "max_gen_len": 200,
            "temperature": 0.5,
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model,
                body=json.dumps(body)
            )
        except NoCredentialsError as exc:
            raise RuntimeError(
                "AWS credentials not found. Configure them locally with 'aws configure'."
            ) from exc
        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(f"Bedrock request failed: {exc}") from exc

        result = json.loads(response["body"].read())
        return result.get("generation", "").strip()


# ---------- Base Agent ----------
class BaseAgent:
    def __init__(self, name, llm=None):
        self.name = name
        self.llm = llm
        self.memory = []

    def remember(self, entry):
        self.memory.append(entry)


# ---------- Calculator Agent ----------
class CalculatorAgent(BaseAgent):
    def __init__(self, name="CalculatorAgent"):
        super().__init__(name)

    def handle_compute(self, payload):
        """Perform financial math based on Rule of 72"""
        if "rate" in payload:
            rate = float(payload["rate"])
            result = rule_of_72(rate=rate)
            explanation = f"T = 72 / {rate} = {result['years']:.2f} years"
            return {"math": explanation, "result": result}

        if "time" in payload:
            time_val = float(payload["time"])
            result = rule_of_72(time=time_val)
            explanation = f"R = 72 / {time_val} = {result['rate_pct']:.2f}%"
            return {"math": explanation, "result": result}

        if "compare_rates" in payload:
            rates = payload["compare_rates"]
            result = compare_rates(rates)
            return {"result": result}

        return {"error": "Invalid payload"}


# ---------- Teacher Agent ----------
class TeacherAgent(BaseAgent):
    def __init__(self, name="TeacherAgent", llm=None, calculator=None):
        super().__init__(name, llm)
        self.calculator = calculator

    def receive_user(self, text):
        """Interpret user input and coordinate with calculator + LLM"""
        self.remember({"user": text})
        t = text.lower()

        # === Plotting feature ===
        if "plot" in t or "chart" in t:
            principal = 1000
            rate = 8.0
            years = 10

            # Detect principal (e.g., "plot 5000 at 6%")
            m_principal = re.search(r"(?:plot|growth)\s*(?:[a-z\s]*)?(\d+(\.\d+)?)", text, re.I)
            if m_principal:
                principal = float(m_principal.group(1))

            # Detect rate (e.g., "at 6%")
            m_rate = re.search(r"at\s+(\d+(\.\d+)?)\s*%", text, re.I)
            if m_rate:
                rate = float(m_rate.group(1))

            # Detect years (optional)
            m_years = re.search(r"(\d+)\s*(years|yrs|y)", text, re.I)
            if m_years:
                years = int(m_years.group(1))

            filename = f"growth_{principal:.0f}_{rate:.1f}pct.png"
            try:
                plot_growth(principal=principal, rate_pct=rate, years=years, save_path=filename)
                summary = f"A growth chart for principal {principal:.0f} at {rate:.1f}% for {years} years has been saved as '{filename}'."
            except Exception as e:
                summary = f"Plot failed: {e}"
            return {"summary": summary}

        # === Financial logic ===
        m_rate = re.search(r"(\d+(\.\d+)?)\s*%", text)
        m_time = re.search(r"(\d+(\.\d+)?)\s*(years|yrs|y)\b", text)
        m_compare = re.findall(r"(\d+(\.\d+)?)", text) if "compare" in t else None

        # Compare rates
        if "compare" in t and m_compare:
            rates = [float(x[0]) for x in m_compare]
            resp = self.calculator.handle_compute({"compare_rates": rates})
            summary = "\n".join([
                f"{r['rate_pct']}% → {r.get('doubling_years','?'):.2f} years"
                for r in resp["result"] if "doubling_years" in r
            ])
            return {"summary": summary}

        # Given rate → find years
        if m_rate:
            rate = float(m_rate.group(1))
            resp = self.calculator.handle_compute({"rate": rate})
            math = resp["math"]
            prompt = f"In finance, using the Rule of 72, explain in simple English what this means: {math}."
            explanation = self.llm.generate(prompt)
            return {"summary": explanation, "math": math}

        # Given time → find rate
        if m_time:
            time_val = float(m_time.group(1))
            resp = self.calculator.handle_compute({"time": time_val})
            math = resp["math"]
            prompt = f"In finance, using the Rule of 72, explain in simple English what this means: {math}."
            explanation = self.llm.generate(prompt)
            return {"summary": explanation, "math": math}

        # General fallback
        prompt = f"The user said: '{text}'. Please explain the Rule of 72 in simple terms."
        explanation = self.llm.generate(prompt)
        return {"summary": explanation}


# ---------- Build and Run ----------
def build_agents():
    llm = BedrockLLM()
    calc = CalculatorAgent()
    teacher = TeacherAgent(llm=llm, calculator=calc)
    return teacher


def demo_console():
    print("=== Rule of 72 Bedrock Multi-Agent Demo ===")
    teacher = build_agents()

    while True:
        text = input("\nYou: ").strip()
        if not text or text.lower() in ["exit", "quit"]:
            break

        try:
            resp = teacher.receive_user(text)
        except RuntimeError as exc:
            print(f"\nError: {exc}")
            continue

        print("\nTeacher Summary:")
        print(resp.get("summary", ""))

        if "math" in resp:
            print("\nMath / steps:")
            print(resp["math"])


if __name__ == "__main__":
    demo_console()