## 2024-05-16 - Cache DOM nodes in BeautifulSoup Loops
**Learning:** Repetitive find()/find_all() calls on the same parent element within a loop create a measurable performance bottleneck during HTML parsing.
**Action:** Always cache the result of find() or find_all() calls within the local scope of the loop if the element needs to be accessed multiple times.
