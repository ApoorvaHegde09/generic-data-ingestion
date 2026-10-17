
import ollama

from ai.rag import retrieve_context
from ai.tools import (
    get_latest_ingestion_run,
    get_ingestion_history,
    get_failed_ingestions,
)


# Connect to the local Ollama server
ollama_client = ollama.Client(
    host="http://127.0.0.1:11434"
)

conversation_history = []


def select_tool(question: str) -> str:
    q = question.lower().strip().rstrip("?.!")

    # Questions about uploaded documents
    uploaded_document_keywords = [
        "uploaded document",
        "uploaded file",
        "uploaded pdf",
        "my document",
        "my pdf",
        "my file",
        "technologies mentioned",
        "technologies in",
        "what does my document",
        "what does the document",
        "summarize my document",
        "summarize my uploaded",
        "content of my document",
        "information in my document",
        "extract from my document",
    ]

    if any(keyword in q for keyword in uploaded_document_keywords):
        return "documentation_rag"

    # Questions about project documentation and system behavior
    documentation_keywords = [
        "how does",
        "how do",
        "how is",
        "how are",
        "how can",
        "what happens",
        "how the system",
        "how the ingestion",
        "what technology",
        "how api responses",
        "project documentation",
        "how does the ai assistant",
        "what does an ingestion run track",
        "how are api responses stored",
        "which technologies are used in this project",
        "explain the project",
    ]

    if any(keyword in q for keyword in documentation_keywords):
        return "documentation_rag"

    # Questions about all or previous ingestion runs
    history_keywords = [
        "ingestion history",
        "how many ingestion runs",
        "number of ingestion runs",
        "count of ingestion runs",
        "how many runs",
        "all ingestion runs",
        "all runs",
        "previous ingestion runs",
        "previous runs",
        "show all runs",
        "show me all runs",
        "show me my ingestion history",
        "show my ingestion history",
    ]

    if any(keyword in q for keyword in history_keywords):
        return "ingestion_history"

    # Questions about failed ingestion runs
    failed_keywords = [
        "which runs failed",
        "which ingestion runs",
        "failed ingestion runs",
        "runs had failures",
        "show failed runs",
        "show me the failed runs",
        "which ingestion runs had failures",
    ]

    if any(keyword in q for keyword in failed_keywords):
        return "failed_ingestions"

    # Questions about the latest ingestion
    latest_keywords = [
        "latest ingestion",
        "last ingestion",
        "most recent ingestion",
        "last ingestion run",
        "latest ingestion run",
    ]

    if any(keyword in q for keyword in latest_keywords):
        return "latest_ingestion"

    return "ai_fallback"


def process_question(question: str, db):
    selected_tool = select_tool(question)

    # Use Ollama to classify questions not matched by keywords
    if selected_tool == "ai_fallback":
        tool_prompt = f"""
You are a tool selection assistant.

User question:
{question}

Choose exactly ONE tool.

latest_ingestion:
Questions about the most recent ingestion run.

ingestion_history:
Questions about the number of runs, all runs,
multiple runs, or previous ingestion runs.

failed_ingestions:
Questions asking which ingestion runs had failures.

documentation_rag:
Questions about uploaded documents, PDFs, project documentation,
system behavior, technologies, implementation, or API behavior.

Rules:
- Questions about an uploaded file must use documentation_rag.
- Questions asking how many runs were performed must use
  ingestion_history.
- Questions about the latest run must use latest_ingestion.
- Do not confuse the number of sources with the number of runs.
- Return only one exact tool name.

Allowed tools:
latest_ingestion
ingestion_history
failed_ingestions
documentation_rag
"""

        tool_response = ollama_client.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": tool_prompt,
                }
            ],
        )

        candidate = (
            tool_response["message"]["content"]
            .strip()
            .lower()
        )

        allowed_tools = {
            "latest_ingestion",
            "ingestion_history",
            "failed_ingestions",
            "documentation_rag",
        }

        # Handle extra whitespace or explanatory text in classification
        selected_tool = next(
            (
                tool
                for tool in allowed_tools
                if candidate == tool
            ),
            "latest_ingestion",
        )

    # Execute the selected tool
    if selected_tool == "ingestion_history":
        data = get_ingestion_history(db)

    elif selected_tool == "failed_ingestions":
        data = get_failed_ingestions(db)

    elif selected_tool == "documentation_rag":
        data = retrieve_context(question)

    elif selected_tool == "latest_ingestion":
        data = get_latest_ingestion_run(db)

    else:
        data = get_latest_ingestion_run(db)
        selected_tool = "latest_ingestion"

    # Generate the final answer
    answer_prompt = f"""
You are a helpful Data Engineering Assistant.

Recent conversation:
{conversation_history[-5:]}

Current user question:
{question}

Retrieved information:
{data}

Answer the current question directly using the retrieved information.

General rules:
- Treat retrieved information as the source of truth.
- Never invent facts, counts, technologies, or document contents.
- Do not describe internal tools or retrieval steps.
- Do not begin with phrases like "Here is the answer to your question".
- Keep answers clear, concise, and natural.
- If the retrieved information does not contain the answer,
  say that the information could not be found.
- Use conversation history only to understand follow-up questions.
  Do not use it to invent missing facts.

Ingestion rules:
- One ingestion run means one execution of ingestion.
- Sources are the APIs or inputs processed during a run.
- Never confuse the number of runs with the number of sources.
- For total runs, count the entries in the history data.
- If total_runs is provided, use that value.
- For successful runs, count runs whose status is success.
- For successful sources, use successful_sources.
- For failed sources, use failed_sources.
- For history questions, summarize the actual runs returned.
- Do not assume a list of one run represents multiple runs.

Document and project documentation rules:
- Answer document questions using only the retrieved text.
- List technologies only when they appear in the retrieved text.
- Do not substitute ingestion statistics for document contents.
- If the retrieved text does not contain the requested details,
  explain that the information was not found in the retrieved text.
- Do not claim to have read an entire uploaded file unless its
  contents are actually present in the retrieved information.

Example:
If the retrieved information is:
{{'run_id': 1, 'status': 'success', 'total_sources': 2,
  'successful_sources': 2, 'failed_sources': 0}}

For "What was my latest ingestion run?", answer:
"The latest ingestion was run 1 and completed successfully.
It processed 2 sources, with 2 successful and 0 failed."
"""

    answer_response = ollama_client.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": answer_prompt,
            }
        ],
    )

    answer = answer_response["message"]["content"].strip()

    # Store the recent conversation
    conversation_history.append(
        {
            "user": question,
            "assistant": answer,
        }
    )

    # Keep only the last 10 conversation exchanges
    if len(conversation_history) > 10:
        del conversation_history[:-10]

    return {
        "answer": answer,
        "tool_used": selected_tool,
    }
