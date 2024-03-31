from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError
import numpy as np

replacements = {"▁": " ", "<0x0A>": "<br/>", "Ġ": " ", "\n": "<br>"}


def process_color_nums(color_nums, normalize=True, color_order="rgb"):
    color_nums = np.array(color_nums)
    if color_nums.ndim == 1:
        color_nums = color_nums[:, None]

    assert color_nums.shape[1] <= 3, "color_nums must have 1-3 columns"

    if normalize:
        color_nums = color_nums - color_nums.min(axis=0)
        color_nums = (color_nums / np.clip(color_nums.max(axis=0), 1e-6, None)) * 255

    color_nums = color_nums.astype(int)

    tmp = np.zeros((color_nums.shape[0], 3), dtype=int)
    for i, d in enumerate("rgb"):
        if d in color_order and color_nums.shape[1] > color_order.index(d):
            tmp[:, i] = color_nums[:, color_order.index(d)]
    return tmp


def from_text(tokens, color_nums, normalize=True, color_order="rgb", beautify=True):
    tokens = tokens.copy()
    if type(tokens[0]) == list:
        color_nums = [
            process_color_nums(cn, normalize, color_order) for cn in color_nums
        ]

    else:
        color_nums = process_color_nums(color_nums, normalize, color_order)
        color_nums = color_nums[None, ...]
        tokens = [tokens]

    if beautify:
        for i, ts in enumerate(tokens):
            for j, _t in enumerate(ts):
                for old, new in replacements.items():
                    tokens[i][j] = tokens[i][j].replace(old, new)

    html = ET.Element("html")
    body = ET.Element("body")
    html.append(body)
    for tok_paragraph, col_paragraph in zip(tokens, color_nums):
        p = ET.Element("p")
        body.append(p)
        for tok, col in zip(tok_paragraph, col_paragraph):
            try:
                span = ET.fromstring(f"<span>{tok}</span>")
            except ParseError:
                span = ET.Element("span")
                span.text = tok
            span.attrib["style"] = (
                f"color: rgb({col[0]}, {col[1] if len(col)>1 else 0}, {col[2] if len(col)>2 else 0})"
            )
            p.append(span)

    return ET.tostring(html).decode("utf-8")


def from_ids(
    ids,
    tokenizer,
    color_nums,
    normalize=True,
    color_order="rgb",
    beautify=True,
):
    if isinstance(ids[0], list):
        tokens = [tokenizer.convert_ids_to_tokens(i) for i in ids]
    else:
        tokens = tokenizer.convert_ids_to_tokens(ids)
    return from_text(tokens, color_nums, normalize, color_order, beautify)
