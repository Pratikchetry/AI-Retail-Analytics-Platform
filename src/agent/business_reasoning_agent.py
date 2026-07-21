from dataclasses import dataclass

from src.llm.local_llm import LocalLLM


@dataclass
class BusinessReasoningResult:

    answer: str
    reasoning: str
    evidence: str
    confidence: str


class BusinessReasoningAgent:

    def __init__(self):

        self.llm = LocalLLM()

    def reason(
        self,
        question: str,
        context: str,
        sql_result: str = None
    ) -> BusinessReasoningResult:

        sql_section = ""
        if sql_result and sql_result not in ("NO_SQL_REQUIRED", "INFORMATION_NOT_AVAILABLE"):
            sql_section = f"SQL EXECUTION RESULT (GROUND TRUTH — USE THIS FIRST):\n{sql_result}\n\n"

        prompt = f"""
You are a Senior Revenue Intelligence Consultant.

EVIDENCE HIERARCHY:
1. SQL EXECUTION RESULT = ground truth. Never contradict it.
2. KNOWLEDGE BASE = context only. Use to explain, never to override.
3. If SQL empty/None, use knowledge base as primary.

{sql_section}KNOWLEDGE BASE (CONTEXT ONLY):
{context}

QUESTION: {question}

CRITICAL INSTRUCTIONS:
- If the SQL EXECUTION RESULT contains data, you MUST use it as your ANSWER.
- Do NOT say "the SQL result does not answer the question". The SQL was written by an expert.
- If the SQL returns a single row, that row is the answer.
- Never invent numbers. All money is GBP (£).

Return exactly:

ANSWER:
...

REASONING:
...

EVIDENCE:
...

CONFIDENCE:
...
"""

        response = self.llm.generate(prompt)

        answer = ""
        reasoning = ""
        evidence = ""
        confidence = ""

        current = None

        for line in response.splitlines():

            line = line.strip()

            if line.startswith("ANSWER:"):

                current = "answer"

                answer += (
                    line.replace(
                        "ANSWER:",
                        ""
                    ).strip()
                )

                continue

            if line.startswith("REASONING:"):

                current = "reasoning"

                reasoning += (
                    line.replace(
                        "REASONING:",
                        ""
                    ).strip()
                )

                continue

            if line.startswith("EVIDENCE:"):

                current = "evidence"

                evidence += (
                    line.replace(
                        "EVIDENCE:",
                        ""
                    ).strip()
                )

                continue

            if line.startswith("CONFIDENCE:"):

                current = "confidence"

                confidence += (
                    line.replace(
                        "CONFIDENCE:",
                        ""
                    ).strip()
                )

                continue

            if current == "answer":
                answer += "\n" + line

            elif current == "reasoning":
                reasoning += "\n" + line

            elif current == "evidence":
                evidence += "\n" + line

            elif current == "confidence":
                confidence += "\n" + line

        return BusinessReasoningResult(
            answer=answer.strip(),
            reasoning=reasoning.strip(),
            evidence=evidence.strip(),
            confidence=confidence.strip()
        )