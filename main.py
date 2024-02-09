#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-02-02
# ---------------------------------------------------------------------------
"""Example use of the Buffered package."""
# ---------------------------------------------------------------------------


def main():

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

    # Create a packaged buffer with a packager
    from buffered import PackagedBuffer
    from buffered import SeparatorPackager

    packager = SeparatorPackager(sep_major="|", sep_minor=";")
    packaged_buffer = PackagedBuffer(packager=packager)
    packaged_buffer.put((1, 2, 3))
    packaged_buffer.put((4, 5, 6))
    packaged_buffer.put((7, 8, 9))
    print(packaged_buffer)
    print(packaged_buffer.get())
    print(packaged_buffer)
    print(packaged_buffer.get(-1))
    print(packaged_buffer)
    print(packaged_buffer.dump_packed())
    print(packaged_buffer)


if __name__ == "__main__":
    main()
