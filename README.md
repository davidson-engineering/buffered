# buffered
### A set of containers useful for queues and networking.

Some example code

```python
# Create a buffer
from buffered import Buffer

buffer = Buffer()
buffer.put(1)
buffer.put(2)
buffer.put(3)
buffer.put(4)
buffer.put(5)
print(buffer)
print(buffer.get())
print(buffer)
print(buffer.get(-1))
print(buffer)
```
```
1
Buffer(2 ... 5, len=4/4096)
5
Buffer(2 ... 4, len=3/4096)
```
```python
# Create a packaged buffer with a packager
from buffered import PackagedBuffer
from buffered import SeparatorPackager

packager = SeparatorPackager(sep_major="|", sep_minor=";")
packaged_buffer = PackagedBuffer(packager=packager)
packaged_buffer.put((1, 2, 3))
packaged_buffer.put((4, 5, 6))
packaged_buffer.put((7, 8, 9))
packaged_buffer_copy = packaged_buffer.copy()
print(packaged_buffer)
print(packaged_buffer.get())
print(packaged_buffer)
print(packaged_buffer.get(-1))
print(packaged_buffer)
print(packaged_buffer.dump_packed())
print(packaged_buffer)
print(packaged_buffer_copy)
print(packaged_buffer_copy.dump_packed())
```

```
PackagedBuffer((1, 2, 3) ... (7, 8, 9), len=3/4096)
(1, 2, 3)
PackagedBuffer((4, 5, 6) ... (7, 8, 9), len=2/4096)
(7, 8, 9)
PackagedBuffer((4, 5, 6) ... (4, 5, 6), len=1/4096)
['4;5;6|\n']
PackagedBuffer(None ... None, len=0/4096)
PackagedBuffer((1, 2, 3) ... (7, 8, 9), len=3/4096)
['1;2;3|\n', '4;5;6|\n', '7;8;9|\n']
```
