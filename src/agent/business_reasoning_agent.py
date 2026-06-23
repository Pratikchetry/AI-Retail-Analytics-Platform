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
        context: str
    ) -> BusinessReasoningResult:

        prompt = f"""
You are a Senior Revenue Intelligence Consultant.

Question:
{question}

Retrieved Context:
{context}

Instructions:

1. Do NOT summarize the whole context.

2. Find only evidence directly relevant
to the question.

3. Rank evidence if multiple facts exist.

4. If a single best answer exists,
return ONLY that answer.

5. If information is missing,
explicitly say:

"Information not available in knowledge base."

6. Use business reasoning.

7. Never invent facts.

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