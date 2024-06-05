import sys
import re

def parse_markdown(md_text):
    html_output = []
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'_(.*?)_')
    monospaced_pattern = re.compile(r'`(.*?)`')
    preformatted_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    def process_paragraph(paragraph):
        # Check for invalid nested markup
        if re.search(r'\*\*.*[`_].*[`_].*\*\*', paragraph) or re.search(r'`.*[\*_].*[\*_].*`', paragraph):
            raise Exception("Invalid markdown syntax")

        # Detect standalone markdown characters and ensure they are properly matched
        if paragraph.count('**') % 2 != 0 or paragraph.count('`') % 2 != 0:
            raise Exception("Invalid markdown syntax")

        # Check for single underscores that are not part of a word or within quotes
        if paragraph == '_' or (paragraph.count('_') % 2 != 0 and not re.search(r'\b_\b', paragraph)):
            raise Exception("Invalid markdown syntax")

        # Allow underscores within words and quotes but not as unmatched pairs
        paragraph = bold_pattern.sub(r'<b>\1</b>', paragraph)
        paragraph = italic_pattern.sub(r'<i>\1</i>', paragraph)
        paragraph = monospaced_pattern.sub(r'<tt>\1</tt>', paragraph)
        return paragraph

    preformatted_matches = list(preformatted_pattern.finditer(md_text))
    last_end = 0
    for match in preformatted_matches:
        start, end = match.span()
        paragraphs = md_text[last_end:start].split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                html_output.append(f'<p>{process_paragraph(paragraph)}</p>')
        preformatted_text = match.group(1).strip()
        html_output.append(f'<pre>{preformatted_text}</pre>')
        last_end = end
    paragraphs = md_text[last_end:].split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            html_output.append(f'<p>{process_paragraph(paragraph)}</p>')

    return '\n'.join(html_output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py /path/to/markdown [--out /path/to/output.html]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) == 4 and sys.argv[2] == '--out':
        output_file = sys.argv[3]

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            md_text = file.read()

        html_output = parse_markdown(md_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(html_output)
        else:
            print(html_output)
    except Exception as e:
        print(f"Error: invalid markdown {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
