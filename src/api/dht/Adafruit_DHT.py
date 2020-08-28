def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2, 3 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), Raspberry Pi 3 or not a Raspberry Pi.
    Raspberry Pi 2 (model B+), Raspberry Pi 3,Raspberry Pi 3 (model B+) or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # 2835 is pi 3
    # 2837 is pi 3b+
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    elif match.group(1) == 'BCM2835':
        # Pi 3
        return 3
    elif match.group(1) == 'BCM2837':
        # Pi 3b+
        return 3
    else:
        # Something else, not a pi.
        return None