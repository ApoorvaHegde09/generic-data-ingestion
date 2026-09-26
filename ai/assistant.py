import ollama
from ai.rag import retrieve_context

from ai.tools import (
    get_latest_ingestion_run,
    get_ingestion_history,
    get_failed_ingestions
)

conversation_history = []

def process_question(question: str, db):

    # Ask the AI which tool is needed
    tool_prompt = f"""
You are a tool selection assistant.

Your job is to choose exactly ONE tool for the user's current question.

Conversation history:
{conversation_history}

Current user question:
{question}

Available tools:

1. latest_ingestion

Use this when the user asks about the MOST RECENT ingestion run.

Examples:
- What was my last ingestion?
- What was the latest ingestion?
- How many sources were successful in the latest run?
- How many failed in the last ingestion?
- And how many were successful?
- What about that run?

2. ingestion_history

Use this when the user asks for MULTIPLE ingestion runs or the complete history.

Examples:
- Show my ingestion history.
- Show all ingestion runs.
- What were my previous ingestion runs?
- Show all the runs.

3. failed_ingestions

Use this ONLY when the user asks which INGESTION RUNS had failures.

Examples:
- Which ingestion runs had failures?
- Show me the failed ingestion runs.
- Which runs failed?

IMPORTANT:
Do NOT choose failed_ingestions just because the question contains the word "failed".

4. documentation_rag

Use this when the user asks HOW THE SYSTEM WORKS or asks about information contained in the project documentation.

Examples:
- How does the ingestion system work?
- How does the ingestion system handle failed API requests?
- What happens when an API request fails?
- What does an ingestion run track?
- How does the AI assistant work?
- What technology does the AI assistant use?
- How are API responses stored?
- How does the ingestion process work?

IMPORTANT:
Questions about HOW the system works should use documentation_rag.

Questions about WHICH RUNS failed should use failed_ingestions.

Questions about the LATEST RUN should use latest_ingestion.

Return ONLY one exact value:

latest_ingestion
ingestion_history
failed_ingestions
documentation_rag
"""

    tool_response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": tool_prompt
            }
        ]
    )

    selected_tool = tool_response["message"]["content"].strip()

    # Validate the AI's tool selection
    allowed_tools = {
    "latest_ingestion",
    "ingestion_history",
    "failed_ingestions",
    "documentation_rag"
}

    if selected_tool not in allowed_tools:
        selected_tool = "latest_ingestion"

    # Execute the selected tool
    if selected_tool == "ingestion_history":
        data = get_ingestion_history(db)

    elif selected_tool == "failed_ingestions":
        data = get_failed_ingestions(db)

    elif selected_tool == "documentation_rag":
        data = retrieve_context(question)

    else:
        data = get_latest_ingestion_run(db)
    # Give the tool result to the AI
    answer_prompt = f"""
You are a Data Engineering Assistant.

The system has already retrieved the correct data needed to answer the user's question.

Conversation history:
{conversation_history}

User question:
{question}

Retrieved data:
{data}

Answer the user's question directly using the retrieved data.

Rules:
- Treat the retrieved data as the source of truth.
- Do not say you do not have information when the answer exists in the retrieved data.
- Do not mention the tool or retrieval process.
- Do not use outside knowledge.
- Do not invent information.
- If the user asks about the latest ingestion, use the values from the retrieved data.
- If the user asks how many sources were successful, use successful_sources.
- If the user asks how many sources failed, use failed_sources.
- If the user asks for the run status, use status.
- Keep the answer short and natural.

Example:

Retrieved data:
{{'run_id': 1, 'status': 'success', 'total_sources': 2, 'successful_sources': 2, 'failed_sources': 0}}

Question:
What was my last ingestion?

Good answer:
The latest ingestion was run 1 and completed successfully. It processed 2 sources, with all 2 successful and 0 failed.
"""

    answer_response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": answer_prompt
            }
        ]
    )

    answer = answer_response["message"]["content"]

    conversation_history.append({
        "user": question,
        "assistant": answer
    })

    return {
        "answer": answer,
        "tool_used": selected_tool
    }