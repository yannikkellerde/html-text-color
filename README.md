# Visualize number vector on text using colored html

## Usage
Input:
```python
from html_text_color import from_tokens
html = from_tokens(["I", " am", " a", " sentence", "."], [1, 2, 3, 4, 5], dim_order="b")
```
Output html:  
![test_outputs/test_single.html](test_outputs/test_single.svg)
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
![test_outputs/test_multiple.html](test_outputs/test_multiple.svg)
<br/>

Input:
```python
from html_text_color import from_ids
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
html = from_ids(tokenizer.encode("I am a sentence."), tokenizer, [1, 2, 3, 4, 5])
```
Output html:  
![test_outputs/test_tokens.html](test_outputs/test_tokens.svg)