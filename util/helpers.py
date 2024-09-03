from util.imports import *
from util.variables import *

def clean_html_text(html_text):
    if html_text is None:
        return None
    decoded_text = unescape(html_text)
    cleaned_text = BeautifulSoup(decoded_text, "html.parser").get_text(separator=" ")
    cleaned_text = " ".join(cleaned_text.strip().split())
    return cleaned_text

def generate_concatenated_text(solution, flags_combination):
    flags_dict = {flag: True if flag in flags_combination else False for flag in FLAGS}
    concatenated_text = solution.concat_text(**flags_dict)
    return {'Solution_ID': solution.id, 'Text': concatenated_text}