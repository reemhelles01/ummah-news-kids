import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def generate_kids_news(topic):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not found."

    client = Anthropic(api_key=api_key)

    prompt = f"""
Act as a Muslim educator creating a weekly world news summary for children (ages 6–12) for a platform called "Ummah News Kids".

Topic Focus: {topic}

Create 3 short news stories.

For EACH story:
- What happened
- Why it matters
- What Islam teaches
- What we can do

Then add:
- Good news
- One reflection question

Keep it simple, calm, and positive.
Format in Markdown.
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    except Exception as e:
        return f"Error: {e}"


def save_to_file(content, topic):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"News/news_{topic}_{date_str}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    return filename


if __name__ == "__main__":
    topic = input("Enter topic (or 'general'): ")

    content = generate_kids_news(topic)

    if "Error" not in content:
        filename = save_to_file(content, topic)
        print(content)
        print(f"\nSaved to {filename}")
    else:
        print(content)
def update_index(news_html):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find("<div class=\"card\">")
    end = content.find("</div>", start) + 6

    new_content = content[:start] + f'''
  <div class="card">
    <h2>📰 Today's Story</h2>
    {news_html}
  </div>
''' + content[end:]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)


