def build_system_prompt(response_mode: str, rag_context: str = "", web_context: str = "") -> str:
    """Create system prompt with response style and optional contexts"""
    try:
        base_prompt = (
            "You are NeoStats Assist, a reliable AI assistant. "
            "Answer the user with factual accuracy and clear structure. "
            "If context is provided, prioritize it. If context is insufficient, clearly say so."
        )

        mode_prompt = (
            "Respond in concise mode: keep answers short, direct, and summarized in 3-6 lines."
            if response_mode == "Concise"
            else "Respond in detailed mode: provide thorough explanation, steps, and relevant caveats."
        )

        context_blocks = []
        if rag_context:
            context_blocks.append(f"Local Knowledge Base Context:\n{rag_context}")
        if web_context:
            context_blocks.append(f"Live Web Search Context:\n{web_context}")

        joined_context = "\n\n".join(context_blocks).strip()
        if joined_context:
            return f"{base_prompt}\n\n{mode_prompt}\n\nUse the following context:\n{joined_context}"

        return f"{base_prompt}\n\n{mode_prompt}"
    except Exception:
        return "You are a helpful AI assistant."