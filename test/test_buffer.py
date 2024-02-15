#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-02-02
# Copyright © 2024 Davidson Engineering Ltd.
# ---------------------------------------------------------------------------

import pytest

from buffered.buffer import Buffer


def test_buffer():
    buffer = Buffer()
    assert buffer.empty()
    assert not buffer.not_empty()
    assert buffer.size() == 0
    assert buffer.get() is None
    assert buffer.peek() is None
    assert buffer.dump() == []
    buffer.put(1)
    assert not buffer.empty()
    assert buffer.not_empty()
    assert buffer.size() == 1
    assert buffer.get() == 1
    assert buffer.empty()
    assert not buffer.not_empty()
    assert buffer.size() == 0
    assert buffer.get() is None
    assert buffer.peek() is None
    assert buffer.dump() == []
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert buffer.size() == 3
    assert buffer.peek() == 1
    assert buffer.get() == 1
    assert buffer.size() == 2
    assert buffer.peek() == 2
    assert buffer.get() == 2
    assert buffer.size() == 1
    assert buffer.peek() == 3
    assert buffer.get() == 3
    assert buffer.size() == 0
    assert buffer.get() is None
    assert buffer.peek() is None
    assert buffer.dump() == []
    buffer.put([1, 2, 3])
    assert buffer.size() == 1
    assert buffer.peek() == [1, 2, 3]
    assert buffer.get() == [1, 2, 3]
    assert buffer.size() == 0
    assert buffer.get() is None
    assert buffer.peek() is None
    assert buffer.dump() == []
    buffer.put([1, 2, 3])
    buffer.put([4, 5, 6])
    buffer.put([7, 8, 9])
    assert buffer.size() == 3
    assert buffer.peek() == [1, 2, 3]
    assert buffer.get() == [1, 2, 3]
    assert buffer.size() == 2
    assert buffer.peek() == [4, 5, 6]
    assert buffer.get() == [4, 5, 6]
    assert buffer.size() == 1
    assert buffer.peek() == [7, 8, 9]
    assert buffer.get() == [7, 8, 9]
    assert not buffer


def test_buffer_iter():
    buffer = Buffer([1, 2, 3])
    assert list(buffer) == [1, 2, 3]
    buffer = Buffer()
    assert list(buffer) == []


def test_buffer_copy():
    buffer = Buffer([1, 2, 3])
    buffer_copy = buffer.copy()
    assert buffer == buffer_copy
    assert buffer is not buffer_copy
    buffer_copy.put(4)
    assert buffer != buffer_copy


def test_buffer_get_index():
    buffer = Buffer()
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert buffer.get(0) == 1
    assert buffer.get(1) == 3
    assert buffer.get(0) == 2
    assert buffer.get() is None
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert buffer.peek(-1) == 3
    assert buffer.peek(-2) == 2
    assert buffer.peek(-3) == 1
    with pytest.raises(IndexError):
        buffer.peek(-4)
    assert buffer.get(0) == 1
    assert buffer.get(0) == 2
    assert buffer.get(0) == 3
    assert buffer.get(0) is None


def test_buffer_putback():
    buffer = Buffer()
    buffer.putback(1)
    buffer.putback(2)
    buffer.putback(3)
    assert buffer.size() == 3
    assert buffer.get() == 3
    assert buffer.get() == 2
    assert buffer.get() == 1
    assert buffer.size() == 0
    assert buffer.get() is None
    buffer.putback(1)
    buffer.putback(2)
    buffer.putback(3)
    assert buffer.size() == 3
    assert buffer.get() == 3
    assert buffer.get() == 2
    assert buffer.get() == 1
    assert buffer.size() == 0
    assert buffer.get() is None


def test_buffer_len():
    buffer = Buffer()
    assert len(buffer) == 0
    buffer.put(1)
    assert len(buffer) == 1
    buffer.put(2)
    assert len(buffer) == 2
    buffer.get()
    assert len(buffer) == 1
    buffer.get()
    assert len(buffer) == 0
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.get()
    assert len(buffer) == 1
    buffer.get()
    assert len(buffer) == 0
    buffer.get()
    assert len(buffer) == 0
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.putback(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.get()
    assert len(buffer) == 1
    buffer.get()
    assert len(buffer) == 0
    buffer.get()
    assert len(buffer) == 0
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.putback(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.get()
    assert len(buffer) == 1
    buffer.get()
    assert len(buffer) == 0
    buffer.get()
    assert len(buffer) == 0
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.putback(3)
    assert len(buffer) == 3
    buffer.get()
    assert len(buffer) == 2
    buffer.get()
    assert len(buffer) == 1
    buffer.get()
    assert len(buffer) == 0
    buffer.get()
    assert len(buffer) == 0
    buffer.put(1)
    buffer.put(2)
    buffer.put(3)
    assert len(buffer) == 3


def test_buffer_dataclass():
    from dataclasses import dataclass

    @dataclass
    class Data:
        value: int

    buffer = Buffer([Data(1), Data(2), Data(3)])
    assert buffer.size() == 3


def test_buffer_object():
    class Data:
        def __init__(self, value):
            self.value = value

    buffer = Buffer([Data(1), Data(2), Data(3)])
    assert buffer.size() == 3


def test_buffer_strings():
    string = "hello"
    buffer = Buffer([string])
    buffer.put(string)
    assert buffer.size() == 2

    strings = ["hello"]
    buffer = Buffer(strings)
    assert buffer.size() == 1
    buffer.put(strings)
    assert buffer.size() == 2

    strings = ["hello", "world"]
    buffer = Buffer(strings)
    assert buffer.size() == 2
