import re
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError

import numpy as np
from matplotlib import colormaps
from ykutil import IGNORE_INDEX, describe_array, log

from html_text_color.util import convert_to_ranks

replacements = {"▁": " ", "<0x0A>": "<br/>", "Ġ": " ", "\n": "<br>"}
stupid_color = re.compile(r"^[rgb]{,3}$")


def process_color_nums(
    color_nums, normalize=True, color_order=None, mn=None, mx=None, darkmode=False
):
    color_nums = np.array(color_nums)
    if color_nums.ndim == 1:
        color_nums = color_nums[:, None]

    if color_order is None:
        if color_nums.shape[1] == 1:
            color_order = "viridis"
        else:
            color_order = "rgb"
    assert color_nums.shape[1] <= 3, "color_nums must have 1-3 columns"

    if normalize:
        color_nums = color_nums - (color_nums.min(axis=0) if mn is None else mn)
        color_nums = (
            color_nums
            / np.clip(color_nums.max(axis=0) if mx is None else mx - mn, 1e-6, None)
        ) * 255

    out = np.zeros((color_nums.shape[0], 3), dtype=int)
    if stupid_color.match(color_order):
        color_nums = color_nums.astype(int)
        for i, d in enumerate("rgb"):
            if d in color_order and color_nums.shape[1] > color_order.index(d):
                out[:, i] = color_nums[:, color_order.index(d)]
    else:
        assert color_nums.shape[1] == 1, f"Invalid color_order {color_order}"
        cmap = colormaps.get_cmap(color_order)
        for i, n in enumerate(color_nums[:, 0]):
            if n == IGNORE_INDEX:
                if darkmode:
                    out[i] = np.array((255, 255, 255))
                else:
                    out[i] = np.array((0, 0, 0))
            else:
                out[i] = np.array(cmap(n)[:3]) * 255
    return out


def from_text(
    tokens,
    color_nums,
    normalize=True,
    color_order=None,
    beautify=True,
    ranked=False,
    darkmode=False,
):
    tokens = tokens.copy()
    if ranked:
        color_nums = convert_to_ranks(color_nums)
    if type(tokens[0]) == list:
        mn = min(min(x) for x in color_nums)
        mx = max(max(x) for x in color_nums)
        color_nums = [
            process_color_nums(
                cn, normalize, color_order, mn=mn, mx=mx, darkmode=darkmode
            )
            for cn in color_nums
        ]

    else:
        mn = min(color_nums)
        mx = max(color_nums)
        color_nums = process_color_nums(
            color_nums, normalize, color_order, mn=mn, mx=mx, darkmode=darkmode
        )
        color_nums = color_nums[None, ...]
        tokens = [tokens]

    if beautify:
        for i, ts in enumerate(tokens):
            for j, _t in enumerate(ts):
                for old, new in replacements.items():
                    tokens[i][j] = tokens[i][j].replace(old, new)

    html = ET.Element("html")
    body = ET.Element("body")
    if darkmode:
        body.attrib["style"] = "background-color: black;"
    html.append(body)
    for tok_paragraph, col_paragraph in zip(tokens, color_nums):
        p = ET.Element("p")
        body.append(p)
        hr = ET.Element("hr")
        body.append(hr)
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
    color_order=None,
    beautify=True,
    ranked=False,
    darkmode=False,
):
    if isinstance(ids[0], list):
        tokens = [tokenizer.convert_ids_to_tokens(i) for i in ids]
    else:
        tokens = tokenizer.convert_ids_to_tokens(ids)
    return from_text(
        tokens, color_nums, normalize, color_order, beautify, ranked, darkmode
    )
