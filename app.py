import sys
import re

def parse_markdown(md_text, output_format='ANSI'):
    html_output = []
    ansi_output = []
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

        if output_format == 'HTML':
            paragraph = bold_pattern.sub(r'<b>\1</b>', paragraph)
            paragraph = italic_pattern.sub(r'<i>\1</i>', paragraph)
            paragraph = monospaced_pattern.sub(r'<tt>\1</tt>', paragraph)
        elif output_format == 'ANSI':
            paragraph = bold_pattern.sub(r'\033[1m\1\033[0m', paragraph)
            paragraph = italic_pattern.sub(r'\033[3m\1\033[0m', paragraph)
            paragraph = monospaced_pattern.sub(r'\033[7m\1\033[0m', paragraph)
        return paragraph

    preformatted_matches = list(preformatted_pattern.finditer(md_text))
    last_end = 0
    for match in preformatted_matches:
        start, end = match.span()
        paragraphs = md_text[last_end:start].split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                processed_paragraph = process_paragraph(paragraph)
                if output_format == 'HTML':
                    html_output.append(f'<p>{processed_paragraph}</p>')
                elif output_format == 'ANSI':
                    ansi_output.append(f'{processed_paragraph}')
        preformatted_text = match.group(1).strip()
        if output_format == 'HTML':
            html_output.append(f'<pre>{preformatted_text}</pre>')
        elif output_format == 'ANSI':
            ansi_output.append(f'\033[7m{preformatted_text}\033[0m')
        last_end = end
    paragraphs = md_text[last_end:].split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            processed_paragraph = process_paragraph(paragraph)
            if output_format == 'HTML':
                html_output.append(f'<p>{processed_paragraph}</p>')
            elif output_format == 'ANSI':
                ansi_output.append(f'{processed_paragraph}')

    if output_format == 'HTML':
        return '\n'.join(html_output)
    elif output_format == 'ANSI':
        return '\n'.join(ansi_output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py /path/to/markdown [--out /path/to/output.html] [--format=value]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    output_format = 'ANSI' if '--out' not in sys.argv else 'HTML'
    if '--out' in sys.argv:
        output_file = sys.argv[sys.argv.index('--out') + 1]
    if '--format' in sys.argv:
        output_format = sys.argv[sys.argv.index('--format') + 1].upper()

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            md_text = file.read()

        output = parse_markdown(md_text, output_format)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(output)
        else:
            print(output)
    except Exception as e:
        print(f"Error: invalid markdown {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
