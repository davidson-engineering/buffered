#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-02-02
# ---------------------------------------------------------------------------
"""Example use of the Buffered package."""
# ---------------------------------------------------------------------------

from buffered.buffer import Buffer, PacketBuffer, PackagedBuffer


def main():

    # Create a buffer
    buffer = Buffer()
    buffer.append(1)
    buffer.append(2)
    buffer.append(3)
    buffer.append(4)
    buffer.append(5)
    print(buffer)
    print(buffer.pop())
    print(buffer)
    print(buffer.pop())
    print(buffer)

    # Create a packet buffer
    packet_buffer = PacketBuffer()
    packet_buffer.append((1, 2, 3))
    packet_buffer.append((4, 5, 6))
    packet_buffer.append((7, 8, 9))
    print(packet_buffer)
    print(packet_buffer.pop())
    print(packet_buffer)
    print(packet_buffer.pop())
    print(packet_buffer)

    # Create a packaged buffer with a packager
    from buffered.packager import SeparatorPackager

    packager = SeparatorPackager(sep_major="|", sep_minor=";")
    packaged_buffer = PackagedBuffer(packager=packager)
    packaged_buffer.append((1, 2, 3))
    packaged_buffer.append((4, 5, 6))
    packaged_buffer.append((7, 8, 9))
    print(packaged_buffer)
    print(packaged_buffer.pop())


if __name__ == "__main__":
    main()
