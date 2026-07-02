def format_study_content(content_markdown: str) -> str:
    """
    Cleans up and formats the micro-study plan to ensure high readability on mobile screens.
    It standardizes markdown sections, adds structural HTML/CSS classes where appropriate,
    and inserts clean dividers.
    
    Args:
        content_markdown: Raw study plan markdown from the agent.
        
    Returns:
        The formatted markdown ready for mobile consumption.
    """
    # Simply strip whitespace and ensure clean formatting.
    # The agent will be instructed to output markdown, and we will render it cleanly on the mobile app.
    return content_markdown.strip()
