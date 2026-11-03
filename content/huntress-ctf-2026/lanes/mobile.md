+++
title = "Mobile (Android)"
date = 2026-11-02
draft = true
layout = "lane"
lane = "mobile"
weight = 50

description = "Static APK analysis without a device: answers hidden in assets with a new codec each day, then computed inside the DEX and recovered with a bounded Dalvik interpreter and an x86-64 interpreter for the JNI side."

tags   = ["ctf", "android", "apk", "dex", "reverse-engineering"]
skills = ["Reverse Engineering"]
toc    = true
+++

The mobile lane was static APK analysis without a device. In the early days the answer sat in an asset, encoded with a new codec each day: plain, then reversed, Base64, XOR, split, hex, Caesar, indexed, and on from there.

Later days stopped storing the answer and computed it inside the DEX instead. That called for a bounded Dalvik interpreter, `mobemu.py`, and an x86-64 interpreter for the JNI mixing functions the bytecode handed off to. The same tooling had to cope with secondary DEX files loaded from assets, split App Bundles and reflection.

The apps also carried anti-debug, root and emulator checks. Since nothing ever ran on a device, those checks only had to be read, never run.
