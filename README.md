# Visualize number vector on text using colored html

## Usage
Input:
```python
from html_text_color import from_tokens
html = from_tokens(["I", " am", " a", " sentence", "."], [1, 2, 3, 4, 5], dim_order="b")
```
Output html:
<p><span style="color: rgb(0, 0, 0)">I</span><span style="color: rgb(0, 0, 63)"> am</span><span style="color: rgb(0, 0, 127)"> a</span><span style="color: rgb(0, 0, 191)"> sentence</span><span style="color: rgb(0, 0, 255)">.</span></p>
<br/>

Input:
```python
html = from_tokens(
    [["I", "▁am", "▁a", "▁sentence", "."],
    ["I", "▁am", "▁another", "▁sentence", "."]],
    [[[1, 0, 5], [2, 0, 2], [3, 0, 3], [4, 0, 4], [5, 0, 5]],
    [[5, 0, 0], [4, 2, 0], [3, 4, 0], [2, 6, 0], [1, 8, 0]]],
    dim_order="rgb"
)
```
Output html:
<p><span style="color: rgb(0, 0, 255)">I</span><span style="color: rgb(63, 0, 0)"> am</span><span style="color: rgb(127, 0, 85)"> a</span><span style="color: rgb(191, 0, 170)"> sentence</span><span style="color: rgb(255, 0, 255)">.</span></p><p><span style="color: rgb(255, 0, 0)">I</span><span style="color: rgb(191, 63, 0)"> am</span><span style="color: rgb(127, 127, 0)"> another</span><span style="color: rgb(63, 191, 0)"> sentence</span><span style="color: rgb(0, 255, 0)">.</span></p>
<br/>

Input:
```python
from html_text_color import from_ids
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
html = from_ids(tokenizer.encode("I am a sentence."), tokenizer, [1, 2, 3, 4, 5])
```
Output html:
<p><span style="color: rgb(0, 0, 0)">I</span><span style="color: rgb(63, 0, 0)"> am</span><span style="color: rgb(127, 0, 0)"> a</span><span style="color: rgb(191, 0, 0)"> sentence</span><span style="color: rgb(255, 0, 0)">.</span></p>